from sqlmodel import Field, SQLModel
import uuid
from datetime import datetime

class UserBase(SQLModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=80)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, unique=True)
    created_at: datetime = Field(default=datetime.today())
    updated_at: datetime = Field(default=datetime.now())

class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    id: uuid.UUID

class UserUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
