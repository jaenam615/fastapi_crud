import json

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_201_CREATED

from app.core.dependencies import get_current_user
from app.core.redis import RedisConstants, cached_get, cached_set, redis
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
    await redis.delete(RedisConstants.CACHE_KEY_POST_ALL)
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


@router.post(
    "/",
    response_model=PostOut,
    status_code=HTTP_201_CREATED,
)
async def create_post(
    data: PostCreate,
    post_service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):

    user_id = current_user.id
    post = await post_service.create_post(data=data, user_id=user_id)
    await redis.delete(RedisConstants.CACHE_KEY_POST_ALL)
    return post


@router.get("/", response_model=list[PostOut])
async def list_posts(
    post_service: PostService = Depends(get_post_service),
):
    cached = await cached_get(key=RedisConstants.CACHE_KEY_POST_ALL)
    if cached:
        return json.loads(cached)
    posts = await post_service.list_posts()
    posts_out = [PostOut.model_validate(p) for p in posts]

    await cached_set(
        key=RedisConstants.CACHE_KEY_POST_ALL,
        value=json.dumps([p.model_dump() for p in posts_out]),
        ttl=RedisConstants.CACHE_TTL_POSTS,
    )
    return posts
