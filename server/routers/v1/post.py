from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from helpers.database import get_session
from models.post import Post
from models.comment import Comment
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

@router.get("/{post_uuid}")
async def get_post(post_uuid: uuid.UUID, session: SessionDep) -> Post:
    post = session.exec(select(Post).where(Post.id == post_uuid)).first()

    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    
    return post

@router.delete("/{post_uuid}")
async def delete_post(post_uuid: uuid.UUID, session: SessionDep):
    post = session.exec(select(Post).where(Post.id == post_uuid)).first()

    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    
    session.delete(post)
    session.commit()

    return {
        "message": "Post deleted successfully."
    }

@router.get("/comments/{post_uuid}")
async def get_all_comments_for_post(post_uuid: uuid.UUID, session: SessionDep) -> List[Comment]:
    comments = session.exec(select(Comment).where(Comment.post == post_uuid)).all()

    if not comments:
        raise HTTPException(status_code=404, detail='Comments not found')
    
    return comments

@router.post("/")
async def create_post(post: Post, session: SessionDep) -> Post:
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.patch("/{post_uuid}")
async def update_post(post_uuid: uuid.UUID, updated_post: Post, session: SessionDep) -> Post:
    post = session.exec(select(Post).where(Post.id == post_uuid)).first()

    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    
    post.subtitle = updated_post.subtitle
    post.published = updated_post.published
    post.body = updated_post.body

    session.commit()
    session.refresh()
    return post
