from datetime import date
from db.models import Db_User
from schemas import UserBase
from sqlalchemy.orm.session import Session
from db.hashing import Hash
from fastapi import HTTPException, status, Response

def create_user(db: Session, request: UserBase):
    new_user = Db_User(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password),
        phone_number = request.phone_number,
        gender = request.gender,
        date_of_birth = request.date_of_birth,
        address = request.address
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    return db.query(Db_User).all()

def get_user(db: Session, id: int):
    user = db.query(Db_User).filter(Db_User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with {id} not found')
    return user

def get_user_by_username(db: Session, username: str):
    user = db.query(Db_User).filter(Db_User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with {username} not found')
    return user

def update_user(db: Session, id, request: UserBase):
    user = db.query(Db_User).filter(Db_User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {id} not found'
        )   
    user.username = request.username
    user.email = request.email
    user.password = Hash.bcrypt(request.password)
    user.phone_number = request.phone_number
    user.gender = request.gender
    user.date_of_birth = request.date_of_birth
    user.address = request.address
    
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, id: int):
    id = db.query(Db_User).filter(Db_User.id == id).first()
    if not id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with {id} not found')
    db.delete(id)
    db.commit()
    return Response(status_code=204)
