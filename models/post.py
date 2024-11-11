from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

class Post(SQLModel, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4(), primary_key=True, unique=True)
    subtitle: str = Field(default=None, max_length=80)
    published: bool = Field(default=False)
    newsletter: uuid.UUID = Field(foreign_key='newsletter.id')
    body: str
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=None)
