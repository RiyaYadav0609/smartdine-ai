from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import cv2
import numpy as np

PERSON_CLASS = 0
CHAIR_CLASS = 56
DINING_TABLE_CLASS = 60
MODEL_NAME = "yolov8n.pt"

_model = None
_model_error = None


def get_model():
    global _model, _model_error
    if _model is not None:
        return _model
    if _model_error is not None:
        raise RuntimeError(_model_error)
    try:
        from ultralytics import YOLO
        _model = YOLO(MODEL_NAME)
        return _model
    except Exception as e:
        _model_error = f"Unable to load YOLO model: {e}"
        raise RuntimeError(_model_error)


def box_center(x1, y1, x2, y2):
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def mean_optical_flow(prev_gray, gray, roi):
    x1, y1, x2, y2 = roi
    x1, y1 = max(0, int(x1)), max(0, int(y1))
    x2, y2 = max(0, int(x2)), max(0, int(y2))
    if x2 <= x1 or y2 <= y1:
        return 0.0
    prev_crop = prev_gray[y1:y2, x1:x2]
    curr_crop = gray[y1:y2, x1:x2]
    if prev_crop.size == 0 or curr_crop.size == 0:
        return 0.0
    flow = cv2.calcOpticalFlowFarneback(prev_crop, curr_crop, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    return float(np.mean(mag))


def nearest_table(person_box, tables, max_distance=180):
    px, py = box_center(*person_box)
    best_idx, best_dist = None, float("inf")
    for i, tb in enumerate(tables):
        tx, ty = box_center(*tb["box"])
        d = euclidean((px, py), (tx, ty))
        if d < best_dist and d <= max_distance:
            best_dist = d
            best_idx = i
    return best_idx


def activity_label(score):
    if score < 0.8:
        return "low"
    if score < 2.0:
        return "medium"
    return "high"


def analyze_restaurant_video(video_path: str, frame_skip: int = 5, save_annotated: bool = True) -> dict[str, Any]:
    try:
        model = get_model()
    except Exception as e:
        return {"success": False, "error": str(e)}

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return {"success": False, "error": "Could not open video"}

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 1280)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 720)

    out = None
    annotated_path = None
    if save_annotated:
        out_dir = Path(video_path).parent
        annotated_path = str(out_dir / f"annotated_{Path(video_path).name}")
        out = cv2.VideoWriter(annotated_path, cv2.VideoWriter_fourcc(*"mp4v"), max(1.0, fps / max(frame_skip, 1)), (width, height))

    frame_idx = 0
    processed_frames = 0
    prev_gray = None
    person_stats = {}
    people_counts, chair_counts, table_counts = [], [], []
    occupied_table_counts, free_table_counts = [], []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1
        if frame_idx % frame_skip != 0:
            continue
        processed_frames += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        try:
            results = model.track(frame, persist=True, verbose=False)
        except Exception as e:
            cap.release()
            if out is not None:
                out.release()
            return {"success": False, "error": f"Tracking failed: {e}"}

        boxes = results[0].boxes
        people, chairs, tables = [], [], []
        if boxes is not None and len(boxes) > 0:
            xyxy = boxes.xyxy.cpu().numpy()
            clss = boxes.cls.cpu().numpy().astype(int)
            ids = boxes.id.cpu().numpy().astype(int) if boxes.id is not None else [-1] * len(xyxy)
            confs = boxes.conf.cpu().numpy()
            for box, cls_id, track_id, conf in zip(xyxy, clss, ids, confs):
                if conf < 0.35:
                    continue
                x1, y1, x2, y2 = box.tolist()
                item = {"box": [x1, y1, x2, y2], "track_id": int(track_id), "conf": float(conf)}
                if cls_id == PERSON_CLASS:
                    people.append(item)
                elif cls_id == CHAIR_CLASS:
                    chairs.append(item)
                elif cls_id == DINING_TABLE_CLASS:
                    tables.append(item)

        occupied_tables = set()
        for p in people:
            pbox = p["box"]
            pid = p["track_id"]
            table_idx = nearest_table(pbox, tables)
            if pid not in person_stats:
                person_stats[pid] = {"frames": 0, "table_id": None, "activity_scores": []}
            person_stats[pid]["frames"] += 1
            person_stats[pid]["table_id"] = table_idx
            if table_idx is not None:
                occupied_tables.add(table_idx)
            flow_score = mean_optical_flow(prev_gray, gray, pbox) if prev_gray is not None else 0.0
            person_stats[pid]["activity_scores"].append(flow_score)
            x1, y1, x2, y2 = map(int, pbox)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 220, 0), 2)
            cv2.putText(frame, f"Person {pid} | {flow_score:.2f}", (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 220, 0), 2)

        for c in chairs:
            x1, y1, x2, y2 = map(int, c["box"])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 180, 0), 2)
            cv2.putText(frame, "Chair", (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 180, 0), 2)

        for i, t in enumerate(tables):
            x1, y1, x2, y2 = map(int, t["box"])
            color = (0, 0, 255) if i in occupied_tables else (255, 0, 255)
            label = f"Table {i} {'Occupied' if i in occupied_tables else 'Free'}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

        people_counts.append(len(people))
        chair_counts.append(len(chairs))
        table_counts.append(len(tables))
        occupied_table_counts.append(len(occupied_tables))
        free_table_counts.append(max(0, len(tables) - len(occupied_tables)))

        cv2.putText(frame, f"People: {len(people)}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 220, 0), 2)
        cv2.putText(frame, f"Chairs: {len(chairs)}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 180, 0), 2)
        cv2.putText(frame, f"Tables: {len(tables)}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)
        cv2.putText(frame, f"Occupied: {len(occupied_tables)}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        if out is not None:
            out.write(frame)
        prev_gray = gray.copy()

    cap.release()
    if out is not None:
        out.release()

    if processed_frames == 0:
        return {"success": False, "error": "No frames processed"}

    def avg(arr):
        return round(float(np.mean(arr)), 2) if arr else 0.0

    people_summary = []
    for pid, stats in person_stats.items():
        mean_act = round(float(np.mean(stats["activity_scores"])) if stats["activity_scores"] else 0.0, 2)
        people_summary.append({
            "person_id": pid,
            "frames_seen": stats["frames"],
            "assigned_table_id": stats["table_id"],
            "activity_score": mean_act,
            "activity_label": activity_label(mean_act),
        })

    overall_activity = round(float(np.mean([p["activity_score"] for p in people_summary])) if people_summary else 0.0, 2)
    return {
        "success": True,
        "video_path": str(video_path),
        "annotated_video_path": annotated_path,
        "frames_processed": processed_frames,
        "avg_people_count": avg(people_counts),
        "max_people_count": int(max(people_counts)) if people_counts else 0,
        "avg_chair_count": avg(chair_counts),
        "avg_table_count": avg(table_counts),
        "avg_occupied_tables": avg(occupied_table_counts),
        "avg_free_tables": avg(free_table_counts),
        "overall_dining_activity_score": overall_activity,
        "overall_dining_activity_label": activity_label(overall_activity),
        "people_activity": people_summary,
    }
