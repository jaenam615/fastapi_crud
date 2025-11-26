from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate
from app.repositories.post_repository import post_repo

class PostService:
    def create_post(self, db: Session, data: PostCreate, user_id: int) -> Post:
        post = Post(
            title=data.title,
            content=data.content,
            user_id=user_id,
        )
        return post_repo.create(db, post)

    async def list_posts(self, db: Session) -> list[Post]:
        return await post_repo.list(db)

    async def delete_post(self, db: Session, user_id:int, post_id: int) -> bool:
        post = await post_repo.get(db, post_id)
        if post and post.user_id == user_id:
            db.delete(post)
            db.commit()
            return True
        return False

post_service = PostService()

