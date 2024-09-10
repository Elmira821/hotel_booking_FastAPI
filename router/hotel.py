from typing import List, Optional
from schemas import Hotel_Base, Hotel_Display, UserBase
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from db.database import get_db
from db import db_hotel, models
from datetime import date

from authen.authen_key import get_current_user
import datetime, shutil, string, random, os

router = APIRouter(
    prefix='/hotels',
    tags=['hotels']
)

image_url_types = ['absolute', 'relative']

### Search function
# show all hotels and all the rooms
@router.get('', response_model=List[Hotel_Display])
def get_all_hotels(
    db: Session = Depends(get_db),
    hotel_name: str = None,
    location: str = None,
    min_price: int = 0,
    max_price: int = 999999,
    
 ):
    return db_hotel.get_all_hotels(db, hotel_name, location, min_price, max_price)

# Search specific hotel information
# Search a specific hotel and its room by ID
@router.get('/{id}', response_model = Hotel_Display)
def get_hotel(id: int, db: Session = Depends(get_db)):
    return db_hotel.get_hotel(db, id)

### Create function
@router.post('')
def create_hotel(request: Hotel_Base, db: Session = Depends(get_db),current_user: UserBase = Depends(get_current_user)):
                 
    if not request.image_url_type in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail="Parameter image_url_type can only take values absolute or relative")
    return db_hotel.create_hotel(db, request)


### Update function
@router.put('/{id}')
def update_hotel(id: int, request: Hotel_Base, db: Session = Depends(get_db),current_user: UserBase = Depends(get_current_user)):
    return db_hotel.update_hotel(db, id, request)
#authentication

### Delete function
# delete a hotel by hotel_name
@router.delete('/{id}')
def delete_hotel(id: int, db: Session = Depends(get_db),current_user: UserBase = Depends(get_current_user)):
    return db_hotel.delete_hotel(db, id)

