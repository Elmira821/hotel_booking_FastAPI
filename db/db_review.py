from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
from db.models import DbReview
from schemas import Review, ReviewBase    
from datetime import datetime

def create(db: Session, request:ReviewBase):
    new_review = DbReview(
        text = request.text,
        user_id = request.user_id,
        hotel_id = request.hotel_id,
        timestamp = datetime.now()
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

def get_all(db:Session, hotel_id: int):
    return db.query(DbReview).filter(DbReview.hotel_id == hotel_id).all()

def update_review(db: Session, id: int, user_id: int, request: Review):
    review = db.query(DbReview).filter(DbReview.id == id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    elif review.user_id != user_id:
        raise HTTPException(status_code=403, detail="Only review creator can update it")
    else:    
        review.text = request.text 
        db.commit()
        db.refresh(review)
        return review
    
def delete_review(db: Session, id: int, user_id: int):   
    review = db.query(DbReview).filter(DbReview.id == id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    elif review.user_id != user_id:
        raise HTTPException(status_code=403, detail="Only review creator can delete it")
    else:  
        db.delete(review)
        db.commit()
        return Response(status_code=204)