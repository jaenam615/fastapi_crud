from random import choice
from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings

write_engine = create_async_engine(
    settings.DATABASE_WRITE_URL,
    echo=False,
    future=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
)

read_engines = [
    create_async_engine(
        url,
        echo=False,
        future=True,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_timeout=settings.DB_POOL_TIMEOUT,
    )
    for url in settings.DATABASE_READ_URLS
]


def get_read_engine():
    return choice(read_engines)


class Base(DeclarativeBase):
    pass


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    engine = request.state.db_engine
    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
        class_=AsyncSession,
    )

    async with AsyncSessionLocal() as db:
        yield db
