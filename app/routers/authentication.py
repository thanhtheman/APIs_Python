from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, oauth2, schema, utils

router = APIRouter(tags=["Authentication"])

@router.post('/sqlalchemy/login')
def log_in(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {'token': access_token, "token_type": "bearer"}