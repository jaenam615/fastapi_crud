from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.post import PostCreate, PostOut
from app.services.post_service import post_service

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostOut)
def create_post(data: PostCreate, db: Session = Depends(get_db)):
    return post_service.create_post(db, data, user_id=1)  # placeholder

@router.get("/", response_model=list[PostOut])
def list_posts(db: Session = Depends(get_db)):
    return post_service.list_posts(db)
