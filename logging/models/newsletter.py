from sqlmodel import Field, SQLModel, Index
import uuid
from datetime import datetime
from helpers.generate_uuid import generate_uuid
from typing import Optional

class NewsletterBase(SQLModel):
    user: uuid.UUID = Field(foreign_key='user.id')
    name: str | None = Field(default='')

class Newsletter(NewsletterBase, table=True):
    id: uuid.UUID = Field(default_factory=generate_uuid, primary_key=True, unique=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    
    __table_args__ = (
        Index('ix_newsletter_name', 'name'),
    )

class NewsletterCreate(NewsletterBase):
    pass

class NewsletterPublic(NewsletterBase):
    id: uuid.UUID
    
class NewsletterUpdate(SQLModel):
    user: Optional[uuid.UUID] = None
    name: Optional[str] = None
