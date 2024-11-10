from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.leaf_models import Piece, Picture, Likes, Includes
from config.database import get_db
from schemas.piece_schema import PieceInput, PieceOutput
from utils.authorize import get_current_user
import uuid
import boto3
import os
from typing import Optional

router = APIRouter(
    prefix="/piece",
    tags=["piece"]
)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

@router.post("/create", response_model=PieceOutput)
async def create_piece(
    piece_number: int,
    description: Optional[str] | None,
    draft_id: int,
    picture: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]

    # S3에 파일 업로드
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    _uuid = str(uuid.uuid4())  # UUID를 문자열로 변환
    unique_filename = f"{_uuid}_{picture.filename}"
    s3_key = f"uploads/pictures/{unique_filename}"

    try:
        s3.upload_fileobj(picture.file, S3_BUCKET_NAME, s3_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file to S3: {str(e)}")

    file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

    # 새로운 Picture 객체 생성 및 저장
    new_picture = Picture(picture_link=file_url, picture_id=_uuid)
    db.add(new_picture)
    db.commit()
    db.refresh(new_picture)

    # 새로운 Piece 객체 생성 및 저장
    new_piece = Piece(
        piece_number=piece_number,
        description=description,
        draft_id=draft_id,
        user_id=user_id,
        picture_id=_uuid
    )

    db.add(new_piece)
    db.commit()
    db.refresh(new_piece)

    return {
        "piece_id": new_piece.piece_id,
        "piece_number": new_piece.piece_number,
        "description": new_piece.description,
        "picture_link": new_picture.picture_link
    }


@router.get("/user-stats")
async def get_user_stats(
    db: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user)
):
    user_id = 9 # current_user["user_id"]
    
    # 1. 현재 사용자가 업로드한 총 piece 개수
    total_pieces = db.query(func.count(Piece.piece_id)).filter(Piece.user_id == user_id).scalar()

    # 2. 사용자의 piece들이 받은 총 좋아요 개수
    total_likes = (
        db.query(func.count(Likes.piece_id))
        .join(Piece, Piece.piece_id == Likes.piece_id)
        .filter(Piece.user_id == user_id)
        .scalar()
    )

    # 3. 사용자의 piece들이 완성품에 포함된 총 횟수
    total_includes = (
        db.query(func.count(Includes.piece_id))
        .join(Piece, Piece.piece_id == Includes.piece_id)
        .filter(Piece.user_id == user_id)
        .scalar()
    )

    return {
        "total_pieces": total_pieces,
        "total_likes": total_likes,
        "total_includes": total_includes
    }