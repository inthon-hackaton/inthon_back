from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.leaf_models import Draft, Picture, Likes, Piece, User
from schemas.draft_schema import DraftInput, DraftOutput, DraftList, HomeDraft

class DraftRepository:
    def __init__(self, db: Session = get_db) -> None:
        self.db = db

    def get_draft(self, draft_id: int) -> Optional[DraftOutput]:
        draft = self.db.query(Draft).filter(Draft.draft_id == draft_id).first()
        return DraftOutput.from_orm(draft) if draft else None

    def create_draft(self, draft_id: int, user_id: int, picture_id: str, description: str, created_at: str):
        new_draft = Draft(draft_id = draft_id, user_id = user_id, picture_id = picture_id, description = description, created_at = created_at)
        self.db.add(new_draft)
        self.db.commit()
        self.db.refresh(new_draft)
        return DraftOutput.from_orm(new_draft)

    def delete_draft(self, draft_id: int) -> None:
        draft = self.get_draft(draft_id)
        if draft:
            self.db.delete(draft)
            self.db.commit()
            
    async def get_draft_list(self, offset: int, limit: int) -> HomeDraft:
        draft_list = self.db.query(Draft.draft_id, Draft.description, Draft.picture_id).offset(offset).limit(limit).all()

        response_draft_list = []

        
        for draft in draft_list:
            image_info = self.db.query(Picture.picture_link, Picture.picture_id).filter(Picture.picture_id == draft.picture_id).first()
            draft_used_count = self.db.query(Piece.piece_id).filter(Piece.draft_id == image_info.draft_id).count()
            example_user_picute_id_list = self.db.query(Piece.user_id).filter(Piece.draft_id == image_info.draft_id).limit(3).all()
            user_picture_id_list = [
                self.db.query(User.picture_id).filter(User.user_id == example_user_picture_id[0]).first()
                for example_user_picture_id in example_user_picute_id_list
            ]

            draft_dict = {
                "draft_id": draft.draft_id,
                "description": draft.description,  
                "draft_link": image_info.picture_link, 
                "draft_used_count": draft_used_count,
                "draft_user_list": [
                    self.db.query(Picture.picture_link).filter(Picture.picture_id == user_picture_id.picture_id).first()
                    for user_picture_id in user_picture_id_list if user_picture_id is not None
                ]
            }
            
            response_draft_list.append(draft_dict)
            print(response_draft_list)

        return response_draft_list
    