import json
from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder

from app.core.dependencies import get_current_user
from app.core.redis import RedisConstants, cached_get, cached_set, redis
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
    comment = await comment_service.create_comment(data=data, user_id=user_id)
    await redis.delete(
        f"{RedisConstants.CACHE_KEY_COMMENT_POST}:{data.post_id}:page:1:size:20"
    )
    return comment


@router.get("/post/{post_id}", response_model=List[CommentOut])
async def list_comments(
    post_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    comment_service=Depends(get_comment_service),
):
    cached = await cached_get(
        key=f"{RedisConstants.CACHE_KEY_COMMENT_POST}:{post_id}:page:{page}:size:{size}"
    )
    if cached:
        return json.loads(cached)
    comments = await comment_service.list_comments(
        post_id=post_id, page=page, size=size
    )
    comments_out = [CommentOut.model_validate(c) for c in comments]
    json_data = json.dumps(jsonable_encoder(comments_out))

    await cached_set(
        key=f"{RedisConstants.CACHE_KEY_COMMENT_POST}:{post_id}:page:{page}:size:{size}",
        value=json_data,
        ttl=RedisConstants.CACHE_TTL_COMMENTS,
    )

    return comments
