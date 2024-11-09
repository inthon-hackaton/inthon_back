from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from config.database import get_db
from schemas.draft_schema import DraftOutput, DraftList
# from services.draft_service import DraftService
from dotenv import load_dotenv
import os
import boto3
from models.leaf_models import Picture, Draft, LeafUser
from datetime import datetime 
import uuid
from io import BytesIO


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

# @router.get("/draft-list", response_model=DraftList)
# async def get_draft_list(
#     offset:int,
#     limit:int,
#     db: Session = Depends(get_db)
# ):
#     return await service.get_draft_list(offset=offset, limit=limit)

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