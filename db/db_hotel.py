from sqlalchemy.orm.session import Session
from db.models import Db_Hotel, Db_Booking
from schemas import Hotel_Base
from fastapi import Response
from datetime import date

# search with hotel_name and location
def get_all_hotels(db: Session, hotel_name: str , location: str, min_price: int, max_price: int):
    hotel = db.query(Db_Hotel)
    
    if hotel_name:
        hotel = hotel.filter(Db_Hotel.hotel_name == hotel_name)

    if location:
        hotel = hotel.filter(Db_Hotel.location == location)

    if min_price !=0:
        hotel = db.query(Db_Hotel).filter(Db_Hotel.price >= min_price)

    if max_price !=999999:
        hotel = db.query(Db_Hotel).filter(Db_Hotel.price <= max_price)

    return hotel.all()

# search specific hotel/room by ID
def get_hotel(db: Session, id: int):
    hotel = db.query(Db_Hotel).filter(Db_Hotel.id == id).first()
    # handle errors
    return hotel

### Create function
def create_hotel(db: Session, request: Hotel_Base):
    new_hotel = Db_Hotel(
        hotel_name = request.hotel_name,
        location = request.location,
        room_number = request.room_number,
        bed_size = request.bed_size,
        price =  request.price,
        available = request.available,
        description = request.description,
        image_url = request.image_url,
        image_url_type = request.image_url_type,
    )
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel


### Update function
def update_hotel(db: Session, id: int, request: Hotel_Base):
    hotel= db.query(Db_Hotel).filter(Db_Hotel.id == id).first()
    if hotel:
        hotel.hotel_name = request.hotel_name
        hotel.location  = request.location
        hotel.room_number =request.room_number   
        hotel.price = request.price
        hotel.bed_size = request.bed_size
        hotel.available = request.available
        hotel.description = request.description
#       hotel.available_dates = ",".join(str(x) for x in request.available_dates)
        hotel.image_url = request.image_url
        hotel.image_url_type = request.image_url_type
        
    db.commit()
    db.refresh(hotel)
    return hotel

### Delete function
# delete a hotel
def delete_hotel(db: Session, id: int):
    hotel_name = db.query(Db_Hotel).filter(Db_Hotel.id == id).first()
    db.delete(hotel_name)
    db.commit()
    return Response(status_code=204)