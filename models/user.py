from sqlmodel import Field, Session, SQLModel, create_engine, select
import uuid
from datetime import datetime

def generate_uuid():
    return str(uuid.uuid4())

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=generate_uuid, primary_key=True, unique=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=80)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
