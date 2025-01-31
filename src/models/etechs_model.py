from infra.base import Base

from datetime import datetime
from datetime import timezone

from sqlalchemy import ForeignKey, String

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Etech(Base):
    __tablename__ = "etechs"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str] = mapped_column(String(400), nullable=True)
    price: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(
        String(155), unique=True, nullable=False)
    user: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    topics: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    description: Mapped[str] = mapped_column(
        String(1000), unique=True, nullable=False)
    create_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now(timezone.utc))
    update_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now(timezone.utc),  onupdate=datetime.now(timezone.utc))

    user_relationship = relationship("User", back_populates="etechs")
    chapter_relationship = relationship(
        "Chapter", back_populates="etech_relationship")
    comments_relationship = relationship(
        "Comment", back_populates="etech_relationship")

    def to_dict(self):
        return {
            "id": self.id,
            "image": self.image,
            "price": self.price,
            "title": self.title,
            "topics": self.topics,
            "create_at": self.create_at,
            "update_at": self.update_at,
            "description": self.description,
            "user": self.user_relationship.to_dict(),
        }

    def bring_just_comments(self):
        return {
            "comments": [comment.to_dict() for comment in self.comments_relationship]
        }

    def brins_jus_chapters(self):
        return {
            "chapters": [chapter.to_dict() for chapter in self.chapter_relationship]
        }
