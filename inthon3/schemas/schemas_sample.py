from pydantic import BaseModel
from typing import Optional, List, Literal

class User(BaseModel):
    user_id: int
    user_name: str