from fastapi import FastAPI

from sqlmodel import Field, Session, SQLModel, create_engine, select

class Newsletter(SQLModel, table=True):
    id: int = Field(primary_key=True)

sqlite_file = "test.db"
sqlite_url = f"sqlite:///{sqlite_file}"
engine = create_engine(sqlite_url)

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
