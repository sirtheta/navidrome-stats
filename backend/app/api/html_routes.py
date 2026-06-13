from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_babel import _
from sqlalchemy.orm import Session

from app.config import DB_PATH, USE_SAMPLE_DATA
from app.db import crud
from app.db.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.globals.update(_=_)
templates.env.globals["use_sample_data"] = USE_SAMPLE_DATA
templates.env.globals["db_path"] = DB_PATH


@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    users = crud.get_all_users(db=db)
    top_songs = crud.get_global_top_songs(db=db, limit=10)
    top_artists = crud.get_global_top_artists(db=db, limit=10)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "users": users,
            "top_songs": top_songs,
            "top_artists": top_artists,
        },
    )


@router.get("/user/{user_name}", response_class=HTMLResponse)
def user_detail(request: Request, user_name: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_name(db=db, user_name=user_name)
    if user is None:
        # TODO: define a 404 web page
        return JSONResponse(content={"message": _("user not found")}, status_code=404)
    songs = crud.get_top_songs(db=db, user_id=user.id)
    albums = crud.get_top_albums(db=db, user_id=user.id)
    artists = crud.get_top_artists(db=db, user_id=user.id)
    return templates.TemplateResponse(
        request=request,
        name="user.html",
        context={
            "user": user,
            "songs": songs,
            "albums": albums,
            "artists": artists,
        },
    )


@router.get("/compare", response_class=HTMLResponse)
def compare(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="compare.html",
    )
