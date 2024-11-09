from pydantic import BaseModel
from typing import Optional

class PictureInput(BaseModel):
    picture_id: str
    picture_link: str

    class Config:
        orm_mode = True 

class PictureOutput(BaseModel):
    picture_id: str
    picture_link: str

    class Config:
        from_attributes = True
