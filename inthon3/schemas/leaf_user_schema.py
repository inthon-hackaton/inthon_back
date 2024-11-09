from pydantic import BaseModel

class LeafUserInput(BaseModel):
    nickname: str

class LeafUserOutput(BaseModel):
    user_id: int
    nickname: str

    class Config:
        orm_mode = True
