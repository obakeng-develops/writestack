from sqlmodel import create_engine, Session, SQLModel
import os

postgres_url = os.getenv("POSTGRES_URL")
engine = create_engine(postgres_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
