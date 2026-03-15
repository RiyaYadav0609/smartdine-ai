from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
from app.routes.auth import router as auth_router
from app.routes.recommend import router as recommend_router
from app.routes.bookings import router as bookings_router
from app.routes.admin import router as admin_router
from app.routes.video import router as video_router
from app.services.seed import seed_restaurants

app = FastAPI(title="SmartDine AI Pro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
db = SessionLocal()
seed_restaurants(db)
db.close()

app.include_router(auth_router)
app.include_router(recommend_router)
app.include_router(bookings_router)
app.include_router(admin_router)
app.include_router(video_router)

@app.get("/")
def root():
    return {"message": "SmartDine AI Pro backend is running"}
