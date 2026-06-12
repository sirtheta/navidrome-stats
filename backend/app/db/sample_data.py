import random

from sqlalchemy.orm import Session
from sqlalchemy.sql import insert

from app.db.database import Base, SessionFactory, engine
from app.db.models import Album, Annotation, Artist, MediaFile, User


def init_sample_db() -> None:
    # create all tables
    Base.metadata.create_all(bind=engine)

    with SessionFactory() as db:
        init_sample_data(db=db)


def init_sample_data(db: Session) -> None:
    # insert sample data

    users = [
        ("u1", "alice"),
        ("u2", "bob"),
        ("u3", "charlie"),
    ]
    artists = [
        ("ar1", "Radiohead"),
        ("ar2", "Daft Punk"),
        ("ar3", "Portishead"),
        ("ar4", "Massive Attack"),
        ("ar5", "Björk"),
    ]
    albums = [
        ("al1", "OK Computer", "Radiohead", "ar1", 12),
        ("al2", "Kid A", "Radiohead", "ar1", 10),
        ("al3", "Discovery", "Daft Punk", "ar2", 14),
        ("al4", "Dummy", "Portishead", "ar3", 11),
        ("al5", "Mezzanine", "Massive Attack", "ar4", 11),
        ("al6", "Homogenic", "Björk", "ar5", 10),
        ("al7", "Homework", "Daft Punk", "ar2", 16),
        ("al8", "Dummy", "Portishead", "ar3", 9),
    ]
    tracks = [
        ("t01", "Karma Police", "Radiohead", "ar1", "OK Computer", "al1"),
        ("t02", "Paranoid Android", "Radiohead", "ar1", "OK Computer", "al1"),
        ("t03", "No Surprises", "Radiohead", "ar1", "OK Computer", "al1"),
        ("t04", "Everything in Its Right Place", "Radiohead", "ar1", "Kid A", "al2"),
        ("t05", "How to Disappear Completely", "Radiohead", "ar1", "Kid A", "al2"),
        ("t06", "Harder Better Faster Stronger", "Daft Punk", "ar2", "Discovery", "al3"),
        ("t07", "One More Time", "Daft Punk", "ar2", "Discovery", "al3"),
        ("t08", "Get Lucky", "Daft Punk", "ar2", "Discovery", "al3"),
        ("t09", "Da Funk", "Daft Punk", "ar2", "Homework", "al7"),
        ("t10", "Around the World", "Daft Punk", "ar2", "Homework", "al7"),
        ("t11", "Glory Box", "Portishead", "ar3", "Dummy", "al4"),
        ("t12", "Sour Times", "Portishead", "ar3", "Dummy", "al4"),
        ("t13", "Unfinished Sympathy", "Massive Attack", "ar4", "Mezzanine", "al5"),
        ("t14", "Teardrop", "Massive Attack", "ar4", "Mezzanine", "al5"),
        ("t15", "Angel", "Massive Attack", "ar4", "Mezzanine", "al5"),
        ("t16", "Joga", "Björk", "ar5", "Homogenic", "al6"),
        ("t17", "Bachelorette", "Björk", "ar5", "Homogenic", "al6"),
        ("t18", "All is Full of Love", "Björk", "ar5", "Homogenic", "al6"),
        ("t19", "Exit Music", "Radiohead", "ar1", "OK Computer", "al1"),
        ("t20", "Let Down", "Radiohead", "ar1", "OK Computer", "al1"),
    ]

    db.execute(insert(User).values(users))
    db.execute(insert(Artist).values(artists))
    db.execute(insert(Album).values(albums))
    db.execute(insert(MediaFile).values(tracks))

    # conn.executemany(
    #     "INSERT INTO media_file VALUES (?,?,?,?,?,?,?)",
    #     [(t[0], t[1], t[2], t[3], t[4], t[5], 240) for t in tracks],
    # )

    random.seed(42)
    annotations = []
    for user_id, _ in users:
        for track in tracks:
            count = random.randint(0, 30)
            if count > 0:
                annotations.append((user_id, track[0], "media_file", count))

    db.execute(insert(Annotation).values(annotations))

    # print(db.execute(select()).all())

    db.commit()
