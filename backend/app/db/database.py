from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    Session,
    sessionmaker,
)
from sqlalchemy.pool import StaticPool

from app.config import DB_PATH, USE_SAMPLE_DATA


class Base(DeclarativeBase, MappedAsDataclass):
    pass


# create engine
if USE_SAMPLE_DATA:
    # create an in-memory database
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
# create session
SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session]:
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
