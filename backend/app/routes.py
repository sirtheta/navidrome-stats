from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.models import Annotation
from fastapi import Depends
from app.db import crud
from app.db.database import get_db
from app.schemas import UserOut

from fastapi import FastAPI

app = FastAPI()


# ── HTML routes ──────────────────────────────────────────────────────────────

# @app.get("/")
# def index():
#     db = get_db()
#     users = queries.get_all_users(db)
#     top_songs = queries.get_global_top_songs(db, limit=10)
#     return render_template("index.html", users=users, top_songs=top_songs)
#
#
# @app.get("/user/<user_name>")
# def user_detail(user_name):
#     db = get_db()
#     user = queries.get_user_by_name(db, user_name)
#     if not user:
#         abort(404)
#     songs = queries.get_top_songs(db, user["id"])
#     albums = queries.get_top_albums(db, user["id"])
#     artists = queries.get_top_artists(db, user["id"])
#     return render_template(
#         "user.html",
#         user=user,
#         songs=songs,
#         albums=albums,
#         artists=artists,
#     )
#
#
# @app.get("/compare")
# def compare():
#     return render_template("compare.html")
#

# ── JSON API ─────────────────────────────────────────────────────────────────

@app.post("/api/users", response_model=list[UserOut])
def api_users(db : Session =Depends(get_db)):
    users = crud.get_all_users(db=db)
    return users


# @app.post("/api/user/{user_name}/top-songs")
# def api_top_songs(user_id : str,db : Session =Depends(get_db)):
#     user = queries.get_user_by_name(db, user_name)
#     if not user:
#         abort(404)
#     return jsonify(queries.get_top_songs(db, user["id"]))


# @app.post("/api/user/<user_name>/top-albums")
# def api_top_albums(user_name):
#     db = get_db()
#     user = queries.get_user_by_name(db, user_name)
#     if not user:
#         abort(404)
#     return jsonify(queries.get_top_albums(db, user["id"]))


# @app.post("/api/user/<user_name>/top-artists")
# def api_top_artists(user_name):
#     db = get_db()
#     user = queries.get_user_by_name(db, user_name)
#     if not user:
#         abort(404)
#     return jsonify(queries.get_top_artists(db, user["id"]))


# @app.post("/api/compare/songs")
# def api_compare_songs():
#     return jsonify(queries.get_cross_user_matrix(get_db()))

