from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.subscription import Subscription
from typing import Annotated

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

@router.get("/{newsletter_id}")
async def get_all_subscriptions_for_newsletter(newsletter_id: int, session: SessionDep):
    subscriptions = session.exec(select(Subscription).where(Subscription.newsletter == newsletter_id).limit(10)).all()

    if subscriptions is None:
        raise HTTPException(status_code=404, detail='No subscriptions')

    return subscriptions
