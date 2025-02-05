from sqlmodel import SQLModel, Field
import uuid
from helpers.generate_uuid import generate_uuid
from datetime import datetime
from typing import Optional

class CommentBase(SQLModel):
    body: str
    post: uuid.UUID = Field(foreign_key='post.id')
    user: uuid.UUID = Field(foreign_key='user.id')

class Comment(CommentBase, table=True):
    id: uuid.UUID = Field(default_factory=generate_uuid, primary_key=True, unique=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

class CommentCreate(CommentBase):
    pass

class CommentPublic(CommentBase):
    id: uuid.UUID
    
class CommentUpdate(SQLModel):
    body: Optional[str] = None
    post: Optional[uuid.UUID] = None
    user: Optional[uuid.UUID] = None
