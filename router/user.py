from sqlalchemy.orm.session import Session
from schemas import UserBase, UserDisplay
from fastapi import APIRouter, Depends,HTTPException
from db.database import get_db
from db import db_user
from typing import List
from authen.authen_key import get_current_user



router = APIRouter(
  prefix='/users',
  tags=['users']
)

@router.get('', response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db), 
    current_user: UserDisplay = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return db_user.get_all_users(db)


@router.get('/{id}', response_model=UserBase)
def get_user(id: int, db: Session = Depends(get_db), 
    current_user: UserDisplay = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return db_user.get_user(db, id)

@router.post('', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# Update
@router.put('')
def update_user(request: UserBase, db: Session = Depends(get_db), 
    current_user: UserDisplay = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return db_user.update_user(db, current_user.id, request)


# Delete
@router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db), 
    current_user: UserDisplay = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return db_user.delete_user(db, id)