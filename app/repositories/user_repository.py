from abc import ABC, abstractmethod

from asyncmy.errors import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        pass


class UserRepository(UserRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        try:
            self._session.add(user)
            await self._session.commit()
        except IntegrityError as e:
            await self._session.rollback()
            raise e
        await self._session.refresh(user)
        return user
