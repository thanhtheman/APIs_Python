
from fastapi import FastAPI
from .routers import post, user, authentication



#create the database at the beginning
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)

