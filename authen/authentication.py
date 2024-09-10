from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import models
from db.db_user import get_user
from db.models import Db_User
from db.hashing import Hash
from authen import authen_key
from authen.authen_key import get_current_user
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from schemas import UserDisplay

router = APIRouter(
    tags=['authentication']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Db_User).filter(Db_User.username == request.username).first()
    if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    if not Hash.verify(user.password, request.password):
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
    
    access_token = authen_key.create_access_token(data={"username": user.username})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
}

@router.get('/{id}/role', response_model = str)
def get_role(id: int, db: Session = Depends(get_db), current_user: UserDisplay = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    else:
      user = get_user(db, id)
      if user.role != "admin":
        return f'user with id {id} is not admin'
      else:
        return 'user with id {id} is the ADMINistrator'



    