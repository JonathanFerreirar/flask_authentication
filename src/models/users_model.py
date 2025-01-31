from infra.base import Base

from datetime import datetime
from datetime import timezone


from sqlalchemy import String
from .etechs_model import Etech

from .comments_model import Comment

from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(155), nullable=False)
    password: Mapped[str] = mapped_column(String(155), nullable=False)
    email: Mapped[str] = mapped_column(
        String(155), unique=True, nullable=False)
    create_at: Mapped[str] = mapped_column(
        nullable=False, default=datetime.now(timezone.utc))
    update_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now(timezone.utc),  onupdate=datetime.now(timezone.utc))

    etechs: Mapped[list["Etech"]] = relationship(
        "Etech", back_populates="user_relationship")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="user_relationship")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,

        }

    def dict_without_email(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def to_dict_complete(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password

        }

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"
