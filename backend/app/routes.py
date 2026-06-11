from app.schemas import TopArtist
from app.schemas import TopAlbum
from app.schemas import TopSong
from fastapi.responses import JSONResponse
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.db import crud
from app.db.database import get_db
from app.schemas import UserOut

app = FastAPI()


# ── HTML routes ──────────────────────────────────────────────────────────────

# @app.get("/")
# def index():
#     db = get_db()
#     users = crud.get_all_users(db)
#     top_songs = crud.get_global_top_songs(db, limit=10)
#     return render_template("index.html", users=users, top_songs=top_songs)
#
#
# @app.get("/user/<user_name>")
# def user_detail(user_name):
#     db = get_db()
#     user = crud.get_user_by_name(db, user_name)
#     if not user:
#         abort(404)
#     songs = crud.get_top_songs(db, user["id"])
#     albums = crud.get_top_albums(db, user["id"])
#     artists = crud.get_top_artists(db, user["id"])
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
def api_users(db: Session = Depends(get_db)):
    users = crud.get_all_users(db=db)
    return users


@app.post("/api/user/{user_name}/top-songs", response_model=list[TopSong])
def api_top_songs(user_name : str,db : Session =Depends(get_db)):
    user = crud.get_user_by_name(db=db, user_name=user_name)
    if user is None:
        return JSONResponse(content={"message":"user not found"}, status_code=404)
    
    return crud.get_top_songs(db=db, user_id=user.id)


@app.post("/api/user/{user_name}/top-albums", response_model=list[TopAlbum])
def api_top_albums(user_name : str,db : Session =Depends(get_db)):
    user = crud.get_user_by_name(db=db, user_name=user_name)
    if user is None:
        return JSONResponse(content={"message":"user not found"}, status_code=404)
    return crud.get_top_albums(db=db, user_id=user.id)


@app.post("/api/user/{user_name}/top-artists", response_model=list[TopArtist])
def api_top_artists(user_name : str,db : Session =Depends(get_db)):
    user = crud.get_user_by_name(db=db, user_name=user_name)
    if user is None:
        return JSONResponse(content={"message":"user not found"}, status_code=404)
    return crud.get_top_artists(db=db, user_id=user.id)


@app.post("/api/compare/songs")
def api_compare_songs(db : Session =Depends(get_db)):
    return crud.get_cross_user_matrix(db=db)
