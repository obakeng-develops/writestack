from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from helpers.database import get_session
from models.newsletter import Newsletter
from models.post import Post
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/newsletters",
    tags=["newsletters"],
    responses={
        404: {
            "description": "Not found"
        }
    },
)

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/{newsletter_id}")
async def get_newsletter(newsletter_id: uuid.UUID, session: SessionDep) -> Newsletter:
    newsletter = session.get(Newsletter, newsletter_id)

    if newsletter is None:
        raise HTTPException(status_code=404, detail='Newsletter not found')
    
    return newsletter

@router.get("/posts/{newsletter_id}")
async def get_posts_by_newsletter(newsletter_id: uuid.UUID, session: SessionDep) -> List[Post]:
    posts = session.exec(select(Post).where(Post.newsletter == newsletter_id)).all()

    if posts is None:
        raise HTTPException(status_code=404, details='There are no posts')

    return posts

@router.patch("/{newsletter_id}")
async def update_newsletter(newsletter_id: uuid.UUID, updated_newsletter: Newsletter, session: SessionDep) -> Newsletter:
    newsletter = session.get(Newsletter, newsletter_id)

    if newsletter is None:
        raise HTTPException(status_code=404, detail='Newsletter not found')
    
    newsletter.name = updated_newsletter.name 
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
