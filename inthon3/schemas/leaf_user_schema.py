from pydantic import BaseModel
from typing import Optional, List, ClassVar

class LeafUserInput(BaseModel):
    nickname: str

class LeafUserOutput(BaseModel):
    user_id: int
    nickname: str

    class Config:
        orm_mode = True

class DraftLeafUser(BaseModel):
    user_image_list: List[str]