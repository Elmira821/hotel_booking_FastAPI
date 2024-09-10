from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
from datetime import datetime
from db.models  import DbHotelRating
from schemas import RatingBase



def create(db: Session, request: RatingBase):
    new_rating = DbHotelRating(
        rating = request.rating,
        user_id = request.user_id,
        hotel_id = request.hotel_id,
        timestamp = datetime.now()
    )
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating


def get_all(db:Session, hotel_id: int):
    return db.query(DbHotelRating).filter(DbHotelRating.hotel_id == hotel_id).all()

def update_rating(db: Session, id: int, user_id: int, request: RatingBase):
    rating = db.query(DbHotelRating).filter(DbHotelRating.id == id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    elif rating.user_id != user_id:
        raise HTTPException(status_code=403, detail="Only rating creator can update it")
    else:    
        rating.hotel_id = request.hotel_id
        rating.rating = request.rating
        db.commit()
        db.refresh(rating)
        return rating

def delete_rating(db: Session, id: int, user_id: int):
    rating = db.query(DbHotelRating).filter(DbHotelRating.id == id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    elif rating.user_id != user_id:
        raise HTTPException(status_code=403, detail="Only rating creator can delete it")
    else:
        db.delete(rating)
        db.commit()
        return Response(status_code=204)