from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
# . means the root directory
from . import models, schema, utils
from .database import engine, get_db
from sqlalchemy.orm import Session



#create the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()



my_posts = [{'title': 'ML Engineering Playbook', 'content': 'How to become an Ml Engineeer', 'rating': 6, 'id': 1245}, 
{'title': 'Entrepreneur', 'content': 'How to launch your business', 'rating': 5, 'id': 1445},
{'title': 'Machine Learning', 'content': 'How to train genome', 'rating': 7, 'id': 1426}]

#At 3:55, we remove the below model to create a real postgre database
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     rating: Optional[int] = None
#     id: Optional[int]

# this is for Postgres, we moved this into a separate file schema.py at 5:33
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True


#realdictcursor is to make sure we have all the column names on our ouput. This is how we connect to our Postgres database
# try:
#     conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='OhYeah123', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print('Database Connected!')
# except Exception as error:
#     print('Connecting to Database Failed!')
#     print(error)





def find_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

#sqlalchemy routes
@app.get('/sqlalchemy', response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post('/sqlalchemy/post', response_model=schema.Post, status_code = status.HTTP_201_CREATED)
#the 'Post' below is the above class POST, not the Post from the models 
def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get('/sqlalchemy/posts/{id}', response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    search_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not search_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="This post doesn't exist!")
    return search_post

@app.delete("/sqlalchemy/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} doesn't exist")
    else:
        deleted_post.delete(synchronize_session = False)
        db.commit()
        Response(status_code=status.HTTP_204_NO_CONTENT)
        return {'result': f'Post {id} has been successfully deleted!'}

@app.put("/sqlalchemy/posts/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.PostUpdate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    target_post = post_query.first()
    if target_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} doesn't exist. Nothing is updated!")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post

#user registration

@app.post("/sqlalchemy/register", status_code = status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    #hash the password before sending it to the database
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/sqlalchemy/users/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} doesn't exist.")
    return user

@app.get("/sqlalchemy/users", response_model=List[schema.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users
