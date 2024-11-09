from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PieceInput(BaseModel):
    user_id: int
    draft_id: int
    piece_number: int
    picture_id: int
    description: Optional[str] = None

    class Config:
        orm_mode = True 

class PieceOutput(BaseModel):
    piece_id: int
    user_id: int
    draft_id: int
    piece_number: int
    picture_id: int
    description: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
