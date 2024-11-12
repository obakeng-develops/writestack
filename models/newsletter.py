from sqlmodel import Field, Session, SQLModel, create_engine, select
import uuid
from datetime import datetime

def generate_uuid():
    return str(uuid.uuid4())

class Newsletter(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=generate_uuid, primary_key=True, unique=True)
    user: uuid.UUID = Field(foreign_key='user.id')
    name: str | None = Field(default='')
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=None)
