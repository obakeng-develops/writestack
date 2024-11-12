from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime
from helpers.generate_uuid import generate_uuid

class Subscription(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=generate_uuid, primary_key=True, unique=True)
    subscriber: uuid.UUID = Field(foreign_key='user.id')
    newsletter: uuid.UUID = Field(foreign_key='newsletter.id')
