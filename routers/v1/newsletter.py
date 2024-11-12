from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models.newsletter import Newsletter
from datetime import datetime

router = APIRouter(
    prefix="/newsletter",
    tags=["newsletter"],
    responses={
        404: {
            "description": "Not found"
        }
    },
)

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/{newsletter_id}")
async def get_newsletter(newsletter_id: Newsletter, session: SessionDep) -> Newsletter:
    newsletter = session.get(Newsletter, newsletter_id)

    if newsletter is None:
        raise HTTPException(status_code=404, detail='Newsletter not found')
    
    return newsletter

@router.patch("/{newsletter_id}")
async def update_newsletter(newsletter_id: id, updated_newsletter: Newsletter, session: SessionDep) -> Newsletter:
    newsletter = session.get(newsletter, newsletter_id)

    if newsletter is None:
        raise HTTPException(status_code=404, detail='Newsletter not found')
    
    newsletter.name = update_newsletter.name 
    newsletter.updated_at = datetime.now()

    session.commit()
    session.refresh()
    return newsletter

@router.post("/{newsletter_id}")
async def create_newsletter(newsletter: Newsletter, session: SessionDep) -> Newsletter:
    session.add(newsletter)
    session.commit()
    session.refresh(newsletter)
    return newsletter
