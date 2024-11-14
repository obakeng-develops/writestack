from sqlmodel import SQLModel, Field
import uuid
from helpers.generate_uuid import generate_uuid

class Comment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=generate_uuid, primary_key=True, unique=True)
    body: str
    post: uuid.UUID = Field(foreign_key='post.id')
    user: uuid.UUID = Field(foreign_key='user.id')
