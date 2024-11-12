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

@router.get("/{user_id}")
async def get_all_subscriptions(user_id: int, session: SessionDep):
    subscriptions = session.exec(select(Subscription).where(Subscription.subscriber == user_id).limit(10)).all()
    return subscriptions
