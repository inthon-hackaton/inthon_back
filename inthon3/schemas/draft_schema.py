from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DraftInput(BaseModel):
    user_id: int
    picture_id: int
    description: Optional[str] = None

class DraftOutput(BaseModel):
    draft_id: int
    user_id: int
    picture_id: int
    description: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
