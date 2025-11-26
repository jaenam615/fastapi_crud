from sqlalchemy.orm import Session
from app.models.post import Post

class PostRepository:
    def create(self, db: Session, post: Post):
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    def list(self, db: Session):
        return db.query(Post).all()

    def get(self, db: Session, post_id: int):
        return db.query(Post).filter(Post.id == post_id).first()

post_repo = PostRepository()
