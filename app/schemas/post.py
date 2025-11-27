from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    model_config = {"from_attributes": True}


class PostDeleteOut(BaseModel):
    success: bool
    message: str | None = None
