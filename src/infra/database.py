from typing import Generator
from dotenv import dotenv_values
from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import Session, sessionmaker

config = {
    **dotenv_values(".env"),
}


DATABASE_URL = config.get('DATABASE_URL')

engine = create_engine(
    DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine)


class DatabaseConnection():
    def __init__(self):
        self.session_factory = SessionLocal

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Provide a transactional scope for database operations."""
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


db_connection = DatabaseConnection()


def get_database_session():
    """Create and manage a database session using a context manager."""
    return db_connection.get_session()
