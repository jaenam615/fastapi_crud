from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.comment import CommentCreate, CommentOut
from app.services.comment_service import comment_service
from app.core.db import get_db

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentOut)
def create_comment(data: CommentCreate, db: Session = Depends(get_db)):
    # Replace user_id=1 with actual authenticated user in production
    return comment_service.create_comment(db, data, user_id=1)

@router.get("/post/{post_id}", response_model=List[CommentOut])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    return comment_service.list_comments(db, post_id)
