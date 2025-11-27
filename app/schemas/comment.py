from datetime import datetime

from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str
    post_id: int


class CommentOut(BaseModel):
    id: int
    content: str
    post_id: int
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
