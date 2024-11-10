from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session, aliased
from config.database import get_db
from schemas.draft_schema import DraftOutput, DraftList, HomeDraft
# from services.draft_service import DraftService
from dotenv import load_dotenv
import os
import boto3
from models.leaf_models import Picture, Draft, LeafUser, Piece
from datetime import datetime 
import uuid
from io import BytesIO
from pydantic import BaseModel

load_dotenv()

# AWS 환경 변수
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = "leaf-bucket"

s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

router = APIRouter(
    prefix="/draft",
    tags=["draft"]
)

@router.get("/draft-list", response_model=List[HomeDraft])
async def get_draft_list(
    offset:int,
    limit:int,
    db: Session = Depends(get_db)
):
    
    draft_list = db.query(Draft).offset(offset).limit(limit).all()

    response_draft_list = []

    
    for draft in draft_list:
        image_info = db.query(Picture).filter(Picture.picture_id == draft.picture_id).first()
        draft_used_count = db.query(Piece).filter(Piece.picture_id == image_info.picture_id).count()
        example_user_picute_id_list = db.query(Piece).filter(Piece.picture_id == image_info.picture_id).limit(3).all()
        user_picture_id_list = [
            db.query(LeafUser).filter(LeafUser.user_id == example_user_picture_id[0]).first()
            for example_user_picture_id in example_user_picute_id_list
        ]

        draft_dict = {
            "draft_id": draft.draft_id,
            "description": draft.description,  
            "draft_link": image_info.picture_link, 
            "draft_used_count": draft_used_count,
            "draft_user_list": [
                db.query(Picture).filter(Picture.picture_id == user_picture_id.picture_id).first()
                for user_picture_id in user_picture_id_list if user_picture_id is not None
            ]
        }
        
        response_draft_list.append(draft_dict)
        print(response_draft_list)

    return response_draft_list

@router.post("/create", response_model=None)
async def create_draft(
    description: Optional[str],
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    id = uuid.uuid4()
    unique_filename = f"{id}_{file.filename}"
    s3_key = f"uploads/draft_pictures/{unique_filename}"
    try:
        # 파일을 S3로 업로드
        s3.upload_fileobj(file.file, S3_BUCKET_NAME, s3_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to upload file to S3")

    file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

    new_picture = Picture(picture_link = file_url, picture_id = id)
    db.add(new_picture)
    db.commit()
    db.refresh(new_picture)

    new_draft = Draft(draft_id = 1, user_id = 1, picture_id = id, description = description, created_at = datetime.now())
    db.add(new_draft)
    db.commit()
    db.refresh(new_draft)

    return {"status" : "success"}

# 응답 모델 정의
class PieceInfo(BaseModel):
    piece_id: int
    picture_link: str
    piece_number: int
    nickname: str
    profile_picture_link: Optional[str] = None

@router.get("/draft-piece-list", response_model=List[PieceInfo])
async def get_draft_piece_list(
    draft_id: int,
    db: Session = Depends(get_db)
):
    # 존재하는 draft_id인지 확인
    if not db.query(Piece).filter(Piece.draft_id == draft_id).first():
        raise HTTPException(status_code=404, detail="Draft not found")

    # Picture 테이블에 대한 별칭 생성
    PiecePicture = aliased(Picture)
    UserPicture = aliased(Picture)

    # 쿼리 작성
    pieces = (
        db.query(
            Piece.piece_id,
            Piece.piece_number,  # piece_number 추가
            PiecePicture.picture_link.label('piece_picture_link'),
            LeafUser.nickname,
            UserPicture.picture_link.label('user_picture_link')
        )
        .join(PiecePicture, Piece.picture_id == PiecePicture.picture_id)
        .join(LeafUser, Piece.user_id == LeafUser.user_id)
        .outerjoin(UserPicture, LeafUser.picture_id == UserPicture.picture_id)
        .filter(Piece.draft_id == draft_id)
        .all()
    )

    # 응답 데이터 구성
    result = [
        PieceInfo(
            piece_id=piece.piece_id,
            picture_link=piece.piece_picture_link,
            piece_number=piece.piece_number,
            nickname=piece.nickname,
            profile_picture_link=piece.user_picture_link
        )
        for piece in pieces
    ]

    return result
    