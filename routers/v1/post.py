from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models.post import Post
from datetime import datetime
from typing import Annotated

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

@router.get("/")
async def get_post(post_id: int, session: SessionDep) -> Post:
    post = session.get(Post, post_id)

    if post is None:
        raise HTTPException(status_code=404, detail='Post not found')
    
    return post

@router.delete("/{post_id}")
async def delete_post(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)

    if post is None:
        raise HTTPException(status_code=404, detail='Post not found')
    
    session.delete(post)
    session.commit()

    return {
        "message": "Post deleted successfully."
    }

@router.post("/")
async def create_post(post: Post, session: SessionDep) -> Post:
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.patch("/{post_id}")
async def update_post(post_id: int, updated_post: Post, session: SessionDep) -> Post:
    post = session.get(Post, post_id)

    if post is None:
        raise HTTPException(status_code=404, detail='Post not found')
    
    post.subtitle = updated_post.subtitle
    post.published = updated_post.published
    post.body = updated_post.body

    session.commit()
    session.refresh()
    return post
