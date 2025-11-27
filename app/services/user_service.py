from abc import ABC, abstractmethod

from passlib.context import CryptContext

from app.models.user import User
from app.repositories.user_repository import UserRepositoryInterface
from app.schemas.user import UserCreate

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
        hashed = pwd.hash(data.password)
        user = User(username=data.username, password=hashed)
        return await self._repo.create(user=user)

    async def authenticate(self, username: str, password: str) -> User | None:
        user = await self._repo.get_by_username(username=username)
        if not user:
            return None
        if not pwd.verify(password, user.password):
            return None
        return user
