from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    Session,
    sessionmaker,
)

from app.config import DB_PATH


class Base(DeclarativeBase, MappedAsDataclass):
    pass


# create engine
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
# create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# create session
SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session]:
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
