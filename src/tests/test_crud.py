from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import crud
from app.db.database import Base
from app.db.models import User
from app.db.sample_data import init_sample_data
from app.schemas import TopAlbum, TopArtist, TopSong, UserOut


def test_get_all_users_returns_sorted_play_counts(db_session):
    users = crud.get_all_users(db_session)

    assert len(users) == 3
    assert all(isinstance(user, UserOut) for user in users)
    assert users[0].user_name == "bob"
    assert users[0].total_plays == 288
    assert users[1].user_name == "charlie"
    assert users[2].user_name == "alice"
    assert users[0].total_plays >= users[1].total_plays >= users[2].total_plays


def test_get_all_users_excludes_users_without_plays():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    with session_factory() as session:
        init_sample_data(db=session)
        session.add(User(id="u0", user_name="inactive"))
        session.commit()

        user_names = {user.user_name for user in crud.get_all_users(session)}

        assert "inactive" not in user_names


def test_get_user_by_name_found(db_session):
    user = crud.get_user_by_name(db_session, "alice")

    assert user is not None
    assert user.id == "u1"
    assert user.user_name == "alice"


def test_get_user_by_name_not_found(db_session):
    assert crud.get_user_by_name(db_session, "missing") is None


def test_get_top_songs_for_user(db_session):
    songs = crud.get_top_songs(db_session, user_id="u1")

    assert len(songs) == 10
    assert all(isinstance(song, TopSong) for song in songs)
    assert songs[0].title == "Unfinished Sympathy"
    assert songs[0].artist == "Massive Attack"
    assert songs[0].play_count == 28
    assert songs[0].play_count >= songs[1].play_count


def test_get_top_songs_respects_limit(db_session):
    songs = crud.get_top_songs(db_session, user_id="u1", limit=3)

    assert len(songs) == 3


def test_get_top_songs_unknown_user_returns_empty(db_session):
    assert crud.get_top_songs(db_session, user_id="missing") == []


def test_get_top_albums_for_user(db_session):
    albums = crud.get_top_albums(db_session, user_id="u1")

    assert len(albums) == 7
    assert all(isinstance(album, TopAlbum) for album in albums)
    assert albums[0].name == "Mezzanine"
    assert albums[0].artist == "Massive Attack"
    assert albums[0].play_count == 47
    assert albums[0].play_count >= albums[1].play_count


def test_get_top_albums_sums_track_plays_per_album(db_session):
    albums = crud.get_top_albums(db_session, user_id="u1")
    mezzanine = next(album for album in albums if album.name == "Mezzanine")

    assert mezzanine.play_count == 47
    assert mezzanine.artist == "Massive Attack"


def test_get_top_artists_for_user(db_session):
    artists = crud.get_top_artists(db_session, user_id="u1")

    assert len(artists) == 5
    assert all(isinstance(artist, TopArtist) for artist in artists)
    assert artists[0].name == "Radiohead"
    assert artists[0].play_count == 56
    assert artists[0].play_count >= artists[1].play_count


def test_get_global_top_songs(db_session):
    songs = crud.get_global_top_songs(db_session, limit=5)

    assert len(songs) == 5
    assert songs[0].title == "Da Funk"
    assert songs[0].artist == "Daft Punk"
    assert songs[0].play_count == 73
    assert songs[0].play_count >= songs[1].play_count


def test_get_global_top_artists(db_session):
    artists = crud.get_global_top_artists(db_session, limit=5)

    assert len(artists) == 5
    assert artists[0].name == "Radiohead"
    assert artists[0].play_count == 230
    assert artists[0].play_count >= artists[1].play_count


def test_get_cross_user_matrix(db_session):
    matrix = crud.get_cross_user_matrix(db_session, limit=3)

    assert matrix["users"] == ["alice", "bob", "charlie"]
    assert matrix["songs"] == [
        "Da Funk — Daft Punk",
        "Bachelorette — Björk",
        "Everything in Its Right Place — Radiohead",
    ]
    assert matrix["matrix"] == [
        [23, 13, 23],
        [20, 25, 19],
        [30, 27, 13],
    ]


def test_get_cross_user_matrix_respects_limit(db_session):
    matrix = crud.get_cross_user_matrix(db_session, limit=5)

    assert len(matrix["songs"]) == 5
    assert len(matrix["matrix"]) == 3
    assert all(len(row) == 5 for row in matrix["matrix"])


def test_get_cross_user_matrix_empty_database():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    with session_factory() as session:
        assert crud.get_cross_user_matrix(session) == {
            "songs": [],
            "users": [],
            "matrix": [],
        }
