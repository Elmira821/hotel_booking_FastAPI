from datetime import datetime
from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
from db.models import DbGuestRating
from schemas import GuestRatingBase

def create_feedback(db: Session, request:GuestRatingBase):
    new_guest_rating = DbGuestRating(
        guest_id=request.guest_id,
        user_id=request.user_id,
        guest_rating=request.guest_rating,  
        hotel_id=request.hotel_id,
        timestamp=datetime.now(),  
    )
    db.add(new_guest_rating)
    db.commit()
    db.refresh(new_guest_rating)
    return new_guest_rating

def get_all(db:Session, user_id: int):
    return db.query(DbGuestRating).filter(DbGuestRating.user_id == user_id).all()

def update_guest_rating(db: Session, id: int, request: GuestRatingBase):
    guest_rating = db.query(DbGuestRating).filter(DbGuestRating.id == id).first()
    if guest_rating:    
        guest_rating.hotel_id = request.hotel_id
        guest_rating.guest_rating = request.guest_rating
        guest_rating.user_id = request.user_id

        db.commit()
        db.refresh(guest_rating)
        return guest_rating


def delete_guest_rating(db: Session, id: int):
    id = db.query(DbGuestRating).filter(DbGuestRating.id == id).first()
    if id:
        db.delete(id)
        db.commit()
        return Response(status_code=204)