from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime, date
from enum import Enum

# User
class GenderEnum(str, Enum):
    other = 'other'
    male = 'male'
    female = 'female'
    

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = ''
    gender: Optional[GenderEnum] = None
    date_of_birth: Optional[date] = None
    role: Optional[str] = 'user'
    address: Optional[str] = ''

class UserDisplay(BaseModel):
    username: str
    email: str
    role: str
    class Config:
        from_attributes = True

class UserAuth(BaseModel):
    id: int
    username: str
    email: str
    role: str

class UserUpdate(BaseModel):
    username: str = None
    email: str = None
    password: str = None
    class Config:
        from_attributes = True

class Hotel_Base(BaseModel):
    hotel_name: str
    location: str
    room_number: str
    bed_size: str
    price: int
    available: bool
    description:  Optional[str]
    available_dates : List[str]
    image_url: str
    image_url_type:str
    

class Review(BaseModel):    
    text: str
    user_id: int
    timestamp: datetime 
    class Config:
        from_attributes = True

class Rating(BaseModel):
    rating: int
    user_id: int
    hotel_id: int
    timestamp: datetime 
    class Config:
        from_attributes = True

class GuestRating(BaseModel):        #owner rating the guest
    user_id: int
    guest_id: int
    rating: int
    hotel_id: int
    timestamp: datetime 
    class Config:
        from_attributes = True

class FlagBase(BaseModel):
    hotel_name: str
    location: str
    user_id: int
    reason: str
    timestamp: datetime 
   
class FlagDisplay(BaseModel):
    hotel_name: str
    location: str
    user_id: int
    reason: str
    timestamp: datetime 
    class Config:
        from_attributes = True

class Hotel_Display(BaseModel):
    id: int
    hotel_name: str
    location: str
    room_number: str
    bed_size: str
    price: int
    available : Optional[bool]
    image_url: str
    image_url_type:str
    description : str
#   user: User 
    reviews: List[Review]   
    ratings: List[Rating]
    guest_ratings: List[GuestRating]    #owner rating the guest
    class Config:
        from_attributes = True


# class ImageBase(BaseModel):
#    image_url: str
#    image_url_type: str
#    caption: str
#    hotel_id: int
#    room_id: str
#    creator_id: int

#class ImageDisplay(BaseModel):
#    id: int
#    image_url: str
#    image_url_type: str
#    caption: str
#    hotel_id: str
#    room_id: str
#    creator_id: str
#    timestamp: datetime
#    class Config():
#        from_attributes = True

class Booking_Base(BaseModel):
    guest_name: str = Field(..., title="Guest Name", max_length=100)
    guest_email: EmailStr = Field(..., title="Guest Email")
    check_in_date: date = Field(..., title="Check-in Date")
    check_out_date: date = Field(..., title="Check-out Date")
    is_confirmed: Optional[bool] = Field(True, title="Booking Confirmation")
    room_id: int    

class Booking_Display(BaseModel):
    guest_name: str = Field(..., title="Guest Name", max_length=100)
    guest_email: EmailStr = Field(..., title="Guest Email")
    check_in_date: date = Field(..., title="Check-in Date")
    check_out_date: date = Field(..., title="Check-out Date")
    is_confirmed: Optional[bool] = Field(False, title="Booking Confirmation")

class ReviewBase(BaseModel):   
    user_id: int
    text: str
    hotel_id: int
    #image url
    
class RatingBase(BaseModel):
    user_id: int
    #guest_id: int
    rating: int
    hotel_id: int

class GuestRatingBase(BaseModel):        #owner rating the guest
    user_id: int
    guest_id:int 
    #feedback: str
    guest_rating: int
    hotel_id: int



