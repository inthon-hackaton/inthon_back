from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.leaf_models import Draft
from schemas.draft_schema import DraftInput, DraftOutput

class DraftRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_draft(self, draft_id: int) -> Optional[DraftOutput]:
        draft = self.db.query(Draft).filter(Draft.draft_id == draft_id).first()
        return DraftOutput.from_orm(draft) if draft else None

    def create_draft(self, draft_data: DraftInput) -> DraftOutput:
        new_draft = Draft(**draft_data.dict())
        self.db.add(new_draft)
        self.db.commit()
        self.db.refresh(new_draft)
        return DraftOutput.from_orm(new_draft)

    def delete_draft(self, draft_id: int) -> None:
        draft = self.get_draft(draft_id)
        if draft:
            self.db.delete(draft)
            self.db.commit()
