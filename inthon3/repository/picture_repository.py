from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.leaf_models import Picture
from schemas.picture_schema import PictureInput, PictureOutput

class PictureRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_picture(self, picture_id: int) -> Optional[PictureOutput]:
        picture = self.db.query(Picture).filter(Picture.picture_id == picture_id).first()
        return PictureOutput.from_orm(picture) if picture else None

    def create_picture(self, picture_link: str) -> PictureOutput:
        new_picture = Picture(picture_link=picture_link)
        self.db.add(new_picture)
        self.db.commit()
        self.db.refresh(new_picture)
        return PictureOutput.from_orm(new_picture)

    def delete_picture(self, picture_id: int) -> None:
        picture = self.get_picture(picture_id)
        if picture:
            self.db.delete(picture)
            self.db.commit()
