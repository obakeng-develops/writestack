from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from helpers.database import get_session
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
async def get_post(post_uuid: uuid.UUID, session: SessionDep) -> Post:
    post = session.exec(select(Post).where(Post.id == post_uuid)).first()

    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    
    return post

@router.delete("/{post_uuid}", response_model=PostPublic, status_code=status.HTTP_200_OK)
async def delete_post(post_uuid: uuid.UUID, session: SessionDep):
    post = session.exec(select(Post).where(Post.id == post_uuid)).first()

    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    
    session.delete(post)
    session.commit()

    return {
        "message": "Post deleted successfully."
    }

@router.get("/comments/{post_uuid}", response_model=List[CommentPublic], status_code=status.HTTP_200_OK)
async def get_all_comments_for_post(post_uuid: uuid.UUID, session: SessionDep) -> List[Comment]:
    comments = session.exec(select(Comment).where(Comment.post == post_uuid)).all()

    if not comments:
        raise HTTPException(status_code=404, detail='Comments not found')
    
    return comments

@router.post("/", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, session: SessionDep) -> Post:
    create_post = Post.model_validate(post)
    session.add(create_post)
    session.commit()
    session.refresh(create_post)
    return create_post

@router.patch("/{post_uuid}", response_model=PostPublic, status_code=status.HTTP_200_OK)
async def update_post(post_uuid: uuid.UUID, updated_post: PostUpdate, session: SessionDep) -> Post:
    post = session.exec(select(Post).where(Post.id == post_uuid)).first()

    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    
    post_data = updated_post.model_dump(exclude_unset=True)
    post.sqlmodel_update(post_data)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post
