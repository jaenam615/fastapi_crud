from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.user import User
from app.schemas.post import PostCreate, PostOut, PostDeleteOut
from app.services.post_service import post_service
from app.core.dependencies import get_current_user


router = APIRouter(prefix="/posts", tags=["Posts"])

@router.delete("/{post_id}", response_model=PostOut)
async def delete_post(
        post_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    user_id = current_user.id
    success = await post_service.delete_post(db, user_id=user_id, post_id=post_id)
    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Not authorized")
    return PostDeleteOut(success=True, message="Post deleted")

@router.post("/", response_model=PostOut)
def create_post(
        data: PostCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    user_id = current_user.id
    return post_service.create_post(db, data, user_id=user_id)

@router.get("/", response_model=list[PostOut])
def list_posts(db: Session = Depends(get_db)):
    return post_service.list_posts(db)

