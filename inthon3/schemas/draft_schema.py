from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .leaf_user_schema import DraftLeafUser

class DraftInput(BaseModel):
    user_id: int
    picture_id: int
    description: Optional[str] = None
    class Config:
        orm_mode = True 

class DraftOutput(BaseModel):
    draft_id: int
    user_id: int
    picture_id: int
    description: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

class HomeDraft(BaseModel):
    draft_link: str
    draft_user_list: List[Optional[DraftLeafUser]]
    description : Optional[str]
    draft_used_count: int
    draft_id: int
    class Config:
        orm_mode = True 


class DraftList(BaseModel):
    draft_list : List[HomeDraft]

    class Config:
        orm_mode = True 