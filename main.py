from fastapi import FastAPI
from . import models
from .database import engine
from app import schemas
from .routers import post,users 

models.Base.metadata.create_all(bind=engine)



app = FastAPI()
#first function has priority

app.include_router(post.router)
app.include_router(users.router)
    

