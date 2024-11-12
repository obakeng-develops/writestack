from fastapi import FastAPI

from sqlmodel import SQLModel
from models.comment import Comment
from models.post import Post
from models.subscription import Subscription
from dotenv import load_dotenv
from routers.v1 import newsletter, user
from database import engine, create_tables
import os

load_dotenv()

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables()

app.include_router(newsletter.router)
app.include_router(user.router)
