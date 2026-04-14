from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "live_analysis.json"


def _ensure_file() -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("{}", encoding="utf-8")


def load_live_analysis() -> dict[str, Any]:
    _ensure_file()
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_live_analysis(data: dict[str, Any]) -> None:
    _ensure_file()
    DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def update_restaurant_analysis(restaurant_id: int, payload: dict[str, Any]) -> None:
    data = load_live_analysis()
    data[str(restaurant_id)] = payload
    save_live_analysis(data)


def get_restaurant_analysis(restaurant_id: int) -> dict[str, Any] | None:
    data = load_live_analysis()
    return data.get(str(restaurant_id))
