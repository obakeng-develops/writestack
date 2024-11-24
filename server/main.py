from fastapi import FastAPI

from sqlmodel import SQLModel
from models.comment import Comment
from models.post import Post
from models.subscription import Subscription
from dotenv import load_dotenv
from routers.v1 import newsletter, user, post, subscriptions, comment
from helpers.database import engine, create_tables
from prometheus_fastapi_instrumentator import Instrumentator
import os

load_dotenv()

app = FastAPI()

instrumentator = Instrumentator().instrument(app)

@app.on_event("startup")
def on_startup():
    create_tables()
    instrumentator.expose(app)

app.include_router(newsletter.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(subscriptions.router)
app.include_router(comment.router)
