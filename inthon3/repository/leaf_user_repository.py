from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.leaf_models import Leaf_User
from schemas.leaf_user_schema import LeafUserInput, LeafUserOutput

class LeafUserRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_leaf_user(self, user_id: int) -> Optional[LeafUserOutput]:
        leaf_user = self.db.query(Leaf_User).filter(Leaf_User.user_id == user_id).first()
        return LeafUserOutput.from_orm(leaf_user) if leaf_user else None

    def create_leaf_user(self, leaf_user_data: LeafUserInput) -> LeafUserOutput:
        new_leaf_user = Leaf_User(**leaf_user_data.dict())
        self.db.add(new_leaf_user)
        self.db.commit()
        self.db.refresh(new_leaf_user)
        return LeafUserOutput.from_orm(new_leaf_user)

    def delete_leaf_user(self, user_id: int) -> None:
        leaf_user = self.get_leaf_user(user_id)
        if leaf_user:
            self.db.delete(leaf_user)
            self.db.commit()
