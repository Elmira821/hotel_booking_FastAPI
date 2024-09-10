from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_rating
from schemas import RatingBase, UserAuth
from authen.authen_key import get_current_user



router = APIRouter(
    prefix='/hotel_ratings',
    tags=['hotel_ratings']
)

@router.get('')
def ratings(hotel_id: int, db: Session = Depends(get_db)):
    return db_rating.get_all(db, hotel_id)

@router.post('')
def create(request:RatingBase , db:Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
    rating = request.rating
    if rating < 0 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between(including) 0 and 5")
    return db_rating.create(db, request)

@router.put('/{id}')
def update_rating(id: int, request: RatingBase, db:Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
     return db_rating.update_rating(db, id, current_user.id, request)

@router.delete('/{id}')
def delete_rating(id: int, db:Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
     return db_rating.delete_rating(db, id, current_user.id)