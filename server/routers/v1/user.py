from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from models.user import User, UserCreate, UserPublic, UserUpdate
from models.newsletter import Newsletter, NewsletterPublic
from helpers.database import get_session
import uuid
import structlog
import sys
import fastapi

python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
fastapi_version = fastapi.__version__

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

# configure structlog
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ],
)

# logger
log = structlog.get_logger()

@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, request: Request, session: SessionDep) -> User:
    user_agent = request.headers.get('User-Agent')
    
    log.debug("Validating user data...")
    new_user = User.model_validate(user)
    log.debug("Validation complete.")
    session.add(new_user)
    log.info("Adding new user", email=new_user.email, created_at=new_user.created_at, first_name=new_user.first_name, last_name=new_user.last_name, route=request.url.path, status_code=201, method=request.method, device_type=user_agent, py_version=python_version, fastapi_version=fastapi_version)
    session.commit()
    log.info("Committing user to the database.")
    session.refresh(new_user)
    log.info("Refreshing user model")
    return new_user

@router.get("/{user_uuid}", response_model=UserPublic, status_code=status.HTTP_200_OK)
async def get_user(user_uuid: uuid.UUID, request: Request, session: SessionDep) -> User:
    user_agent = request.headers.get('User-Agent')
    
    log.debug("Searching for user with ID %s", user_uuid)
    user = session.exec(select(User).where(User.id == user_uuid)).first()

    if not user:
        log.exception("User ID %s not found", user_uuid, route=request.url.path, status_code=404, method=request.method)
        raise HTTPException(status_code=404, detail='User not found')
    
    log.info("User found", email=user.email, first_name=user.first_name, last_name=user.last_name, route=request.url.path, method=request.method, status_code=200, device_type=user_agent, py_version=python_version, fastapi_version=fastapi_version)
    return user

@router.patch("/{user_uuid}", response_model=UserPublic, status_code=status.HTTP_200_OK)
async def update_user(user_uuid: uuid.UUID, updated_user: UserUpdate, request: Request, session: SessionDep) -> User:
    user_agent = request.headers.get('User-Agent')
    
    log.debug("Searching for user with ID %s", user_uuid)
    user = session.exec(select(User).where(User.id == user_uuid)).first()

    if not user:
        log.exception("User ID %s not found", user_uuid, router=request.url.path, status_code=404, method=request.method, device_type=user_agent)
        raise HTTPException(status_code=404, detail='User not found')
    
    log.info("Updating user %s", user.email)
    user_data = updated_user.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_data)
    log.info("Update completed.")
    log.info("Adding user", email=user.email, first_name=user.first_name, last_name=user.last_name, route=request.url.path, method=request.method, status_code=200, device_type=user_agent, py_version=python_version, fastapi_version=fastapi_version)
    session.add(user)
    log.info("User added")
    session.commit()
    log.info("User committed")
    session.refresh(user)
    return user

@router.get("/newsletters/{user_uuid}", response_model=List[NewsletterPublic], status_code=status.HTTP_200_OK)
async def get_newsletters_for_users(user_uuid: uuid.UUID, request: Request, session: SessionDep) -> List[Newsletter]:
    user_agent = request.headers.get('User-Agent')
    
    log.debug("Searching for newsletters for user with ID %s", user_uuid)
    newsletters = session.exec(select(Newsletter).where(Newsletter.user == user_uuid)).all()

    if not newsletters:
        log.exception("Newsletters not found for user %s", user_uuid, router=request.url.path, status_code=404, method=request.method, device_type=user_agent, py_version=python_version, fastapi_version=fastapi_version)
        raise HTTPException(status_code=404, detail='No newsletters found')

    log.info("Newsletters found", route=request.url.path, status_code=200, method=request.method, device_type=user_agent, py_version=python_version, fastapi_version=fastapi_version)
    return newsletters
