from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentOut
from app.services.comment_service import comment_service
from app.core.db import get_db

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentOut)
def create_comment(
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user.id
    return comment_service.create_comment(db, data, user_id=user_id)

@router.get("/post/{post_id}", response_model=List[CommentOut])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    return comment_service.list_comments(db, post_id)
