from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PieceInput(BaseModel):
    piece_number: int
    description: str
    draft_id: int

    class Config:
        orm_mode = True 

class PieceOutput(BaseModel):
    piece_id: int
    draft_id: int
    piece_number: int
    picture_id: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
