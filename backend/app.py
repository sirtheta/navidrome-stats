from flask import Flask, render_template, jsonify, abort
from db import get_db, close_db
from config import USE_SAMPLE_DATA, DB_PATH, PORT, DEBUG
import queries

app = Flask(__name__)
app.teardown_appcontext(close_db)


@app.context_processor
def inject_globals():
    return {
        "use_sample_data": USE_SAMPLE_DATA,
        "db_path": DB_PATH,
    }


# ── HTML routes ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    db = get_db()
    users = queries.get_all_users(db)
    top_songs = queries.get_global_top_songs(db, limit=10)
    return render_template("index.html", users=users, top_songs=top_songs)


@app.route("/user/<user_name>")
def user_detail(user_name):
    db = get_db()
    user = queries.get_user_by_name(db, user_name)
    if not user:
        abort(404)
    songs = queries.get_top_songs(db, user["id"])
    albums = queries.get_top_albums(db, user["id"])
    artists = queries.get_top_artists(db, user["id"])
    return render_template(
        "user.html",
        user=user,
        songs=songs,
        albums=albums,
        artists=artists,
    )


@app.route("/compare")
def compare():
    return render_template("compare.html")


# ── JSON API ─────────────────────────────────────────────────────────────────

@app.route("/api/users")
def api_users():
    return jsonify(queries.get_all_users(get_db()))


@app.route("/api/user/<user_name>/top-songs")
def api_top_songs(user_name):
    db = get_db()
    user = queries.get_user_by_name(db, user_name)
    if not user:
        abort(404)
    return jsonify(queries.get_top_songs(db, user["id"]))


@app.route("/api/user/<user_name>/top-albums")
def api_top_albums(user_name):
    db = get_db()
    user = queries.get_user_by_name(db, user_name)
    if not user:
        abort(404)
    return jsonify(queries.get_top_albums(db, user["id"]))


@app.route("/api/user/<user_name>/top-artists")
def api_top_artists(user_name):
    db = get_db()
    user = queries.get_user_by_name(db, user_name)
    if not user:
        abort(404)
    return jsonify(queries.get_top_artists(db, user["id"]))


@app.route("/api/compare/songs")
def api_compare_songs():
    return jsonify(queries.get_cross_user_matrix(get_db()))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
