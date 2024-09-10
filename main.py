from fastapi import FastAPI, Response
from router import user, hotel, bookings, review, rating, guest_rating, flag
from db import models
from db.database import engine
from authen import authentication
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware 

booking_app= FastAPI()

booking_app.include_router(user.router)
booking_app.include_router(review.router)
booking_app.include_router(rating.router)
booking_app.include_router(guest_rating.router)
booking_app.include_router(flag.router)
booking_app.include_router(authentication.router)
booking_app.include_router(hotel.router)
booking_app.include_router(bookings.router)

@booking_app.get("/")
async def root():
    return {"message": "Hello, world!"}

@booking_app.get("/favicon.ico")
async def favicon():
    return Response (status_code=204)

@booking_app.get('/hello')
def index():
    return {'message': 'Welcome to EasyBook!'}

models.Base.metadata.create_all(engine)

booking_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for your React app's domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)