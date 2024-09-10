from sqlalchemy.orm import Session
from db.models import DbFlag
from schemas import FlagBase
from datetime import datetime

def create_flag(db: Session, request: FlagBase):
    new_flag = DbFlag(
        hotel_name = request.hotel_name,
        location = request.location,
        reason = request.reason,
        timestamp = datetime.now()
    )
    db.add(new_flag)
    db.commit()
    db.refresh(new_flag)
    return new_flag