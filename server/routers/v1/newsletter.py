from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from helpers.database import get_session
from helpers.logging import global_logger
from models.newsletter import Newsletter, NewsletterCreate, NewsletterPublic, NewsletterUpdate
from models.post import Post, PostPublic
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

@router.get("/{newsletter_uuid}", response_model=NewsletterPublic, status_code=status.HTTP_200_OK)
async def get_newsletter(newsletter_uuid: uuid.UUID, request: Request, session: SessionDep) -> Newsletter:
    #logging
    user_agent = request.headers.get('User-Agent')
    newsletter_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, newsletter_id=newsletter_uuid, host=request.client.host)
    
    newsletter_logger.info("newesletter.search.started")
    newsletter = session.exec(select(Newsletter).where(Newsletter.id == newsletter_uuid)).first()

    if not newsletter:
        newsletter_logger.error("newsletter.search.failed", detail="Newsletter not found", status_code=404)
        raise HTTPException(status_code=404, detail='Newsletter not found')
    
    newsletter_logger.info("newsletter.search.success", status_code=200)
    return newsletter

@router.get("/posts/{newsletter_uuid}", response_model=List[PostPublic], status_code=status.HTTP_200_OK)
async def get_posts_by_newsletter(newsletter_uuid: uuid.UUID, request: Request, session: SessionDep) -> List[Post]:
    # logging
    user_agent = request.headers.get('User-Agent')
    newsletter_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, newsletter_id=newsletter_uuid, host=request.client.host)
    
    newsletter_logger.info("posts.search.started")
    posts = session.exec(select(Post).where(Post.newsletter == newsletter_uuid)).all()

    if not posts:
        newsletter_logger.error("newsletter.search.failed", detail="No posts found", status_code=404)
        raise HTTPException(status_code=404, details='There are no posts')

    newsletter_logger.info("newsletter.search.status", status_code=200)
    return posts

@router.patch("/{newsletter_uuid}", response_model=NewsletterPublic, status_code=status.HTTP_200_OK)
async def update_newsletter(newsletter_uuid: uuid.UUID, updated_newsletter: NewsletterUpdate, request: Request, session: SessionDep) -> Newsletter:
    # logging
    user_agent = request.headers.get('User-Agent')
    newsletter_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, newsletter_id=newsletter_uuid, host=request.client.host)
    
    newsletter_logger.info("newsletter.search.started")
    newsletter = session.exec(select(Newsletter).where(Newsletter.id == newsletter_uuid)).first()

    if not newsletter:
        newsletter_logger.error("newsletter.search.failed", detail="Newsletter not found", status_code=400)
        raise HTTPException(status_code=404, detail='Newsletter not found')
    
    newsletter_logger.info("newsletter.update.data_received")
    
    newsletter_data = updated_newsletter.model_dump(exclude_unset=True)
    newsletter.sqlmodel_update(newsletter_data)
    newsletter_logger.info("newsletter.update.database_commit.started")
    session.add(newsletter)
    newsletter_logger.info("newsletter.update.database_commit.success")
    session.commit()
    newsletter_logger.info("newsletter.update.success", status_code=200)
    session.refresh(newsletter)
    return newsletter

@router.post("/", response_model=NewsletterPublic, status_code=status.HTTP_201_CREATED)
async def create_newsletter(newsletter: NewsletterCreate, request: Request, session: SessionDep) -> Newsletter:
    #logging
    user_agent = request.headers.get('User-Agent')
    newsletter_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, host=request.client.host)
    
    newsletter_logger.info("newsletter.validation.started")
    create_newsletter = Newsletter.model_validate(newsletter)
    newsletter_logger.info("newsletter.validation.success")
    newsletter_logger.info("newsletter.creation.database_commit.started")
    session.add(create_newsletter)
    newsletter_logger.info("newsletter.creation.database_commit.success")
    session.commit()
    newsletter_logger.info("newsletter.creation.success", status_code=200)
    session.refresh(create_newsletter)
    return create_newsletter
