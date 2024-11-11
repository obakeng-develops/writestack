from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

class Comment(SQLModel, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4(), primary_key=True, unique=True)
    body: str
    user: uuid.UUID = Field(foreign_key='user.id')
