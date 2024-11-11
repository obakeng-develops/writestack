from fastapi import FastAPI

from sqlmodel import SQLModel, create_engine
from models.newsletter import Newsletter
from models.user import User
from models.comment import Comment
from models.post import Post
from models.subscription import Subscription
from dotenv import load_dotenv
import os

load_dotenv()

postgres_url = os.getenv("POSTGRES_URL")
engine = create_engine(postgres_url)

def create_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/")
def index():
    return {
        "message": "Hello World"
    }
