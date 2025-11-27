from abc import ABC, abstractmethod

from app.models.comment import Comment
from app.repositories.comment_repository import CommentRepository
from app.schemas.comment import CommentCreate


class CommentServiceInterface(ABC):
    @abstractmethod
    async def create_comment(self, data: CommentCreate, user_id: int):
        pass

    @abstractmethod
    async def list_comments(self, post_id: int):
        pass


class CommentService(CommentServiceInterface):
    def __init__(self, repo: CommentRepository):
        self._repo = repo

    async def create_comment(self, data: CommentCreate, user_id: int):
        comment = Comment(content=data.content, post_id=data.post_id, user_id=user_id)
        return await self._repo.create(comment=comment)

    async def list_comments(self, post_id: int):
        return await self._repo.list_by_post(post_id)
