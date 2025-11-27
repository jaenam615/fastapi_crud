from typing import List

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.dependencies import get_comment_service
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentOut

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=CommentOut)
async def create_comment(
    data: CommentCreate,
    comment_service=Depends(get_comment_service),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user.id
    return await comment_service.create_comment(data=data, user_id=user_id)


@router.get("/post/{post_id}", response_model=List[CommentOut])
async def list_comments(
    post_id: int,
    comment_service=Depends(get_comment_service),
):
    return await comment_service.list_comments(post_id=post_id)
