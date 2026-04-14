"""from pathlib import Path
import pandas as pd
from geopy.distance import geodesic
from app.services.live_analysis import get_restaurant_analysis

DATA = Path(__file__).resolve().parents[2] / "data" / "restaurants.csv"


def load_data():
    return pd.read_csv(DATA)


def calc_waiting_time(crowd_count: int) -> int:
    return max(5, int(crowd_count * 2.2))


def feature_impact(hour, day_of_week, is_weekend, crowd_count):
    return {
        "hour": round(hour * 0.02, 2),
        "day_of_week": round(day_of_week * 0.03, 2),
        "is_weekend": round(is_weekend * 0.20, 2),
        "crowd_count": round(crowd_count * 0.05, 2),
    }


def recommend(state=None, city=None, latitude=None, longitude=None, hour=19, day_of_week=5, is_weekend=1):
    df = load_data()

    if state:
        df = df[df["state"].str.lower() == state.lower()]
    if city:
        df = df[df["city"].str.lower() == city.lower()]

    if df.empty:
        return []

    if latitude is None or longitude is None:
        latitude = float(df.iloc[0]["latitude"])
        longitude = float(df.iloc[0]["longitude"])

    results = []
    for _, row in df.iterrows():
        restaurant_id = int(row["id"])
        live = get_restaurant_analysis(restaurant_id)

        # fallback to CSV crowd when no analyzed video has been attached yet
        crowd_count = int(row["crowd_count"])
        waiting_time = calc_waiting_time(crowd_count)
        occupied_tables = None
        free_tables = None
        activity_score = None
        analysis_source = "default_dataset"

        if live:
            crowd_count = int(round(live.get("avg_people_count", crowd_count)))
            waiting_time = int(round(live.get("estimated_waiting_time_minutes", waiting_time)))
            occupied_tables = live.get("avg_occupied_tables")
            free_tables = live.get("avg_free_tables")
            activity_score = live.get("overall_dining_activity_score")
            analysis_source = "cv_video_analysis"

        distance = geodesic((latitude, longitude), (row["latitude"], row["longitude"])).km
        smart_score = round((0.55 * waiting_time) + (0.30 * distance) - (0.15 * float(row["rating"] * 10)), 2)

        results.append({
            "id": restaurant_id,
            "name": row["name"],
            "state": row["state"],
            "city": row["city"],
            "cuisine": row["cuisine"],
            "rating": float(row["rating"]),
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),
            "crowd_count": int(crowd_count),
            "waiting_time": int(waiting_time),
            "distance_km": round(distance, 2),
            "smart_score": smart_score,
            "feature_impact": feature_impact(hour, day_of_week, is_weekend, int(crowd_count)),
            "occupied_tables": occupied_tables,
            "free_tables": free_tables,
            "activity_score": activity_score,
            "analysis_source": analysis_source,
        })

    return sorted(results, key=lambda x: x["smart_score"])[:10]"""
"""from pathlib import Path
import pandas as pd
from geopy.distance import geodesic
from app.services.live_analysis import load_live_analysis

DATA = Path(__file__).resolve().parents[2] / "data" / "restaurants.csv"

CITY_COORDS = {
    "Mumbai": (19.0760, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Kolkata": (22.5726, 88.3639),
    "New Delhi": (28.6139, 77.2090),
}

def load_data():
    return pd.read_csv(DATA)

def calc_waiting_time(crowd_count: int) -> int:
    return max(5, int(crowd_count * 2.2))

def feature_impact(hour, day_of_week, is_weekend, crowd_count):
    return {
        "hour": round(hour * 0.02, 2),
        "day_of_week": round(day_of_week * 0.03, 2),
        "is_weekend": round(is_weekend * 0.20, 2),
        "crowd_count": round(crowd_count * 0.05, 2),
    }

def recommend(state=None, city=None, latitude=None, longitude=None, hour=19, day_of_week=5, is_weekend=1):
    df = load_data()
    live = load_live_analysis()

    if state:
        df = df[df["state"].str.lower() == state.lower()]
    if city:
        df = df[df["city"].str.lower() == city.lower()]

    if df.empty:
        return []

    if latitude is None or longitude is None:
        if city in CITY_COORDS:
            latitude, longitude = CITY_COORDS[city]
        else:
            latitude = float(df.iloc[0]["latitude"])
            longitude = float(df.iloc[0]["longitude"])

    results = []
    for _, row in df.iterrows():
        rid = str(int(row["id"]))
        distance = geodesic((latitude, longitude), (row["latitude"], row["longitude"])).km

        if rid in live:
            crowd_count = int(round(live[rid].get("avg_people_count", row["crowd_count"])))
            waiting_time = int(live[rid].get("estimated_waiting_time_minutes", calc_waiting_time(crowd_count)))
            occupied = live[rid].get("avg_occupied_tables", 0)
            free_tables = live[rid].get("avg_free_tables", 0)
            source = "cv"
        else:
            crowd_count = int(row["crowd_count"])
            waiting_time = calc_waiting_time(crowd_count)
            occupied = None
            free_tables = None
            source = "default"

        smart_score = round((0.55 * waiting_time) + (0.30 * distance) - (0.15 * float(row["rating"] * 10)), 2)

        results.append({
            "id": int(row["id"]),
            "name": row["name"],
            "state": row["state"],
            "city": row["city"],
            "cuisine": row["cuisine"],
            "rating": float(row["rating"]),
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),
            "crowd_count": int(crowd_count),
            "waiting_time": int(waiting_time),
            "distance_km": round(distance, 2),
            "smart_score": smart_score,
            "feature_impact": feature_impact(hour, day_of_week, is_weekend, int(crowd_count)),
            "data_source": source,
            "occupied_tables": occupied,
            "free_tables": free_tables,
        })

    return sorted(results, key=lambda x: x["smart_score"])[:10]"""
"""from pathlib import Path
from math import radians, sin, cos, sqrt, atan2
import pandas as pd
import requests

from app.services.live_analysis import load_live_analysis

DATA = Path(__file__).resolve().parents[2] / "data" / "restaurants.csv"

# State -> City -> Area coordinates
LOCATION_MAP = {
    "Delhi": {
        "New Delhi": {
            "Rohini": {"lat": 28.7041, "lng": 77.1025},
            "Connaught Place": {"lat": 28.6304, "lng": 77.2177},
            "Dwarka": {"lat": 28.5823, "lng": 77.0500},
            "Vasant Kunj": {"lat": 28.5293, "lng": 77.1532},
        }
    },
    "Maharashtra": {
        "Mumbai": {
            "Andheri": {"lat": 19.1136, "lng": 72.8697},
            "Bandra": {"lat": 19.0596, "lng": 72.8295},
            "Juhu": {"lat": 19.1075, "lng": 72.8263},
            "Powai": {"lat": 19.1197, "lng": 72.9051},
        },
        "Pune": {
            "Kothrud": {"lat": 18.5074, "lng": 73.8077},
            "Koregaon Park": {"lat": 18.5362, "lng": 73.8939},
            "Hinjewadi": {"lat": 18.5913, "lng": 73.7389},
            "Viman Nagar": {"lat": 18.5665, "lng": 73.9122},
        },
    },
    "Karnataka": {
        "Bangalore": {
            "Indiranagar": {"lat": 12.9784, "lng": 77.6408},
            "Koramangala": {"lat": 12.9279, "lng": 77.6271},
            "Whitefield": {"lat": 12.9698, "lng": 77.7499},
            "Jayanagar": {"lat": 12.9299, "lng": 77.5824},
        }
    },
    "TamilNadu": {
        "Chennai": {
            "T Nagar": {"lat": 13.0418, "lng": 80.2341},
            "Adyar": {"lat": 13.0012, "lng": 80.2565},
            "Velachery": {"lat": 12.9716, "lng": 80.2212},
            "Anna Nagar": {"lat": 13.0850, "lng": 80.2101},
        }
    },
    "Telangana": {
        "Hyderabad": {
            "Banjara Hills": {"lat": 17.4156, "lng": 78.4347},
            "Jubilee Hills": {"lat": 17.4326, "lng": 78.4071},
            "Hitech City": {"lat": 17.4435, "lng": 78.3772},
            "Gachibowli": {"lat": 17.4401, "lng": 78.3489},
        }
    },
}


def load_data():
    return pd.read_csv(DATA)


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    a = min(1.0, max(0.0, a))
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def feature_impact(hour, day_of_week, is_weekend, crowd_count):
    return {
        "hour": round(hour * 0.02, 2),
        "day_of_week": round(day_of_week * 0.03, 2),
        "is_weekend": round(is_weekend * 0.20, 2),
        "crowd_count": round(crowd_count * 0.05, 2),
    }


def get_reference_location(state=None, city=None, area=None, latitude=None, longitude=None):
    if latitude is not None and longitude is not None:
        return latitude, longitude

    if state and city and area:
        try:
            loc = LOCATION_MAP[state][city][area]
            return loc["lat"], loc["lng"]
        except KeyError:
            return None, None

    return None, None


def fetch_overpass_restaurants(ref_lat, ref_lng, radius_km):
    overpass_url = "https://overpass-api.de/api/interpreter"
    radius_m = int(min(radius_km * 1000, 20000))

    query = f
    [out:json];
    node["amenity"="restaurant"](around:{radius_m},{ref_lat},{ref_lng});
    out 30;
    

    try:
        response = requests.get(
            overpass_url,
            params={"data": query},
            headers={"User-Agent": "SmartDineAI-Pro/1.0"},
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        items = []
        for node in data.get("elements", []):
            tags = node.get("tags", {})
            name = tags.get("name")
            if not name:
                continue

            lat = float(node["lat"])
            lng = float(node["lon"])
            dist = calculate_distance(ref_lat, ref_lng, lat, lng)
            if dist > radius_km:
                continue

            cuisine = tags.get("cuisine", "Multi Cuisine").replace("_", " ").title()
            rating = round(3.8 + ((node["id"] % 10) / 10), 1)

            # Default estimated values for real restaurants
            crowd_count = 10 + (node["id"] % 10)
            waiting_time = max(5, 8 + int(crowd_count * 1.3) + int(dist))

            items.append({
                "id": int(node["id"]),
                "name": name,
                "state": state_from_coords_fallback(ref_lat, ref_lng),
                "city": city_from_coords_fallback(ref_lat, ref_lng),
                "cuisine": cuisine,
                "rating": rating,
                "latitude": lat,
                "longitude": lng,
                "crowd_count": crowd_count,
                "waiting_time": waiting_time,
                "distance_km": round(dist, 2),
                "occupied_tables": None,
                "free_tables": None,
                "data_source": "real",
            })

        return items
    except Exception:
        return []


def state_from_coords_fallback(lat, lng):
    # lightweight fallback label for UI when real reverse geocode is not stored
    return "Detected Area"


def city_from_coords_fallback(lat, lng):
    return "Nearby"


def recommend(
    state=None,
    city=None,
    area=None,
    latitude=None,
    longitude=None,
    group_size=2,
    radius_km=5.0,
    hour=19,
    day_of_week=5,
    is_weekend=1,
):
    ref_lat, ref_lng = get_reference_location(
        state=state,
        city=city,
        area=area,
        latitude=latitude,
        longitude=longitude,
    )

    if ref_lat is None or ref_lng is None:
        return []

    live = load_live_analysis()
    df = load_data()

    results = []
    seen_names = set()

    # 1) Real nearby restaurants from Overpass
    real_items = fetch_overpass_restaurants(ref_lat, ref_lng, radius_km)

    for item in real_items:
        # if by chance admin has analyzed a same-name restaurant, use CV values
        matched_live = None
        for _, row in df.iterrows():
            rid = str(int(row["id"]))
            if row["name"].strip().lower() == item["name"].strip().lower() and rid in live:
                matched_live = live[rid]
                break

        if matched_live:
            item["crowd_count"] = int(round(matched_live.get("avg_people_count", item["crowd_count"])))
            item["waiting_time"] = int(matched_live.get("estimated_waiting_time_minutes", item["waiting_time"]))
            item["occupied_tables"] = matched_live.get("avg_occupied_tables")
            item["free_tables"] = matched_live.get("avg_free_tables")
            item["data_source"] = "cv"

        item["smart_score"] = round((0.55 * item["waiting_time"]) + (0.30 * item["distance_km"]) - (0.15 * float(item["rating"] * 10)), 2)
        item["feature_impact"] = feature_impact(hour, day_of_week, is_weekend, int(item["crowd_count"]))

        seen_names.add(item["name"].strip().lower())
        results.append(item)

    # 2) Also include local/admin restaurants so CV-updated restaurants definitely appear
    for _, row in df.iterrows():
        rid = str(int(row["id"]))
        rlat = float(row["latitude"])
        rlng = float(row["longitude"])

        dist = calculate_distance(ref_lat, ref_lng, rlat, rlng)
        if dist > radius_km:
            continue

        name_key = row["name"].strip().lower()
        if name_key in seen_names:
            continue

        if rid in live:
            crowd_count = int(round(live[rid].get("avg_people_count", row["crowd_count"])))
            waiting_time = int(live[rid].get("estimated_waiting_time_minutes", max(5, int(crowd_count * 2.2))))
            occupied = live[rid].get("avg_occupied_tables")
            free_tables = live[rid].get("avg_free_tables")
            source = "cv"
        else:
            crowd_count = int(row["crowd_count"])
            waiting_time = max(5, int(crowd_count * 2.2) + int(group_size))
            occupied = None
            free_tables = None
            source = "default"

        results.append({
            "id": int(row["id"]),
            "name": row["name"],
            "state": row["state"],
            "city": row["city"],
            "cuisine": row["cuisine"],
            "rating": float(row["rating"]),
            "latitude": rlat,
            "longitude": rlng,
            "crowd_count": int(crowd_count),
            "waiting_time": int(waiting_time),
            "distance_km": round(dist, 2),
            "smart_score": round((0.55 * waiting_time) + (0.30 * dist) - (0.15 * float(row["rating"] * 10)), 2),
            "feature_impact": feature_impact(hour, day_of_week, is_weekend, int(crowd_count)),
            "data_source": source,
            "occupied_tables": occupied,
            "free_tables": free_tables,
        })

    return sorted(results, key=lambda x: x["smart_score"])[:20]"""
from pathlib import Path
from math import radians, sin, cos, sqrt, atan2
import pandas as pd
import requests

from app.services.live_analysis import load_live_analysis

DATA = Path(__file__).resolve().parents[2] / "data" / "restaurants.csv"

# State -> City -> Area coordinates
LOCATION_MAP = {
    "Delhi": {
        "New Delhi": {
            "Rohini": {"lat": 28.7041, "lng": 77.1025},
            "Connaught Place": {"lat": 28.6304, "lng": 77.2177},
            "Dwarka": {"lat": 28.5823, "lng": 77.0500},
            "Vasant Kunj": {"lat": 28.5293, "lng": 77.1532},
        }
    },
    "Maharashtra": {
        "Mumbai": {
            "Andheri": {"lat": 19.1136, "lng": 72.8697},
            "Bandra": {"lat": 19.0596, "lng": 72.8295},
            "Juhu": {"lat": 19.1075, "lng": 72.8263},
            "Powai": {"lat": 19.1197, "lng": 72.9051},
        },
        "Pune": {
            "Kothrud": {"lat": 18.5074, "lng": 73.8077},
            "Koregaon Park": {"lat": 18.5362, "lng": 73.8939},
            "Hinjewadi": {"lat": 18.5913, "lng": 73.7389},
            "Viman Nagar": {"lat": 18.5665, "lng": 73.9122},
        },
    },
    "Karnataka": {
        "Bangalore": {
            "Indiranagar": {"lat": 12.9784, "lng": 77.6408},
            "Koramangala": {"lat": 12.9279, "lng": 77.6271},
            "Whitefield": {"lat": 12.9698, "lng": 77.7499},
            "Jayanagar": {"lat": 12.9299, "lng": 77.5824},
        }
    },
    "TamilNadu": {
        "Chennai": {
            "T Nagar": {"lat": 13.0418, "lng": 80.2341},
            "Adyar": {"lat": 13.0012, "lng": 80.2565},
            "Velachery": {"lat": 12.9716, "lng": 80.2212},
            "Anna Nagar": {"lat": 13.0850, "lng": 80.2101},
        }
    },
    "Telangana": {
        "Hyderabad": {
            "Banjara Hills": {"lat": 17.4156, "lng": 78.4347},
            "Jubilee Hills": {"lat": 17.4326, "lng": 78.4071},
            "Hitech City": {"lat": 17.4435, "lng": 78.3772},
            "Gachibowli": {"lat": 17.4401, "lng": 78.3489},
        }
    },
}


def load_data():
    return pd.read_csv(DATA)


def calculate_distance(lat1, lon1, lat2, lon2):
    r = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    a = min(1.0, max(0.0, a))
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return r * c


def feature_impact(hour, day_of_week, is_weekend, crowd_count):
    return {
        "hour": round(hour * 0.02, 2),
        "day_of_week": round(day_of_week * 0.03, 2),
        "is_weekend": round(is_weekend * 0.20, 2),
        "crowd_count": round(crowd_count * 0.05, 2),
    }


def get_reference_location(state=None, city=None, area=None, latitude=None, longitude=None):
    # Use GPS coordinates only if valid and non-zero
    if latitude not in (None, 0, 0.0) and longitude not in (None, 0, 0.0):
        return latitude, longitude

    # Otherwise use manual selection mapping
    if state and city and area:
        try:
            loc = LOCATION_MAP[state][city][area]
            return loc["lat"], loc["lng"]
        except KeyError:
            return None, None

    return None, None


def fetch_overpass_restaurants(ref_lat, ref_lng, radius_km):
    overpass_url = "https://overpass-api.de/api/interpreter"
    radius_m = int(min(radius_km * 1000, 20000))

    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="restaurant"](around:{radius_m},{ref_lat},{ref_lng});
      way["amenity"="restaurant"](around:{radius_m},{ref_lat},{ref_lng});
      relation["amenity"="restaurant"](around:{radius_m},{ref_lat},{ref_lng});
    );
    out center tags;
    """

    try:
        response = requests.get(
            overpass_url,
            params={"data": query},
            headers={"User-Agent": "SmartDineAI-Pro/1.0"},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        items = []
        seen = set()

        for element in data.get("elements", []):
            tags = element.get("tags", {})
            name = tags.get("name")
            if not name:
                continue

            # nodes have lat/lon directly; ways/relations use center
            if "lat" in element and "lon" in element:
                lat = float(element["lat"])
                lng = float(element["lon"])
            elif "center" in element:
                lat = float(element["center"]["lat"])
                lng = float(element["center"]["lon"])
            else:
                continue

            dist = calculate_distance(ref_lat, ref_lng, lat, lng)
            if dist > radius_km:
                continue

            key = (name.strip().lower(), round(lat, 4), round(lng, 4))
            if key in seen:
                continue
            seen.add(key)

            cuisine = tags.get("cuisine", "Multi Cuisine").replace("_", " ").title()
            rating = round(3.8 + ((int(element["id"]) % 10) / 10), 1)

            crowd_count = 10 + (int(element["id"]) % 10)
            waiting_time = max(5, 8 + int(crowd_count * 1.3) + int(dist))

            items.append({
                "id": int(element["id"]),
                "name": name,
                "state": "Detected Area",
                "city": "Nearby",
                "cuisine": cuisine,
                "rating": rating,
                "latitude": lat,
                "longitude": lng,
                "crowd_count": crowd_count,
                "waiting_time": waiting_time,
                "distance_km": round(dist, 2),
                "occupied_tables": None,
                "free_tables": None,
                "data_source": "real",
            })

        return items

    except Exception as e:
        print("Overpass fetch error:", str(e))
        return []


def recommend(
    state=None,
    city=None,
    area=None,
    latitude=None,
    longitude=None,
    group_size=2,
    radius_km=5.0,
    hour=19,
    day_of_week=5,
    is_weekend=1,
):
    print("Recommend called with:", state, city, area, latitude, longitude, group_size, radius_km)

    ref_lat, ref_lng = get_reference_location(
        state=state,
        city=city,
        area=area,
        latitude=latitude,
        longitude=longitude,
    )

    if ref_lat is None or ref_lng is None:
        print("No valid reference location found")
        return []

    live = load_live_analysis()
    df = load_data()

    results = []
    seen_names = set()

    # 1) Real nearby restaurants from Overpass / OSM
    real_items = fetch_overpass_restaurants(ref_lat, ref_lng, radius_km)

    if not real_items:
        print("No real nearby restaurants found from Overpass, using local dataset fallback")

    for item in real_items:
        matched_live = None

        # match with local CSV restaurants by exact name
        for _, row in df.iterrows():
            rid = str(int(row["id"]))
            if row["name"].strip().lower() == item["name"].strip().lower() and rid in live:
                matched_live = live[rid]
                break

        if matched_live:
            item["crowd_count"] = int(round(matched_live.get("avg_people_count", item["crowd_count"])))
            item["waiting_time"] = int(matched_live.get("estimated_waiting_time_minutes", item["waiting_time"]))
            item["occupied_tables"] = matched_live.get("avg_occupied_tables")
            item["free_tables"] = matched_live.get("avg_free_tables")
            item["data_source"] = "cv"

        item["smart_score"] = round(
            (0.55 * item["waiting_time"]) + (0.30 * item["distance_km"]) - (0.15 * float(item["rating"] * 10)),
            2,
        )
        item["feature_impact"] = feature_impact(hour, day_of_week, is_weekend, int(item["crowd_count"]))

        seen_names.add(item["name"].strip().lower())
        results.append(item)

    # 2) Include local CSV restaurants also, so CV-updated / default managed restaurants appear too
    for _, row in df.iterrows():
        rid = str(int(row["id"]))
        rlat = float(row["latitude"])
        rlng = float(row["longitude"])

        dist = calculate_distance(ref_lat, ref_lng, rlat, rlng)
        if dist > radius_km:
            continue

        name_key = row["name"].strip().lower()
        if name_key in seen_names:
            continue

        if rid in live:
            crowd_count = int(round(live[rid].get("avg_people_count", row["crowd_count"])))
            waiting_time = int(
                live[rid].get(
                    "estimated_waiting_time_minutes",
                    max(5, int(crowd_count * 2.2)),
                )
            )
            occupied = live[rid].get("avg_occupied_tables")
            free_tables = live[rid].get("avg_free_tables")
            source = "cv"
        else:
            crowd_count = int(row["crowd_count"])
            waiting_time = max(5, int(crowd_count * 2.2) + int(group_size))
            occupied = None
            free_tables = None
            source = "default"

        results.append({
            "id": int(row["id"]),
            "name": row["name"],
            "state": row["state"],
            "city": row["city"],
            "cuisine": row["cuisine"],
            "rating": float(row["rating"]),
            "latitude": rlat,
            "longitude": rlng,
            "crowd_count": int(crowd_count),
            "waiting_time": int(waiting_time),
            "distance_km": round(dist, 2),
            "smart_score": round(
                (0.55 * waiting_time) + (0.30 * dist) - (0.15 * float(row["rating"] * 10)),
                2,
            ),
            "feature_impact": feature_impact(hour, day_of_week, is_weekend, int(crowd_count)),
            "data_source": source,
            "occupied_tables": occupied,
            "free_tables": free_tables,
        })

    return sorted(results, key=lambda x: x["smart_score"])[:20]
