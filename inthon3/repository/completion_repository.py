from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.leaf_models import Completion
from schemas.completion_schema import CompletionInput, CompletionOutput

class CompletionRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_completion(self, completion_id: int) -> Optional[CompletionOutput]:
        completion = self.db.query(Completion).filter(Completion.completion_id == completion_id).first()
        return CompletionOutput.from_orm(completion) if completion else None

    def create_completion(self, completion_data: CompletionInput) -> CompletionOutput:
        new_completion = Completion(**completion_data.dict())
        self.db.add(new_completion)
        self.db.commit()
        self.db.refresh(new_completion)
        return CompletionOutput.from_orm(new_completion)

    def delete_completion(self, completion_id: int) -> None:
        completion = self.get_completion(completion_id)
        if completion:
            self.db.delete(completion)
            self.db.commit()
