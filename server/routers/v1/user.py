from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.user import User
from models.newsletter import Newsletter
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

@router.post("/")
async def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/{user_id}")
async def get_user(user_id: uuid.UUID, session: SessionDep) -> User:
    user = session.get(User, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    return user

@router.patch("/{user_id}")
async def update_user(user_id: uuid.UUID, updated_user: User, session: SessionDep) -> User:
    user = session.get(user, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    user.first_name = updated_user.first_name
    user.last_name = updated_user.last_name
    user.email = updated_user.email

    session.commit()
    session.refresh()
    return user

@router.get("/newsletters/{user_id}")
async def get_newsletters_for_users(user_id: uuid.UUID, session: SessionDep) -> List[Newsletter]:
    newsletters = session.exec(select(Newsletter).where(Newsletter.user == user_id)).all()

    if newsletters is None:
        raise HTTPException(status_code=404, detail='No newsletters found')

    return newsletters
