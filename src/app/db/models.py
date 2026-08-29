from sqlalchemy import (
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    user_name: Mapped[str] = mapped_column(String(255), default="", unique=True)
    # name: Mapped[str] = mapped_column(String(255, collation="NOCASE"), default="")
    # email: Mapped[str] = mapped_column(String(255), default="")
    # password: Mapped[str] = mapped_column(String(255), default="")
    # is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    # last_login_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    # last_access_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    # created_at: Mapped[datetime] = mapped_column(DateTime, default_factory=datetime.utcnow)
    # updated_at: Mapped[datetime] = mapped_column(DateTime, default_factory=datetime.utcnow)


class Artist(Base):
    __tablename__ = "artist"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]


class Album(Base):
    __tablename__ = "album"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    artist: Mapped[str]
    artist_id: Mapped[str]
    song_count: Mapped[int] = mapped_column(default=0)


class MediaFile(Base):
    __tablename__ = "media_file"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    # path: Mapped[str] = mapped_column(String(255), default="")
    title: Mapped[str] = mapped_column(String(255), default="")
    artist: Mapped[str] = mapped_column(String(255), default="")
    artist_id: Mapped[str] = mapped_column(String(255), default="")
    album: Mapped[str] = mapped_column(String(255), default="")
    # album_artist: Mapped[str] = mapped_column(String(255), default="")
    album_id: Mapped[str] = mapped_column(String(255), default="")
    # has_cover_art: Mapped[bool] = mapped_column(Boolean, default=False)
    # track_number: Mapped[int] = mapped_column(Integer, default=0)
    # disc_number: Mapped[int] = mapped_column(Integer, default=0)
    # year: Mapped[int] = mapped_column(Integer, default=0)
    # size: Mapped[int] = mapped_column(Integer, default=0)
    # suffix: Mapped[str] = mapped_column(String(255), default="")
    duration: Mapped[float] = mapped_column(Float, default=0)
    # bit_rate: Mapped[int] = mapped_column(Integer, default=0)
    # genre: Mapped[str] = mapped_column(String(255), default="")
    # compilation: Mapped[bool] = mapped_column(Boolean, default=False)
    # created_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    # updated_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)


class Annotation(Base):
    __tablename__ = "annotation"
    __table_args__ = (UniqueConstraint("user_id", "item_id", "item_type"),)

    user_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    item_id: Mapped[str] = mapped_column(String(255), default="", primary_key=True)
    item_type: Mapped[str] = mapped_column(String(255), default="", primary_key=True)
    play_count: Mapped[int] = mapped_column(Integer, default=0)
    # play_date: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    # rating: Mapped[int] = mapped_column(Integer, default=0)
    # starred: Mapped[bool] = mapped_column(Boolean, default=False)
    # starred_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    # rated_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
