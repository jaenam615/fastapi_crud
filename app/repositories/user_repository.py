from asyncmy.errors import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

class UserRepository:
    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, user: User) -> User:
        try:
            db.add(user)
            await db.commit()
        except IntegrityError as e:
            raise e
        await db.refresh(user)
        return user

user_repo = UserRepository()
