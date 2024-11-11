from sqlmodel import Field, Session, SQLModel, create_engine, select
import uuid
from datetime import datetime

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4(), primary_key=True, unique=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=80)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=None)
