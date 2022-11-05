from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass 


# this is the response Post, it inherits the other 3 from class PostBase
class Post(PostBase):
    id: int
    created_at: datetime
# when we query the databse, the ORM - SQLAlchemy actually creates an SQL Alchemy object to send back to the user
# it is not a dictionary. That's why if we add a formal response parameter to our FastAPI decorator, it won't understand this subject as it is not a dict
# the below code will allow FastAPI to ignore this fact and treat it as a dictionary
# it is within the Post class.
    class Config:
        orm_mode = True

#EmailStr library will do the validation
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# this is what we will send back to user after they send us their information
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True