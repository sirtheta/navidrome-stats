import sqlite3
import flask
from config import DB_PATH, USE_SAMPLE_DATA


def get_db():
    if "db" not in flask.g:
        if USE_SAMPLE_DATA:
            from sample_data import build_sample_db
            flask.g.db = build_sample_db()
        else:
            flask.g.db = sqlite3.connect(
                f"file:{DB_PATH}?mode=ro",
                uri=True,
                timeout=5,
                check_same_thread=False,
            )
            flask.g.db.row_factory = sqlite3.Row
    return flask.g.db


def close_db(e=None):
    db = flask.g.pop("db", None)
    if db is not None and not USE_SAMPLE_DATA:
        db.close()
