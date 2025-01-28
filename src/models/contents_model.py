from infra.base import Base

from datetime import datetime
from datetime import timezone
from typing import List

from sqlalchemy import ForeignKey, String

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Content(Base):
    __tablename__ = "contents"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(
        String(1000), unique=False, nullable=False)
    page: Mapped[int] = mapped_column(unique=False, nullable=False)
    images: Mapped[List[str]] = mapped_column(
        ARRAY(String), unique=False, nullable=True)
    create_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now(timezone.utc))
    update_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now(timezone.utc),  onupdate=datetime.now(timezone.utc))
    chapter: Mapped[int] = mapped_column(
        ForeignKey("chapters.id"), nullable=False)

    chapter_relationship = relationship(
        "Chapter", back_populates="content_relationship")

    def to_dict(self):

        return {
            "id": self.id,
            "page": self.page,
            "content": self.content,
            "chapter": self.chapter,
            "create_at": self.create_at,
            "update_at": self.update_at,

        }

    def to_dict_with_chapter(self):
        return {
            "id": self.id,
            "page": self.page,
            "content": self.content,
            "create_at": self.create_at,
            "update_at": self.update_at,
            "chapter": self.chapter_relationship.to_dict_with_etech(),

        }
