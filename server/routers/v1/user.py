from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.user import User, UserCreate, UserPublic, UserUpdate
from models.newsletter import Newsletter, NewsletterPublic
from helpers.database import get_session
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

SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/", response_model=UserPublic)
async def create_user(user: UserCreate, session: SessionDep) -> User:
    create_user = User.model_validate(user)
    session.add(create_user)
    session.commit()
    session.refresh(create_user)
    return create_user

@router.get("/{user_uuid}", response_model=UserPublic)
async def get_user(user_uuid: uuid.UUID, session: SessionDep) -> User:
    user = session.exec(select(User).where(User.id == user_uuid)).first()

    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    return user

@router.patch("/{user_uuid}", response_model=UserPublic)
async def update_user(user_uuid: uuid.UUID, updated_user: UserUpdate, session: SessionDep) -> User:
    user = session.exec(select(User).where(User.id == user_uuid)).first()

    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    user_data = updated_user.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/newsletters/{user_uuid}", response_model=NewsletterPublic)
async def get_newsletters_for_users(user_uuid: uuid.UUID, session: SessionDep) -> List[Newsletter]:
    newsletters = session.exec(select(Newsletter).where(Newsletter.user == user_uuid)).all()

    if not newsletters:
        raise HTTPException(status_code=404, detail='No newsletters found')

    return newsletters
