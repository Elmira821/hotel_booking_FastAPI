from fastapi import APIRouter, Depends, HTTPException
from schemas import UserBase, UserAuth, Booking_Base, Booking_Display
from sqlalchemy.orm import Session
from authen.authen_key import get_current_user
from db.database import get_db
from db import db_booking, models
from email_service import send_confirmation_email


router = APIRouter(
    prefix="/bookings",
    tags=["bookings"]
    )

# create a booking
@router.post("/")
def create_booking(request: Booking_Base, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    try:
        # Save the booking information to the database
        db_booking.create_booking(db, request)
    except HTTPException as e:
        if e.status_code == 400:
            raise HTTPException(status_code=400, detail= "Booking dates conflict with existing bookings.") 
        else:
            raise e
    else:
        # Send confirmation email to the customer
        send_confirmation_email(request.guest_email, request)
        return {"message": "Your booking is confirmed!"}

# delete a booking ticket by booking ID
@router.delete('/{id}')
def delete_booking(id: int, db: Session = Depends(get_db), 
    current_user: UserBase = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return db_booking.delete_booking(db, id)