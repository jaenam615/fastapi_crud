from abc import ABC, abstractmethod
from typing import Sequence

from app.models.post import Post
from app.repositories.post_repository import PostRepositoryInterface
from app.schemas.post import PostCreate


class PostServiceInterface(ABC):
    @abstractmethod
    def create_post(self, data: PostCreate, user_id: int) -> Post:
        pass

    @abstractmethod
    async def list_posts(self, page: int, size: int) -> list[Post]:
        pass

    @abstractmethod
    async def delete_post(self, user_id: int, post_id: int) -> bool:
        pass

    @abstractmethod
    async def get_post_by_id(self, post_id: int) -> Post:
        pass


class PostService(PostServiceInterface):
    def __init__(self, repo: PostRepositoryInterface):
        self._repo = repo

    async def create_post(self, data: PostCreate, user_id: int) -> Post:
        post = Post(
            title=data.title,
            content=data.content,
            user_id=user_id,
        )
        return await self._repo.create(post=post)

    async def list_posts(self, page: int, size: int) -> Sequence[Post]:
        offset = (page - 1) * size
        return await self._repo.list(page=page, size=size, offset=offset)

    async def get_post_by_id(self, post_id: int) -> Post:
        return await self._repo.get_by_id(post_id=post_id)

    async def delete_post(self, user_id: int, post_id: int) -> bool:
        post = await self._repo.get_by_id(post_id=post_id)
        if post and post.user_id == user_id:
            await self._repo.delete(post_id=post_id)
            return True
        return False
