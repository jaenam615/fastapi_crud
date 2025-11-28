from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.post import Post


class PostRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, post: Post) -> Post:
        pass

    @abstractmethod
    async def list(self, page: int, size: int, offset: int) -> Sequence[Post]:
        pass

    @abstractmethod
    async def get_by_id(self, post_id: int) -> Post | None:
        pass

    @abstractmethod
    async def delete(self, post_id: int):
        pass


class PostRepository(PostRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, post: Post) -> Post:
        self._session.add(post)
        await self._session.commit()
        await self._session.refresh(post)
        return post

    async def list(self, page: int, size: int, offset: int) -> Sequence[Post]:
        stmt = (
            select(Post)
            .order_by(Post.created_at.desc())
            .limit(size)
            .offset(offset)
            .options(selectinload(Post.author), selectinload(Post.comments))
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, post_id: int) -> Post | None:
        stmt = select(Post).where(Post.id == post_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, post_id: int) -> None:
        stmt = delete(Post).where(Post.id == post_id)
        await self._session.execute(stmt)
        await self._session.commit()
