from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.leaf_models import User
from schemas.user_schema import UserInput, UserOutput

class UserRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_user(self, user_id: int) -> Optional[UserOutput]:
        user = self.db.query(User).filter(User.user_id == user_id).first()
        return UserOutput.from_orm(user) if user else None

    def create_user(self, user_data: UserInput) -> UserOutput:
        new_user = User(**user_data.dict())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return UserOutput.from_orm(new_user)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
