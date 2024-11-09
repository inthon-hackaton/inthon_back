from pydantic import BaseModel

class CompletionInput(BaseModel):
    user_id: int
    picture_id: int

class CompletionOutput(BaseModel):
    completion_id: int
    user_id: int
    picture_id: int

    class Config:
        orm_mode = True
