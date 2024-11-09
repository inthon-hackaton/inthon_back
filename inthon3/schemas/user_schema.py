from pydantic import BaseModel
from typing import Optional

class UserInput(BaseModel):
    id: str
    pw: str
    email: str
    name: Optional[str] = None
    description: Optional[str] = None

class UserOutput(BaseModel):
    user_id: int
    id: str
    email: str
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True
