from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_guest_rating
from schemas import GuestRatingBase, UserBase
from calculate import calculate_guest_rating
from authen.authen_key import get_current_user

router = APIRouter(
    prefix='/guest_ratings',  
    tags=['guest_ratings']  
)

@router.get('')
def get_all_guest_ratings(user_id: int, db: Session = Depends(get_db)):
    guest_ratings = db_guest_rating.get_all(db, user_id)
    for rating in guest_ratings:
        if rating.guest_rating is not None:
            rating.guest_rating = calculate_guest_rating(rating.guest_rating)  
    return guest_ratings

@router.post('')
def create_guest_rating(request: GuestRatingBase, db: Session = Depends(get_db)):
    new_rating = db_guest_rating.create_feedback(db, request)
    if new_rating.guest_rating is not None:
        if new_rating.guest_rating < 1 or new_rating.guest_rating > 10:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 10")
        new_rating.guest_rating = calculate_guest_rating(new_rating.guest_rating)
    return new_rating



@router.put('/{id}')
def update_rating(id: int, request: GuestRatingBase, db:Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
     return db_guest_rating.update_guest_rating(db, id, request)

@router.delete('/{id}')    
def delete_rating(id: int, db:Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
     return db_guest_rating.delete_guest_rating(db, id)