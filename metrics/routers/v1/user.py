from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from models.user import User, UserCreate, UserPublic, UserUpdate
from models.newsletter import Newsletter, NewsletterPublic
from helpers.database import get_session
import uuid
import time

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
    new_user = User.model_validate(user)
   
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return new_user

@router.get("/{user_uuid}", response_model=UserPublic, status_code=status.HTTP_200_OK)
async def get_user(user_uuid: uuid.UUID, request: Request, session: SessionDep) -> User:
    user = session.exec(select(User).where(User.id == user_uuid)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    return user

@router.patch("/{user_uuid}", response_model=UserPublic, status_code=status.HTTP_200_OK)
async def update_user(user_uuid: uuid.UUID, updated_user: UserUpdate, request: Request, session: SessionDep) -> User:
    user = session.exec(select(User).where(User.id == user_uuid)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    user_data = updated_user.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_data)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user

@router.get("/{user_uuid}/newsletters", response_model=List[NewsletterPublic], status_code=status.HTTP_200_OK)
async def get_newsletters_for_users(user_uuid: uuid.UUID, request: Request, session: SessionDep) -> List[Newsletter]:
    newsletters = session.exec(select(Newsletter).where(Newsletter.user == user_uuid)).all()

    if not newsletters:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No newsletters found')
    
    return newsletters
