from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>' this is how we connect to the database
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:OhYeah123@localhost/fastapi'

#we create an engine to establish the connection to the SQL database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#we need a session to talk to the database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#create a dependency -- > this might the generator concept that we just learned yesterday
# the idea is for every request/query on our database, we create a corresponding session, then it will be closed automatically when we are done.
# because we will write a lot of queries, it makes sense to create the below function so we can call it every time. Hence, the "generator"
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()