from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.comment import Comment


class CommentRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, comment: Comment) -> Comment:
        pass

    @abstractmethod
    async def list_by_post(self, post_id: int) -> Sequence[Comment]:
        pass


class CommentRepository(CommentRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, comment: Comment) -> Comment:
        self._session.add(comment)
        await self._session.commit()
        await self._session.refresh(comment)
        return comment

    async def list_by_post(self, post_id: int):
        stmt = (
            Select(Comment)
            .where(Comment.post_id == post_id)
            .options(selectinload(Comment.author))
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
