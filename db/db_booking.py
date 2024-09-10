from sqlalchemy.orm.session import Session
from datetime import date
from db.models import Db_Booking
from schemas import Booking_Base
from fastapi import Response, HTTPException
from sqlalchemy import and_, or_, func

def check_booking_conflict(db: Session, check_in_date: date, check_out_date: date, room_id: int):
    # 查询数据库中与新日期范围冲突的预订
    conflicting_booking = db.query(Db_Booking).filter(
        and_(
            or_(
                and_(
                    Db_Booking.checkin < check_out_date,
                    Db_Booking.checkout >= check_out_date
                 ),
                 and_(
                     Db_Booking.checkin <= check_in_date,
                     Db_Booking.checkout > check_in_date
                 ),
                 and_(
                     Db_Booking.checkin >= check_in_date,
                     Db_Booking.checkout <= check_in_date
                 ),
                 check_in_date >= check_out_date
#                and_(
#                    func.DATE(Db_Booking.checkout) == checkin_date
#                )
            ),
            Db_Booking.room_id == room_id
        )
    ).first()
    return conflicting_booking

# create a booking
def create_booking(db: Session, request: Booking_Base):

    # check if there is date conflict
    conflicting_booking = check_booking_conflict(db, request.check_in_date, request.check_out_date, request.room_id)
    if conflicting_booking:

        raise HTTPException(status_code=400, detail="Booking dates conflict with existing bookings")
    
    # create new booking
    new_booking = Db_Booking(
        guest_name = request.guest_name,
        guest_email = request.guest_email,
        checkin = request.check_in_date,
        checkout = request.check_out_date,
        room_id = request.room_id
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

# search your Booking by ID
def get_booking(db: Session, id: int):
    booking = db.query(Db_Booking).filter(Db_Booking.id == id).first()
    # handle errors
    return booking

# delete a booking
def delete_booking(db: Session, id: int):
    booking = db.query(Db_Booking).filter(Db_Booking.id == id).first()
    db.delete(booking)
    db.commit()
    return Response(status_code=204)