from infra.base import Base

from datetime import datetime
from datetime import timezone

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    etech: Mapped[int] = mapped_column(
        ForeignKey("etechs.id"), nullable=False)
    comment: Mapped[str] = mapped_column(
        String(1000), unique=False, nullable=False)
    create_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now(timezone.utc))
    update_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now(timezone.utc),  onupdate=datetime.now(timezone.utc))

    user_relationship = relationship("User", back_populates="comments")
    etech_relationship = relationship(
        "Etech", back_populates="comments_relationship")

    def to_dict(self):

        return {
            "id": self.id,
            "etech": self.etech,
            "comment": self.comment,
            "create_at": self.create_at,
            "update_at": self.update_at,
            "user": self.user_relationship.dict_without_email(),

        }

    def to_dict_completed(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "create_at": self.create_at,
            "update_at": self.update_at,
            "etech": self.etech_relationship.to_dict(),
            "user": self.user_relationship.dict_without_email(),
        }
