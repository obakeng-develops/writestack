from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from helpers.database import get_session
from models.subscription import Subscription
from typing import Annotated
import uuid

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
    responses={
        404: {
            "description": "Not found"
        }
    },
)

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/{newsletter_uuid}")
async def get_all_subscriptions_for_newsletter(newsletter_uuid: uuid.UUID, session: SessionDep):
    subscriptions = session.exec(select(Subscription).where(Subscription.newsletter == newsletter_uuid).limit(10)).all()

    if subscriptions is None:
        raise HTTPException(status_code=404, detail='No subscriptions')

    return subscriptions
