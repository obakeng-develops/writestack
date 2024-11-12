from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

def generate_uuid():
    return str(uuid.uuid4())

class Subscription(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=generate_uuid, primary_key=True, unique=True)
    subscriber: uuid.UUID = Field(foreign_key='user.id')
    newsletter: uuid.UUID = Field(foreign_key='newsletter.id')
