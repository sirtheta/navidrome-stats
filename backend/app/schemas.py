from pydantic import BaseModel



class UserOut(BaseModel):
    id: str
    user_name : str
    total_plays: int 