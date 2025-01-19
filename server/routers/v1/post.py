from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from helpers.database import get_session
from helpers.logging import logger, global_logger
from models.post import Post, PostPublic, PostCreate, PostUpdate
from models.comment import Comment, CommentPublic
from datetime import datetime
from typing import Annotated
import uuid
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={
        404: {
            "description": "Not found"
        }
    },
)

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/{post_uuid}", response_model=PostPublic, status_code=status.HTTP_200_OK)
async def get_post(post_uuid: uuid.UUID, request: Request, session: SessionDep) -> Post:
    # logging
    user_agent = request.headers.get('User-Agent')
    post_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, post_id=str(post_uuid), host=request.client.host)
    
    post_logger.info("post.search.started")
    post = session.exec(select(Post).where(Post.id == post_uuid)).first()

    if not post:
        post_logger.error("post.search.failed", detail="Post not found", status_code=404)
        raise HTTPException(status_code=404, detail='Post not found')
    
    post_logger.info("post.search.success", detail="Post found", status_code=200, subtitle=post.subtitle, published=post.published, post_newsletter_id=post.newsletter)
    return post

@router.delete("/{post_uuid}", response_model=PostPublic, status_code=status.HTTP_200_OK)
async def delete_post(post_uuid: uuid.UUID, request: Request, session: SessionDep):
    # logging
    user_agent = request.headers.get('User-Agent')
    post_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, post_id=str(post_uuid), host=request.client.host)
    
    post_logger.info("post.search.started")
    post = session.exec(select(Post).where(Post.id == post_uuid)).first()

    if not post:
        post_logger.error("post.search.failed", detail="User not found", status_code=404)
        raise HTTPException(status_code=404, detail='Post not found')
    
    post_logger.info("post.delete.started")
    session.delete(post)
    post_logger.info("post.delete.database_commit.started")
    session.commit()
    post_logger.info("post.delete.database_commit.success", detail="Post deleted", status_code=200)

    return {
        "message": "Post deleted successfully."
    }

@router.get("/comments/{post_uuid}", response_model=List[CommentPublic], status_code=status.HTTP_200_OK)
async def get_all_comments_for_post(post_uuid: uuid.UUID, request: Request, session: SessionDep) -> List[Comment]:
    # logging
    user_agent = request.headers.get('User-Agent')
    post_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, post_id=str(post_uuid), host=request.client.host)
    
    post_logger.info("comments.search.started")
    comments = session.exec(select(Comment).where(Comment.post == post_uuid)).all()

    if not comments:
        post_logger.error("comment.search.failed", detail="Comment not found", status_code=404)
        raise HTTPException(status_code=404, detail='Comments not found')
    
    comment_data = [(comment.post, comment.user) for comment in comments]
    
    post_logger.info("comments.search.success", detail="Comments found", status_code=200, comments=comment_data)
    return comments

@router.post("/", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, request: Request, session: SessionDep) -> Post:
    # logging 
    user_agent = request.headers.get('User-Agent')
    post_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, host=request.client.host)
    
    post_logger.debug("post.validation.started")
    create_post = Post.model_validate(post)
    post_logger.debug("post.validation.success")
    post_logger.info("post.creation.started")
    session.add(create_post)
    post_logger.info("post.creation.database_commit.started")
    session.commit()
    post_logger.info("post.creation.database_commit.success")
    session.refresh(create_post)
    post_logger.info("post.creation.success", detail="Post created", status_code=201, post_id=str(create_post.id), subtitle=create_post.subtitle, published=create_post.published, post_newsletter_id=create_post.newsletter)
    return create_post

@router.patch("/{post_uuid}", response_model=PostPublic, status_code=status.HTTP_200_OK)
async def update_post(post_uuid: uuid.UUID, updated_post: PostUpdate, request: Request, session: SessionDep) -> Post:
    # logging 
    user_agent = request.headers.get('User-Agent')
    post_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, post_id=str(post_uuid), host=request.client.host)
    
    post_logger.info("post.search.started")
    post = session.exec(select(Post).where(Post.id == post_uuid)).first()

    if not post:
        post_logger.error("post.search.failed", detail="Post not found", status_code=404)
        raise HTTPException(status_code=404, detail='Post not found')
    
    post_logger.info("post.update.data_received")
    post_data = updated_post.model_dump(exclude_unset=True)
    post.sqlmodel_update(post_data)
    post_logger.info("post.update.database_commit.started")
    session.add(post)
    post_logger.info("post.update.database_commit.success")
    session.commit()
    post_logger.info("post.update.success", status_code=200, subtitle=post.subtitle, published=post.published, post_newsletter_id=post.newsletter)
    session.refresh(post)
    return post
