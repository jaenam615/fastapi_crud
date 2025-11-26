from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository, user_repo
from app.schemas.user import UserCreate

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, repo: UserRepository):
        self.user_repo = repo

    async def create_user(self, db: AsyncSession, data: UserCreate):
        hashed = pwd.hash(data.password)
        user = User(username=data.username, password=hashed)
        return await self.user_repo.create(db, user)

    async def authenticate(self, db: AsyncSession, username: str, password: str):
        user = await self.user_repo.get_by_username(db, username)
        if not user:
            return None
        if not pwd.verify(password, user.password):
            return None
        return user


def get_user_service(repo: UserRepository = user_repo) -> UserService:
    return UserService(repo)
