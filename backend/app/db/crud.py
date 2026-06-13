from typing import Any

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.db.models import Annotation, Artist, MediaFile, User
from app.schemas import TopAlbum, TopArtist, TopSong, UserOut


def get_all_users(db: Session) -> list[UserOut]:
    query = (
        select(
            User.id,
            User.user_name,
            func.coalesce(func.sum(Annotation.play_count), 0).label("total_plays"),
        )
        .join(Annotation, Annotation.user_id == User.id)
        .where(Annotation.item_type == "media_file", Annotation.play_count > 0)
        .group_by(User.id)
        .order_by(desc("total_plays"))
    )

    results = db.execute(query).all()
    users = [
        UserOut(
            id=r._tuple()[0],
            user_name=r._tuple()[1],
            total_plays=r._tuple()[2],
        )
        for r in results
    ]
    return users


def get_user_by_name(db: Session, user_name: str) -> User | None:
    query = select(User).where(User.user_name == user_name)
    result = db.scalar(query)
    return result


def get_top_songs(db: Session, user_id: str, limit: int = 10) -> list[TopSong]:
    query = (
        select(
            MediaFile.title,
            MediaFile.artist,
            func.coalesce(Annotation.play_count, 0).label("play_count"),
        )
        .join(MediaFile, MediaFile.id == Annotation.item_id)
        .where(
            Annotation.item_type == "media_file",
            Annotation.user_id == user_id,
            Annotation.play_count > 0,
        )
        .order_by(desc(Annotation.play_count))
        .limit(limit)
    )

    results = db.execute(query).all()
    return [
        TopSong(title=r._tuple()[0], artist=r._tuple()[1], play_count=r._tuple()[2])
        for r in results
    ]


def get_top_albums(db: Session, user_id: str, limit: int = 10) -> list[TopAlbum]:
    query = (
        select(
            MediaFile.album.label("name"),
            MediaFile.artist,
            func.sum(func.coalesce(Annotation.play_count, 0)).label("play_count"),
        )
        .join(MediaFile, MediaFile.id == Annotation.item_id)
        .where(
            Annotation.item_type == "media_file",
            Annotation.user_id == user_id,
            Annotation.play_count > 0,
        )
        .group_by(MediaFile.album_id)
        .order_by(desc("play_count"))
        .limit(limit)
    )

    results = db.execute(query).all()
    return [
        TopAlbum(name=r._tuple()[0], artist=r._tuple()[1], play_count=r._tuple()[2])
        for r in results
    ]


def get_top_artists(db: Session, user_id: str, limit: int = 10) -> list[TopArtist]:
    query = (
        select(
            MediaFile.artist.label("name"),
            func.sum(func.coalesce(Annotation.play_count, 0)).label("play_count"),
        )
        .join(MediaFile, MediaFile.id == Annotation.item_id)
        .where(
            Annotation.item_type == "media_file",
            Annotation.user_id == user_id,
            Annotation.play_count > 0,
        )
        .group_by(MediaFile.artist_id)
        .order_by(desc("play_count"))
        .limit(limit)
    )

    results = db.execute(query).all()
    return [TopArtist(name=r._tuple()[0], play_count=r._tuple()[1]) for r in results]


def get_global_top_songs(db: Session, limit: int = 10) -> list[TopSong]:
    query = (
        select(
            MediaFile.title,
            MediaFile.artist,
            func.sum(func.coalesce(Annotation.play_count, 0)).label("play_count"),
        )
        .join(MediaFile, MediaFile.id == Annotation.item_id)
        .where(
            Annotation.item_type == "media_file",
            Annotation.play_count > 0,
        )
        .group_by(MediaFile.id)
        .order_by(desc("play_count"))
        .limit(limit)
    )

    results = db.execute(query).all()
    return [
        TopSong(title=r._tuple()[0], artist=r._tuple()[1], play_count=r._tuple()[2])
        for r in results
    ]


def get_global_top_artists(db: Session, limit: int = 10) -> list[TopArtist]:
    query = (
        select(
            Artist.name,
            func.sum(func.coalesce(Annotation.play_count, 0)).label("play_count"),
        )
        .join(MediaFile, MediaFile.id == Annotation.item_id)
        .join(Artist, Artist.id == MediaFile.artist_id)
        .where(
            Annotation.item_type == "media_file",
            Annotation.play_count > 0,
        )
        .group_by(MediaFile.artist)
        .order_by(desc("play_count"))
        .limit(limit)
    )

    results = db.execute(query).all()
    return [TopArtist(name=r._tuple()[0], play_count=r._tuple()[1]) for r in results]


def get_cross_user_matrix(db: Session, limit: int = 20) -> dict[str, Any]:
    # 1. Get Users
    users_query = select(User.id, User.user_name).order_by(User.user_name)
    users = [
        {"id": r._tuple()[0], "user_name": r._tuple()[1]}
        for r in db.execute(users_query).all()
    ]

    # 2. Get Top Songs
    songs_query = (
        select(
            MediaFile.id,
            MediaFile.title,
            MediaFile.artist,
            func.sum(func.coalesce(Annotation.play_count, 0)).label("total"),
        )
        .join(MediaFile, MediaFile.id == Annotation.item_id)
        .where(
            Annotation.item_type == "media_file",
            Annotation.play_count > 0,
        )
        .group_by(MediaFile.id)
        .order_by(desc("total"))
        .limit(limit)
    )
    top_songs = [
        {"id": r._tuple()[0], "title": r._tuple()[1], "artist": r._tuple()[2]}
        for r in db.execute(songs_query).all()
    ]

    if not top_songs:
        return {"songs": [], "users": [], "matrix": []}

    song_ids = [s["id"] for s in top_songs]

    # 3. Get Plays for matrix
    plays_query = select(
        Annotation.item_id, Annotation.user_id, Annotation.play_count
    ).where(
        Annotation.item_type == "media_file",
        Annotation.item_id.in_(song_ids),
    )
    plays_results = db.execute(plays_query).all()

    lookup = {}
    for p in plays_results:
        lookup[(p._tuple()[0], p._tuple()[1])] = p._tuple()[2] or 0

    matrix = []
    for user in users:
        row = [lookup.get((sid, user["id"]), 0) for sid in song_ids]
        matrix.append(row)

    return {
        "songs": [f"{s['title']} — {s['artist']}" for s in top_songs],
        "users": [u["user_name"] for u in users],
        "matrix": matrix,
    }
