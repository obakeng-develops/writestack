from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.user import User
from helpers.database import get_session

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
async def get_user(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    return user

@router.patch("/{user_id}")
async def update_user(user_id: int, updated_user: User, session: SessionDep) -> User:
    user = session.get(user, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    user.first_name = updated_user.first_name
    user.last_name = updated_user.last_name
    user.email = updated_user.email

    session.commit()
    session.refresh()
    return user

