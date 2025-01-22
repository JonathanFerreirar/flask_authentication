from random import randrange


from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infra.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    name: Mapped[str]
    password: Mapped[str]

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
