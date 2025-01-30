from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from models.user import User, UserCreate, UserPublic, UserUpdate
from models.newsletter import Newsletter, NewsletterPublic
from helpers.database import get_session
from helpers.logging import logger, global_logger
import uuid

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        404: {
            "description": "Not found"
        }
    }
)

# session dependency
SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, request: Request, session: SessionDep) -> User:
    # logging
    user_agent = request.headers.get('User-Agent')
    user_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, host=request.client.host)
    
    user_logger.debug("user.creation.validation.started")
    new_user = User.model_validate(user)
    user_logger.debug("user.creation.validation.success")
    user_logger.info("user.creation.database_commit.started")
    session.add(new_user)
    user_logger.info("user.creation.database_commit.success", user_id=new_user.id)
    session.commit()
    user_logger.info("user.creation.success", detail="User created", status_code=status.HTTP_201_CREATED)
    session.refresh(new_user)
    return new_user

@router.get("/{user_uuid}", response_model=UserPublic, status_code=status.HTTP_200_OK)
async def get_user(user_uuid: uuid.UUID, request: Request, session: SessionDep) -> User:
    # logging
    user_agent = request.headers.get('User-Agent')
    user_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, user_id=str(user_uuid), host=request.client.host)
    
    user_logger.debug("user.search.started")
    user = session.exec(select(User).where(User.id == user_uuid)).first()

    if not user:
        user_logger.error("user.search.failed", detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    user_logger.info("user.search.success", detail="User found", status_code=status.HTTP_200_OK)
    return user

@router.patch("/{user_uuid}", response_model=UserPublic, status_code=status.HTTP_200_OK)
async def update_user(user_uuid: uuid.UUID, updated_user: UserUpdate, request: Request, session: SessionDep) -> User:
    # logging
    user_agent = request.headers.get('User-Agent')
    user_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, user_id=str(user_uuid), host=request.client.host)
    
    user_logger.debug("user.search.started")
    user = session.exec(select(User).where(User.id == user_uuid)).first()

    if not user:
        user_logger.error("user.search.failed", detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    user_logger.info("user.update.data_received")
    user_data = updated_user.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_data)
    user_logger.info("user.update.database_commit.started")
    session.add(user)
    user_logger.info("user.update.database_commit.complete")
    session.commit()
    user_logger.info("user.update.success", detail="User updated", status_code=status.HTTP_200_OK)
    session.refresh(user)
    return user

@router.get("/{user_uuid}/newsletters", response_model=List[NewsletterPublic], status_code=status.HTTP_200_OK)
async def get_newsletters_for_users(user_uuid: uuid.UUID, request: Request, session: SessionDep) -> List[Newsletter]:
    # logging
    user_agent = request.headers.get('User-Agent')
    user_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, user_id=str(user_uuid), host=request.client.host)
    
    user_logger.debug("newsletter.search.started")
    newsletters = session.exec(select(Newsletter).where(Newsletter.user == user_uuid)).all()

    if not newsletters:
        user_logger.error("newsletter.search.failed", detail="No newsletters not found", status_code=status.HTTP_404_NOT_FOUND)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No newsletters found')

    user_logger.info("newsletter.search.success", detail="Newsletters found", status_code=status.HTTP_200_OK)
    return newsletters
