from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.leaf_models import Completion, Includes, Piece, Picture
from config.database import get_db
from utils.authorize import get_current_user
from datetime import datetime
from typing import List
from pydantic import BaseModel
from schemas.completion_schema import CompletionCreateInput

router = APIRouter(
    prefix="/completion",
    tags=["completion"]
)

class PieceInfo(BaseModel):
    piece_id: int
    piece_number: int
    picture_link: str

class CompletionResponse(BaseModel):
    completion_id: int
    user_id: int
    created_at: datetime
    pieces: List[PieceInfo]

@router.post("/create", response_model=CompletionResponse)
async def create_completion(
    completion_data: CompletionCreateInput,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]

    new_completion = Completion(
        user_id=user_id,
        created_at=datetime.utcnow()
    )
    db.add(new_completion)
    db.commit()
    db.refresh(new_completion)

    pieces_info = []  # PieceInfo 객체들을 저장할 리스트

    for piece_id in completion_data.piece_ids:
        # 각 piece_id가 실제로 존재하는지 확인
        piece = db.query(Piece).filter_by(piece_id=piece_id).first()
        if not piece:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Piece with ID {piece_id} not found."
            )

        new_include = Includes(
            piece_id=piece_id,
            completion_id=new_completion.completion_id
        )
        db.add(new_include)

        # PieceInfo 객체 생성
        piece_picture = db.query(Picture).filter_by(picture_id=piece.picture_id).first()
        if not piece_picture:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Picture for Piece with ID {piece_id} not found."
            )

        piece_info = PieceInfo(
            piece_id=piece.piece_id,
            piece_number=piece.piece_number,
            picture_link=piece_picture.picture_link
        )
        pieces_info.append(piece_info)

    db.commit()

    return {
        "completion_id": new_completion.completion_id,
        "user_id": user_id,
        "created_at": new_completion.created_at,
        "pieces": pieces_info
    }

@router.get("/user-list", response_model=List[CompletionResponse])
async def get_user_completion_list(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]

    # 해당 유저의 completion 목록 조회
    completions = db.query(Completion).filter(Completion.user_id == user_id).all()

    # 각 completion에 포함된 piece 배열을 조회하여 반환 데이터 구성
    result = []
    for completion in completions:
        # completion에 포함된 piece를 piece_number 기준으로 정렬하여 조회
        pieces = (
            db.query(Piece.piece_id, Piece.piece_number, Picture.picture_link)
            .join(Includes, Includes.piece_id == Piece.piece_id)
            .join(Picture, Picture.picture_id == Piece.picture_id)
            .filter(Includes.completion_id == completion.completion_id)
            .order_by(Piece.piece_number)
            .all()
        )

        # pieces 배열에 각 piece 정보 추가
        piece_data = [
            {
                "piece_id": piece.piece_id,
                "piece_number": piece.piece_number,
                "picture_link": piece.picture_link,
            }
            for piece in pieces
        ]

        # 각 completion의 결과에 포함된 piece 배열 추가
        result.append({
            "completion_id": completion.completion_id,
            "created_at": completion.created_at,
            "pieces": piece_data,
        })

    return result