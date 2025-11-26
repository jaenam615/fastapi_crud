from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.core.db import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(BigInteger, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    author = relationship("User")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
