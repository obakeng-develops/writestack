from sqlmodel import Field, SQLModel, Index
import uuid
from datetime import datetime
from typing import Optional

class UserBase(SQLModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=80)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, unique=True)
    created_at: datetime = Field(default=datetime.today())
    updated_at: datetime = Field(default=datetime.now())
    
    __table_args__ = (
        Index('ix_user_email', 'email'),
    )

class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    id: uuid.UUID

class UserUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
