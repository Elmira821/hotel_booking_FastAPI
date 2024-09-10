from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_flag
from schemas import FlagBase, UserBase
from authen.authen_key import get_current_user

router = APIRouter(
    prefix='/flags',  
    tags=['flags']  
)

@router.post ('')
def flag_hotel(request: FlagBase, db: Session = Depends(get_db),current_user: UserBase = Depends(get_current_user)):
    new_flag = db_flag.create_flag(db, request)
    return new_flag