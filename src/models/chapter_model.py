from infra.base import Base

from datetime import datetime
from datetime import timezone

from sqlalchemy import ForeignKey, String

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Chapter(Base):
    __tablename__ = "chapters"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(155), unique=False, nullable=False)
    chapter_number: Mapped[int] = mapped_column(unique=False, nullable=False)
    create_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now(timezone.utc))
    update_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now(timezone.utc),  onupdate=datetime.now(timezone.utc))
    etech: Mapped[int] = mapped_column(
        ForeignKey("etechs.id"), nullable=False)

    etech_relationship = relationship(
        "Etech", back_populates="chapter_relationship")

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "create_at": self.create_at,
            "update_at": self.update_at,
            "chapter_number": self.chapter_number,
            "etech": self.etech,

        }

    def to_dict_with_etech(self):
        return {
            "id": self.id,
            "title": self.title,
            "create_at": self.create_at,
            "update_at": self.update_at,
            "chapter_number": self.chapter_number,
            "etech_id": self.etech_relationship.to_dict(),

        }
