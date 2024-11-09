from pydantic import BaseModel
from typing import Optional

class PictureInput(BaseModel):
    picture_link: str

class PictureOutput(BaseModel):
    picture_id: int
    picture_link: str

    class Config:
        orm_mode = True
