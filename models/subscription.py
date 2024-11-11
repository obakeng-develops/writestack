from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

class Subscription(SQLModel, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4(), primary_key=True, unique=True)
    subscriber: uuid.UUID = Field(foreign_key='user.id')
    newsletter: uuid.UUID = Field(foreign_key='newsletter.id')
