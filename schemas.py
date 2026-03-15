from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class RecommendationRequest(BaseModel):
    state: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    hour: Optional[int] = 19
    day_of_week: Optional[int] = 5
    is_weekend: Optional[int] = 1

class BookingRequest(BaseModel):
    user_email: str
    restaurant_id: int
    guests: int
    slot: str

class RestaurantOut(BaseModel):
    id: int
    name: str
    state: str
    city: str
    cuisine: str
    rating: float
    latitude: float
    longitude: float
    crowd_count: int
    waiting_time: int
    distance_km: float
    smart_score: float
    feature_impact: Dict[str, float]

class StatsOut(BaseModel):
    total_restaurants: int
    total_bookings: int
    avg_waiting_time: float
    avg_crowd_count: float
    city_distribution: Dict[str, int]
