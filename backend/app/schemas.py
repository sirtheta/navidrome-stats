from pydantic import BaseModel


class UserOut(BaseModel):
    id: str
    user_name: str
    total_plays: int


class TopSong(BaseModel):
    title: str
    artist: str
    play_count: int


class TopAlbum(BaseModel):
    name: str
    artist: str
    play_count: int


class TopArtist(BaseModel):
    name: str
    play_count: int
