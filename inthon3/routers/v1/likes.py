from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from models.leaf_models import Likes, Piece
from config.database import get_db
from utils.authorize import get_current_user

router = APIRouter(
    prefix="/likes",
    tags=["likes"]
)

@router.post("/")
async def like_piece(
    piece_id: int = Query(..., description="ID of the piece to like"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]

    # 좋아요 중복 체크
    existing_like = db.query(Likes).filter_by(user_id=user_id, piece_id=piece_id).first()
    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already liked this piece."
        )

    # 해당 piece_id가 실제로 존재하는지 확인
    piece = db.query(Piece).filter_by(piece_id=piece_id).first()
    if not piece:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Piece not found."
        )

    # 새로운 좋아요 추가
    new_like = Likes(user_id=user_id, piece_id=piece_id)
    db.add(new_like)
    db.commit()

    return {"user_id": user_id, "piece_id": piece_id}
