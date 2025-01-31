from infra.base import Base

from datetime import datetime
from datetime import timezone


from sqlalchemy import String, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str] = mapped_column(String(400), nullable=True)
    description: Mapped[str] = mapped_column(
        String(1000), unique=False, nullable=False)
    user: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True, nullable=False)
    create_at: Mapped[str] = mapped_column(
        nullable=False, default=datetime.now(timezone.utc))
    update_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now(timezone.utc),  onupdate=datetime.now(timezone.utc))

    user_relationship = relationship("User", back_populates="profile")

    def to_dict(self):
        return {
            "id": self.id,
            "image": self.image,
            "description": self.description,
            "user": self.user_relationship.to_dict()
        }
