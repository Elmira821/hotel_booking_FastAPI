from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from authen.authen_key import get_current_user
from db.database import get_db
from db import db_review
from schemas import ReviewBase, UserBase, UserAuth


router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)

@router.get('')
def reviews(hotel_id: int, db: Session = Depends(get_db)):
    return db_review.get_all(db, hotel_id)

@router.post('')
def create(request: ReviewBase, db:Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
    return db_review.create(db, request)


@router.put('/{id}')
def update_review(id: int, request: ReviewBase, db:Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
     return db_review.update_review(db, id, current_user.id, request) 

@router.delete('/{id}')
def delete_review(id: int, db:Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
     return db_review.delete_review(db, id, current_user.id)