from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate
from app.repositories.post_repository import post_repo

class PostService:
    def create_post(self, db: Session, data: PostCreate, user_id: int):
        post = Post(
            title=data.title,
            content=data.content,
            author_id=user_id,
        )
        return post_repo.create(db, post)

    def list_posts(self, db: Session):
        return post_repo.list(db)
post_service = PostService()

