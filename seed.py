"""from sqlalchemy.orm import Session
from app.models.db_models import Restaurant
from app.services.recommender import load_data

def seed_restaurants(db: Session):
    if db.query(Restaurant).count() > 0:
        return
    df = load_data()
    for _, row in df.iterrows():
        db.add(Restaurant(
            id=int(row["id"]),
            name=row["name"],
            state=row["state"],
            city=row["city"],
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            cuisine=row["cuisine"],
            rating=float(row["rating"]),
        ))
    db.commit()"""
from pathlib import Path
import pandas as pd
from sqlalchemy.orm import Session

from app.models.db_models import Restaurant

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "restaurants.csv"


def seed_restaurants(db: Session):
    existing = db.query(Restaurant).first()
    if existing:
        return

    if not DATA_PATH.exists():
        print(f"restaurants.csv not found at: {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)

    for _, row in df.iterrows():
        restaurant = Restaurant(
            id=int(row["id"]),
            name=str(row["name"]),
            state=str(row["state"]),
            city=str(row["city"]),
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            cuisine=str(row["cuisine"]),
            rating=float(row["rating"]),
            crowd_count=int(row["crowd_count"]) if not pd.isna(row["crowd_count"]) else 0,
            waiting_time=int(row["waiting_time"]) if not pd.isna(row["waiting_time"]) else 0,
        )
        db.add(restaurant)

    db.commit()
    print("Restaurants seeded successfully.")
