from infra.base import Base

from datetime import datetime
from datetime import timezone

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class TokenBlocklist(Base):
    __tablename__ = "TokenBlocklist"

    id: Mapped[int] = mapped_column(primary_key=True)
    jti: Mapped[str] = mapped_column(nullable=False, index=True)
    create_at: Mapped[str] = mapped_column(
        nullable=False, default=datetime.now(timezone.utc))
