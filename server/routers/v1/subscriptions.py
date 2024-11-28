from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from helpers.database import get_session
from models.subscription import Subscription, SubscriptionPublic
from typing import Annotated, List
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

@router.get("/newsletter/{newsletter_uuid}", response_model=SubscriptionPublic, status_code=status.HTTP_200_OK)
async def get_all_subscriptions_for_newsletter(newsletter_uuid: uuid.UUID, session: SessionDep) -> List[Subscription]:
    subscriptions = session.exec(select(Subscription).where(Subscription.newsletter == newsletter_uuid).limit(10)).all()

    if not subscriptions:
        raise HTTPException(status_code=404, detail='No subscriptions found for the given newsletter')

    return subscriptions
