import sqlite3
import random


def build_sample_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    _create_schema(conn)
    _seed(conn)
    return conn


def _create_schema(conn):
    conn.executescript("""
        CREATE TABLE users (
            id TEXT PRIMARY KEY,
            user_name TEXT NOT NULL
        );
        CREATE TABLE artist (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        );
        CREATE TABLE album (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            artist TEXT NOT NULL,
            artist_id TEXT NOT NULL,
            song_count INTEGER DEFAULT 0
        );
        CREATE TABLE media_file (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            artist_id TEXT NOT NULL,
            album TEXT NOT NULL,
            album_id TEXT NOT NULL,
            duration INTEGER DEFAULT 0
        );
        CREATE TABLE annotation (
            item_type TEXT NOT NULL,
            item_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            play_count INTEGER,
            PRIMARY KEY (item_type, item_id, user_id)
        );
    """)


def _seed(conn):
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

    conn.executemany("INSERT INTO users VALUES (?,?)", users)
    conn.executemany("INSERT INTO artist VALUES (?,?)", artists)
    conn.executemany("INSERT INTO album VALUES (?,?,?,?,?)", albums)
    conn.executemany("INSERT INTO media_file VALUES (?,?,?,?,?,?,?)",
                     [(t[0], t[1], t[2], t[3], t[4], t[5], 240) for t in tracks])

    random.seed(42)
    annotations = []
    for user_id, _ in users:
        for track in tracks:
            count = random.randint(0, 30)
            if count > 0:
                annotations.append(("media_file", track[0], user_id, count))

    conn.executemany("INSERT INTO annotation VALUES (?,?,?,?)", annotations)
    conn.commit()
