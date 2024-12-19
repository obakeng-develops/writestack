from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from helpers.database import get_session
from helpers.logging import global_logger
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
async def get_all_subscriptions_for_newsletter(newsletter_uuid: uuid.UUID, request: Request, session: SessionDep) -> List[Subscription]:
    # logging
    user_agent = request.headers.get('User-Agent')
    subscription_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, newsletter_id=newsletter_uuid, host=request.client.host)
    
    subscription_logger.info("subscriptions.search.started")
    subscriptions = session.exec(select(Subscription).where(Subscription.newsletter == newsletter_uuid).limit(10)).all()

    if not subscriptions:
        subscription_logger.error("subscriptions.search.failed", detail="No subscriptions found for the given newsletter", status_code=404)
        raise HTTPException(status_code=404, detail='No subscriptions found for the given newsletter')

    subscription_logger.info("subscriptions.search.success", status_code=200)
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
