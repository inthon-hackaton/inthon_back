from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from models.leaf_models import LeafUser, Picture
from config.database import get_db
from utils.authorize import get_current_user
import uuid
import boto3
import os
from typing import Optional
from pydantic import BaseModel

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

@router.post("/create-info")
async def create_user_info(
    nickname: Optional[str] = Query(None, description="New nickname for the user"),
    description: Optional[str] = Query(None, description="New description for the user"),
    profile_picture: Optional[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]
    
    user = db.query(LeafUser).filter(LeafUser.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if nickname:
        user.nickname = nickname
    else:
        raise HTTPException(status_code=400, detail="Nickname is required, but missing")

    if description:
        user.description = description

    # 프로필 사진 업데이트 (S3에 업로드)
    if profile_picture:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        _uuid = str(uuid.uuid4())
        unique_filename = f"{_uuid}_{profile_picture.filename}"
        s3_key = f"profile_pictures/{unique_filename}"

        try:
            s3.upload_fileobj(profile_picture.file, S3_BUCKET_NAME, s3_key)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload file to S3: {str(e)}")

        file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

        new_picture = Picture(picture_link=file_url, picture_id=_uuid)
        db.add(new_picture)
        db.commit()
        db.refresh(new_picture)

        # 사용자 프로필 사진 업데이트
        user.picture_id = new_picture.picture_id

    db.commit()

    return {
        "nickname": user.nickname,
        "description": user.description,
        "picture_url": file_url if profile_picture else None
    }

@router.post("/update-info")
async def update_user_info(
    nickname: Optional[str] = Query(None, description="New nickname for the user"),
    description: Optional[str] = Query(None, description="New description for the user"),
    profile_picture: Optional[UploadFile] = File(None, description="New profile picture"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]

    # 사용자 조회
    user = db.query(LeafUser).filter(LeafUser.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 닉네임 업데이트 (닉네임이 제공된 경우에만)
    if nickname:
        user.nickname = nickname

    # 자기소개 업데이트 (자기소개가 제공된 경우에만)
    if description:
        user.description = description

    # 프로필 사진 업데이트 (profile_picture가 제공된 경우에만)
    file_url = None
    if profile_picture:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        _uuid = str(uuid.uuid4())
        unique_filename = f"{_uuid}_{profile_picture.filename}"
        s3_key = f"profile_pictures/{unique_filename}"

        try:
            s3.upload_fileobj(profile_picture.file, S3_BUCKET_NAME, s3_key)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload file to S3: {str(e)}")

        file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

        # Picture 테이블에 새로운 프로필 사진 추가
        new_picture = Picture(picture_link=file_url, picture_id=_uuid)
        db.add(new_picture)
        db.commit()
        db.refresh(new_picture)

        # 사용자 프로필 사진 업데이트
        user.picture_id = new_picture.picture_id

    # DB에 변경 사항 커밋
    db.commit()

    return {
        "nickname": user.nickname,
        "description": user.description,
        "picture_url": file_url if profile_picture else None
    }

class UserInfoResponse(BaseModel):
    user_id: int
    nickname: str
    description: Optional[str] = None
    picture_url: Optional[str] = None

@router.get("/get-info", response_model=UserInfoResponse)
async def get_user_info(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]

    # 현재 사용자 정보 조회
    user = db.query(LeafUser).filter(LeafUser.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 프로필 사진 URL 가져오기
    picture_url = None
    if user.picture_id:
        picture = db.query(Picture).filter(Picture.picture_id == user.picture_id).first()
        if picture:
            picture_url = picture.picture_link

    return {
        "user_id": user.user_id,
        "nickname": user.nickname,
        "description": user.description,
        "picture_url": picture_url
    }