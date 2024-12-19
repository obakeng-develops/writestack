from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status, Request
from models.comment import Comment, CommentCreate, CommentPublic, CommentUpdate
from typing import Annotated, List
from helpers.database import get_session
from helpers.logging import global_logger
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

@router.get("/{comment_uuid}", response_model=CommentPublic, status_code=status.HTTP_200_OK)
async def get_comment(comment_uuid: uuid.UUID, request: Request, session: SessionDep) -> Comment:
    # logging
    user_agent = request.headers.get('User-Agent')
    comment_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, comment_id=comment_uuid, host=request.client.host)
    
    comment_logger.info("comment.search.started")
    comment = session.get(Comment, comment_uuid)
    
    if not comment:
        comment_logger.error("comment.search.failed", detail="Comment not found", status_code=404)
        raise HTTPException(status_code=404, detail='Comment not found')
    
    comment_logger.info("comment.search.success", status_code=200)
    return comment

@router.post("/", response_model=CommentPublic, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentCreate, request: Request, session: SessionDep) -> Comment:
    # logging
    user_agent = request.headers.get('User')
    comment_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, host=request.client.host)
    
    comment_logger.info("comment.validation.started")
    create_comment = Comment.model_validate(comment)
    comment_logger.info("comment.validation.success")
    comment_logger.info("comment.creation.database_commmit.started")
    session.add(create_comment)
    session.commit()
    comment_logger.info("comment.creation.database_commmit.success")
    session.refresh(create_comment)
    
    comment_logger.info("comment.creation.success")
    return create_comment

@router.patch("/{comment_uuid}", response_model=CommentPublic, status_code=status.HTTP_200_OK)
async def update_comment(comment_uuid: uuid.UUID, updated_comment: CommentUpdate, request: Request, session: SessionDep) -> Comment:
    # logging
    user_agent = request.headers.get('User')
    comment_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, comment_id=comment_uuid, host=request.client.host)
    
    comment_logger.info("comment.search.started")
    comment = session.get(Comment, comment_uuid)
    
    if not comment:
        comment_logger.error("comment.search.failed", detail="Comment not found", status_code=404)
        raise HTTPException(status_code=404, detail='Comment not found')
    
    comment_logger.info("comment.update.data_received")
    comment_data = updated_comment.model_dump(exclude_unset=True)
    comment.sqlmodel_update(comment_data)
    comment_logger.info("comment.update.database_commit.started")
    session.add(comment)
    session.commit()
    comment_logger.info("comment.update.database_commit.success")
    session.refresh(comment)
    
    comment_logger.info("comment.update.success")
    return comment

@router.delete("/{comment_uuid}", status_code=status.HTTP_200_OK)
async def delete_comment(comment_uuid: uuid.UUID, request: Request, session: SessionDep):
    # logging
    user_agent = request.headers.get('User')
    comment_logger = global_logger.bind(device_type=user_agent, http_scheme=request.url.scheme, route=request.url.path, method=request.method, comment_id=comment_uuid, host=request.client.host)
    
    comment_logger.info("comment.search.started")
    comment = session.get(Comment, comment_uuid)
    
    if not comment:
        comment_logger.error("comment.search.failed", detail="Comment not found", status_code=404)
        raise HTTPException(status_code=404, detail='Comment not found')
    
    comment_logger.info("comment.delete.started")
    session.delete(comment)
    session.commit()
    comment_logger.info("comment.delete.success")
    
    return {
        "message": "Comment deleted successfully"
    }
