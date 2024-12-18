from sqlmodel import SQLModel, Field, Index
import uuid
from datetime import datetime
from helpers.generate_uuid import generate_uuid

class PostBase(SQLModel):
    subtitle: str = Field(default=None, max_length=200)
    published: bool = Field(default=False)
    newsletter: uuid.UUID = Field(foreign_key='newsletter.id')
    body: str

class Post(PostBase, table=True):
    id: uuid.UUID = Field(default_factory=generate_uuid, primary_key=True, unique=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    
    __table_args__ = (
        Index('ix_newsletter_id', 'newsletter'),
    )

class PostCreate(PostBase):
    pass

class PostPublic(PostBase):
    id: uuid.UUID
    
class PostUpdate(SQLModel):
    subtitle: str
    published: bool
    newsletter: uuid.UUID
    body: str
