from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schema, utils
from .. import oauth2
# . means the root directory
#.. means we need to go up 1 level

router = APIRouter(prefix="/sqlalchemy/posts", tags=['Post'])

#create the database
# models.Base.metadata.create_all(bind=engine)


#sqlalchemy routes
@router.get('/', response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.post('/create', response_model=schema.Post, status_code = status.HTTP_201_CREATED)
#the 'Post' below is the above class POST, not the Post from the models 
def create_post(post: schema.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}', response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    search_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not search_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="This post doesn't exist!")
    return search_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} doesn't exist")
    else:
        deleted_post.delete(synchronize_session = False)
        db.commit()
        Response(status_code=status.HTTP_204_NO_CONTENT)
        return {'result': f'Post {id} has been successfully deleted!'}

@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.PostUpdate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    target_post = post_query.first()
    if target_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} doesn't exist. Nothing is updated!")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post