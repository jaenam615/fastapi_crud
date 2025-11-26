from sqlalchemy.orm import Session
from app.models.comment import Comment

class CommentRepository:
    def create(self, db: Session, comment: Comment):
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    def list_by_post(self, db: Session, post_id: int):
        return db.query(Comment).filter(Comment.post_id == post_id).all()

comment_repo = CommentRepository()
