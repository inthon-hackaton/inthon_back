from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.leaf_models import Piece
from schemas.piece_schema import PieceInput, PieceOutput

class PieceRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_piece(self, piece_id: int) -> Optional[PieceOutput]:
        piece = self.db.query(Piece).filter(Piece.piece_id == piece_id).first()
        return PieceOutput.from_orm(piece) if piece else None

    def create_piece(self, piece_data: PieceInput) -> PieceOutput:
        new_piece = Piece(**piece_data.dict())
        self.db.add(new_piece)
        self.db.commit()
        self.db.refresh(new_piece)
        return PieceOutput.from_orm(new_piece)

    def delete_piece(self, piece_id: int) -> None:
        piece = self.get_piece(piece_id)
        if piece:
            self.db.delete(piece)
            self.db.commit()
