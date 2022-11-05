from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schema, utils 

router = APIRouter()

#user registration

@router.post("/sqlalchemy/register", status_code = status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    #hash the password before sending it to the database
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/sqlalchemy/users/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} doesn't exist.")
    return user

@router.get("/sqlalchemy/users", response_model=List[schema.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users
