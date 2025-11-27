from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.repositories.comment_repository import CommentRepository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.services.comment_service import CommentService, CommentServiceInterface
from app.services.post_service import PostService, PostServiceInterface
from app.services.user_service import UserService, UserServiceInterface


class DependencyService:
    @staticmethod
    def get_user_service(db: AsyncSession) -> UserService:
        user_repo = UserRepository(session=db)
        return UserService(repo=user_repo)

    @staticmethod
    def get_post_service(db: AsyncSession) -> PostService:
        post_repo = PostRepository(session=db)
        return PostService(repo=post_repo)

    @staticmethod
    def get_comment_service(db: AsyncSession) -> CommentService:
        comment_repo = CommentRepository(session=db)
        return CommentService(repo=comment_repo)


def get_user_service(
    db: AsyncSession = Depends(get_db),
) -> UserServiceInterface:
    return DependencyService.get_user_service(db)


def get_post_service(
    db: AsyncSession = Depends(get_db),
) -> PostServiceInterface:
    return DependencyService.get_post_service(db)


def get_comment_service(
    db: AsyncSession = Depends(get_db),
) -> CommentServiceInterface:
    return DependencyService.get_comment_service(db)
