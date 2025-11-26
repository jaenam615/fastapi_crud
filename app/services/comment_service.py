from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate
from app.repositories.comment_repository import comment_repo

class CommentService:
    def create_comment(self, db: Session, data: CommentCreate, user_id: int):
        comment = Comment(
            content=data.content,
            post_id=data.post_id,
            user_id=user_id
        )
        return comment_repo.create(db, comment)

    def list_comments(self, db: Session, post_id: int):
        return comment_repo.list_by_post(db, post_id)

comment_service = CommentService()
