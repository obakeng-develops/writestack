from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from helpers.database import get_session
from models.newsletter import Newsletter, NewsletterCreate, NewsletterPublic, NewsletterUpdate
from models.post import Post, PostPublic
import uuid
import time

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

@router.get("/{newsletter_uuid}", response_model=NewsletterPublic, status_code=status.HTTP_200_OK)
async def get_newsletter(newsletter_uuid: uuid.UUID, request: Request, session: SessionDep) -> Newsletter:
    newsletter = session.exec(select(Newsletter).where(Newsletter.id == newsletter_uuid)).first()

    if not newsletter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Newsletter not found')
    
    return newsletter

@router.get("/posts/{newsletter_uuid}", response_model=List[PostPublic], status_code=status.HTTP_200_OK)
async def get_posts_by_newsletter(newsletter_uuid: uuid.UUID, request: Request, session: SessionDep) -> List[Post]:
    posts = session.exec(select(Post).where(Post.newsletter == newsletter_uuid)).all()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details='There are no posts')

    return posts

@router.patch("/{newsletter_uuid}", response_model=NewsletterPublic, status_code=status.HTTP_200_OK)
async def update_newsletter(newsletter_uuid: uuid.UUID, updated_newsletter: NewsletterUpdate, request: Request, session: SessionDep) -> Newsletter:
    newsletter = session.exec(select(Newsletter).where(Newsletter.id == newsletter_uuid)).first()

    if not newsletter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Newsletter not found')

    newsletter_data = updated_newsletter.model_dump(exclude_unset=True)
    newsletter.sqlmodel_update(newsletter_data)

    session.add(newsletter)
    session.commit()
    session.refresh(newsletter)
    
    return newsletter

@router.post("/", response_model=NewsletterPublic, status_code=status.HTTP_201_CREATED)
async def create_newsletter(newsletter: NewsletterCreate, request: Request, session: SessionDep) -> Newsletter:
    create_newsletter = Newsletter.model_validate(newsletter)
    
    session.add(create_newsletter)
    session.commit()
    session.refresh(create_newsletter)
    
    return create_newsletter
