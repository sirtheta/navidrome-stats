from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi_babel import _
from sqlalchemy.orm import Session

from app.db import crud
from app.db.database import get_db
from app.schemas import TopAlbum, TopArtist, TopSong, UserOut

router = APIRouter()


# global endpoints


@router.get("/users", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = crud.get_all_users(db=db)
    return users


@router.get("/top-songs", response_model=list[TopSong])
def get_top_songs(limit: int = 10, db: Session = Depends(get_db)) -> list[TopSong]:
    """Get Global Top Songs"""
    top_songs = crud.get_global_top_songs(db=db, limit=limit)
    return top_songs


@router.get("/top-artists", response_model=list[TopArtist])
def get_top_artists(limit: int = 10, db: Session = Depends(get_db)) -> list[TopArtist]:
    """Get Global Top Artists"""
    top_artists = crud.get_global_top_artists(db=db, limit=limit)
    return top_artists


@router.get("/compare/songs")
def get_compare_songs(db: Session = Depends(get_db)):
    return crud.get_cross_user_matrix(db=db)


# user specific endpoints


@router.get("/user/{user_name}/top-songs", response_model=list[TopSong])
def get_user_top_songs(user_name: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_name(db=db, user_name=user_name)
    if user is None:
        return JSONResponse(content={"message": _("user not found")}, status_code=404)

    return crud.get_top_songs(db=db, user_id=user.id)


@router.get("/user/{user_name}/top-albums", response_model=list[TopAlbum])
def get_user_top_albums(user_name: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_name(db=db, user_name=user_name)
    if user is None:
        return JSONResponse(content={"message": _("user not found")}, status_code=404)
    return crud.get_top_albums(db=db, user_id=user.id)


@router.get("/user/{user_name}/top-artists", response_model=list[TopArtist])
def get_user_top_artists(user_name: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_name(db=db, user_name=user_name)
    if user is None:
        return JSONResponse(content={"message": _("user not found")}, status_code=404)
    return crud.get_top_artists(db=db, user_id=user.id)
