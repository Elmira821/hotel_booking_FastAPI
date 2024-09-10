from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime, Date
from db.database import Base
from sqlalchemy import Column, Enum, ARRAY

class Db_User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True, index =True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    phone_number = Column(String, default='')
    gender = Column(Enum('male', 'female','other'),default=None)
    date_of_birth = Column (Date,default=None)
    address = Column(String,default='') 
    role = Column(String, default='user') 
    items = relationship('Db_Hotel', back_populates='user')
    flags = relationship('DbFlag', back_populates='user')


class Db_Hotel(Base):
    __tablename__ = 'hotel'
    id = Column(Integer, primary_key =True, index =True)
    hotel_name = Column(String)
    location = Column(String)
    room_number = Column(String)
    bed_size = Column(String)
    price = Column(Integer)
    available = Column(Boolean)
    image_url = Column (String)
    image_url_type = Column (String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('Db_User', back_populates='items')
    reviews = relationship('DbReview',back_populates='hotel')
    ratings = relationship('DbHotelRating', back_populates='hotel')     
    guest_ratings = relationship('DbGuestRating', back_populates='hotel')
    #flags = relationship('Flag', back_populates='hotel') 
#   available_dates = Column(String)
    description = Column(String)
    
class DbReview(Base):          
    __tablename__='review'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    user_id = Column(Integer)   #changed from username
    timestamp = Column(DateTime)
    hotel_id = Column(Integer, ForeignKey('hotel.id'))
    hotel = relationship("Db_Hotel", back_populates="reviews")

class DbHotelRating(Base):
    __tablename__ = 'hotel_ratings'
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer) 
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime)
    hotel_id = Column(Integer, ForeignKey('hotel.id'))  
    hotel = relationship('Db_Hotel', back_populates='ratings')

class DbGuestRating(Base):
    __tablename__ ='guest_ratings'
    id = Column(Integer, primary_key=True, index=True)
    guest_rating = Column(Integer)
    user_id = Column(Integer,ForeignKey('user.id'))   #owner user id
    guest_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime)
    hotel_id = Column(Integer, ForeignKey('hotel.id')) 
    hotel = relationship('Db_Hotel', back_populates='guest_ratings')

class DbFlag(Base):
    __tablename__='flags'
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    hotel_name = Column(String)
    reason = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship("Db_User", back_populates="flags")
    #hotel = relationship("Db_Hotel", back_populates="flags")  

""" class Db_Image(Base):
    __tablename__ ='images'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    image_url_type = Column(String)
    hotel_id = Column(String)
    room_id = Column(String)
    creator_id = Column(String)
    timestamp = Column(DateTime) """

class Db_Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    guest_name = Column(String, index=True)
    guest_email = Column(String, index=True)
    checkin = Column(Date)
    checkout = Column(Date)
    is_confirmed = Column(Boolean, default=True)
    room_id = Column(Integer)

    # Define foreign key relationship with 'hotel' (room(id))
 #   room_id = Column(Integer, ForeignKey("hotel.id"))
 #   room = relationship("Db_Hotel", back_populates="bookings")

