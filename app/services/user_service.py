from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories.user_repository import user_repo

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def create_user(self, db: Session, data: UserCreate):
        hashed = pwd.hash(data.password)
        user = User(username=data.username, password=hashed)
        return user_repo.create(db, user)

    def authenticate(self, db: Session, username: str, password: str):
        user = user_repo.get_by_username(db, username)
        if not user:
            return None
        if not pwd.verify(password, user.password):
            return None
        return user

user_service = UserService()
