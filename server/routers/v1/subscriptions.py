from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from helpers.database import get_session
from models.subscription import Subscription, SubscriptionPublic, SubscriptionCreate
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

@router.get("/{newsletter_uuid}", response_model=List[SubscriptionPublic], status_code=status.HTTP_200_OK)
async def get_all_subscriptions_for_newsletter(newsletter_uuid: uuid.UUID, session: SessionDep) -> List[Subscription]:
    subscriptions = session.exec(select(Subscription).where(Subscription.newsletter == newsletter_uuid).limit(10)).all()

    if not subscriptions:
        raise HTTPException(status_code=404, detail='No subscriptions found for the given newsletter')

    return subscriptions

@router.post("/", response_model=SubscriptionPublic, status_code=status.HTTP_200_OK)
async def create_subscription(subscription: SubscriptionCreate, session: SessionDep) -> Subscription:
    new_subscription = Subscription.model_validate(subscription)
    session.add(new_subscription)
    session.commit()
    session.refresh(new_subscription)
    return new_subscription

@router.get("/{subscription_uuid}", response_model=SubscriptionPublic, status_code=status.HTTP_200_OK)
async def get_subscription(subscription_uuid: uuid.UUID, session: SessionDep) -> Subscription:
    subscription = session.exec(select(Subscription).where(Subscription.id == subscription_uuid)).first()

    if not subscription:
        raise HTTPException(status_code=404, detail='Subscription not found')
    
    return subscription
