from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime
from helpers.generate_uuid import generate_uuid

class SubscriptionBase(SQLModel):
    subscriber: uuid.UUID = Field(foreign_key='user.id')
    newsletter: uuid.UUID = Field(foreign_key='newsletter.id')

class Subscription(SubscriptionBase, table=True):
    id: uuid.UUID = Field(default_factory=generate_uuid, primary_key=True, unique=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=None) 

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionPublic(SubscriptionBase):
    id: uuid.UUID
    
class SubscriptionUpdate(SQLModel):
    subcriber: uuid.UUID | None = None
    newsletter: uuid.UUID | None = None
