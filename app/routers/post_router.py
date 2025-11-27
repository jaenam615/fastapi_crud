from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_current_user
from app.dependencies import get_post_service
from app.models.user import User
from app.schemas.post import PostCreate, PostDeleteOut, PostOut
from app.services.post_service import PostService

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.delete("/{post_id}", response_model=PostDeleteOut)
async def delete_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user.id
    success = await post_service.delete_post(user_id=user_id, post_id=post_id)
    if not success:
        raise HTTPException(status_code=403, detail="Not authorized")
    return PostDeleteOut(success=True, message="Post deleted")


@router.get("/{post_id}", response_model=PostOut)
async def get_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
):
    post = await post_service.get_post_by_id(post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", response_model=PostOut)
async def create_post(
    data: PostCreate,
    post_service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user.id
    return await post_service.create_post(data=data, user_id=user_id)


@router.get("/", response_model=list[PostOut])
async def list_posts(
    post_service: PostService = Depends(get_post_service),
):
    return await post_service.list_posts()
