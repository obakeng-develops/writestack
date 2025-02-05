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
    subscription_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route_path=request.url.path, method=request.method, newsletter_id=str(newsletter_uuid), host=request.client.host, route_prefix=router.prefix)
    
    subscription_logger.info("subscriptions.search.started")
    subscriptions = session.exec(select(Subscription).where(Subscription.newsletter == newsletter_uuid).limit(10)).all()

    if not subscriptions:
        subscription_logger.error("subscriptions.search.failed", detail="No subscriptions found for the given newsletter", status_code=status.HTTP_404_NOT_FOUND)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No subscriptions found for the given newsletter')

    subscription_logger.info("subscriptions.search.success", detail="Subscriptions found", status_code=status.HTTP_200_OK)
    return subscriptions

@router.post("/", response_model=SubscriptionPublic, status_code=status.HTTP_200_OK)
async def create_subscription(subscription: SubscriptionCreate, request: Request, session: SessionDep) -> Subscription:
    # logging
    user_agent = request.headers.get('User-Agent')
    subscription_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route_path=request.url.path, method=request.method, host=request.client.host, route_prefix=router.prefix)
    
    subscription_logger.debug("subscription.creation.validation.started")
    new_subscription = Subscription.model_validate(subscription)
    subscription_logger.debug("subscription.creation.validation.success")
    subscription_logger.info("subscription.creation.database_commit.started")
    session.add(new_subscription)
    subscription_logger.info("subscription.creation.database_commit.success")
    session.commit()
    subscription_logger.info("subscription.creation.success", detail="Subscription created", status_code=status.HTTP_201_CREATED, subscription_id=new_subscription.id)
    session.refresh(new_subscription)
    return new_subscription

@router.get("/{subscription_uuid}", response_model=SubscriptionPublic, status_code=status.HTTP_200_OK)
async def get_subscription(subscription_uuid: uuid.UUID, request: Request, session: SessionDep) -> Subscription:
    # logging
    user_agent = request.headers.get('User-Agent')
    subscription_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route_path=request.url.path, method=request.method, host=request.client.host, route_prefix=router.prefix)
    
    subscription_logger.debug("subscription.search.started")
    subscription = session.exec(select(Subscription).where(Subscription.id == subscription_uuid)).first()

    if not subscription:
        subscription_logger.error("subscription.search.failed", detail="Subscription not found", status_code=status.HTTP_404_NOT_FOUND)
        raise HTTPException(status_code=404, detail='Subscription not found')
    
    subscription_logger.info("subscription.search.success", detail="Subscription found", status_code=status.HTTP_200_OK)
    return subscription
