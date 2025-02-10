from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status, Request
from models.comment import Comment, CommentCreate, CommentPublic, CommentUpdate
from typing import Annotated, List
from helpers.database import get_session
from helpers.logging import global_logger
import uuid
import time

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={
        404: {
            "description": "Not found"
        }
    },
)

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/{comment_uuid}", response_model=CommentPublic, status_code=status.HTTP_200_OK)
async def get_comment(comment_uuid: uuid.UUID, request: Request, session: SessionDep) -> Comment:    
    comment = session.get(Comment, comment_uuid)
    
    if not comment:
        raise HTTPException(status_code=404, detail='Comment not found')

    return comment

@router.post("/", response_model=CommentPublic, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentCreate, request: Request, session: SessionDep) -> Comment:
    create_comment = Comment.model_validate(comment)
    session.add(create_comment)
    session.commit()
    session.refresh(create_comment)
    return create_comment

@router.patch("/{comment_uuid}", response_model=CommentPublic, status_code=status.HTTP_200_OK)
async def update_comment(comment_uuid: uuid.UUID, updated_comment: CommentUpdate, request: Request, session: SessionDep) -> Comment:
    comment = session.get(Comment, comment_uuid)
    
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found')
    
    comment_data = updated_comment.model_dump(exclude_unset=True)
    comment.sqlmodel_update(comment_data)
    
    session.add(comment)
    session.commit()
    session.refresh(comment)
    
    return comment

@router.delete("/{comment_uuid}", status_code=status.HTTP_200_OK)
async def delete_comment(comment_uuid: uuid.UUID, request: Request, session: SessionDep):
    comment = session.get(Comment, comment_uuid)
    
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found')

    session.delete(comment)
    session.commit()
    
    return {
        "message": "Comment deleted successfully"
    }
