from sqlmodel import Field, SQLModel
import uuid
from datetime import datetime
from helpers.generate_uuid import generate_uuid

class NewsletterBase(SQLModel):
    user: uuid.UUID = Field(foreign_key='user.id')
    name: str | None = Field(default='')

class Newsletter(NewsletterBase, table=True):
    id: uuid.UUID = Field(default_factory=generate_uuid, primary_key=True, unique=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=None)

class NewsletterCreate(NewsletterBase):
    pass

class NewsletterPublic(NewsletterBase):
    id: uuid.UUID
    
class NewsletterUpdate(SQLModel):
    user: uuid.UUID
    name: str
