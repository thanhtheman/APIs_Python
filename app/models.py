from cgitb import text
from sqlite3 import Timestamp
from time import timezone
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

#class extended Base
class Post(Base):
    __tablename__ = "posts2"

# just like we create a table in SQL, we use a Column class in sqlalchemy to create a Column object
# It's the same logic, type of data, is it a primary key, is it possible to be null?
    id = Column(Integer, primary_key = True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

#Let's create a table to store user data

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable=False)
    email = Column(String, nullable = False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))