from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException
from models.comment import Comment, CommentCreate, CommentPublic, CommentUpdate
from typing import Annotated, List
from helpers.database import get_session
import uuid

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

@router.get("/{comment_uuid}", response_model=CommentPublic)
async def get_comment(comment_uuid: uuid.UUID, session: SessionDep) -> Comment:
    comment = session.get(Comment, comment_uuid)
    
    if not comment:
        raise HTTPException(status_code=404, detail='Comment not found')
    
    return comment

@router.post("/{comment_uuid}", response_model=CommentPublic)
async def create_comment(comment: CommentCreate, session: SessionDep) -> Comment:
    create_comment = Comment.model_validate(comment)
    session.add(create_comment)
    session.commit()
    session.refresh(create_comment)
    return create_comment

@router.patch("/{comment_uuid}", response_model=CommentPublic)
async def update_comment(comment_uuid: uuid.UUID, updated_comment: CommentUpdate, session: SessionDep) -> Comment:
    comment = session.get(Comment, comment_uuid)
    
    if not comment:
        raise HTTPException(status_code=404, detail='Comment not found')
    
    comment_data = updated_comment.model_dump(exclude_unset=True)
    comment.sqlmodel_update(comment_data)
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment

@router.delete("/{comment_uuid}")
async def delete_comment(comment_uuid: uuid.UUID, session: SessionDep):
    comment = session.get(Comment, comment_uuid)
    
    if not comment:
        raise HTTPException(status_code=404, detail='Comment not found')
    
    session.delete(comment)
    session.commit()
    
    
    return {
        "message": "Comment deleted successfully"
    }
