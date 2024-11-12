from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

def generate_uuid():
    return str(uuid.uuid4())

class Post(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=generate_uuid, primary_key=True, unique=True)
    subtitle: str = Field(default=None, max_length=80)
    published: bool = Field(default=False)
    newsletter: uuid.UUID = Field(foreign_key='newsletter.id')
    body: str
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=None)
