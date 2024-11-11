from sqlmodel import Field, Session, SQLModel, create_engine, select
import uuid
from datetime import datetime

class Newsletter(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4(), primary_key=True, unique=True)
    user: uuid.UUID = Field(foreign_key='fiefuser.id')
    name: str | None = Field(default='')
    created_at: datetime = Field(default_factory=datetime.now())
    updated_at: datetime = Field(default_factory=None)
