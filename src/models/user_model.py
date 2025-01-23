from infra.base import Base

from datetime import datetime
from datetime import timezone

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    create_at: Mapped[str] = mapped_column(
        nullable=False, default=datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,

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
