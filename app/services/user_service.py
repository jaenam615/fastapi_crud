from abc import ABC, abstractmethod

from app.core.hash import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepositoryInterface
from app.schemas.user import UserCreate


class UserServiceInterface(ABC):
    @abstractmethod
    async def create_user(self, data: UserCreate) -> User:
        pass

    @abstractmethod
    async def authenticate(self, username: str, password: str) -> User | None:
        pass


class UserService(UserServiceInterface):
    def __init__(self, repo: UserRepositoryInterface):
        self._repo = repo

    async def create_user(self, data: UserCreate) -> User:
        hashed = await hash_password(data.password)
        user = User(username=data.username, password=hashed)
        return await self._repo.create(user=user)

    async def authenticate(self, username: str, password: str) -> User | None:
        user = await self._repo.get_by_username(username=username)
        if not user:
            return None
        if not await verify_password(password, user.password):
            return None
        return user
