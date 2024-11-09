from fastapi import Depends, HTTPException, Response, UploadFile
from repository.draft_repository import DraftRepository
from repository.picture_repository import PictureRepository
import uuid
from schemas.draft_schema import DraftInput, DraftOutput, DraftList, HomeDraft
from dotenv import load_dotenv
import os
import boto3
from models.leaf_models import Picture, Draft
from datetime import datetime 


load_dotenv()

# AWS 환경 변수
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = "leaf-bucket"


class DraftService():
    def __init__(self, repository: DraftRepository = Depends()) -> None:
        self.repository = repository
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
    async def get_draft_list(self, offset: int, limit: int):
        return await self.repository.get_draft_list(offset=offset, limit=limit)
        
    async def upload_draft(self, description: str, file: UploadFile):
        id = uuid.uuid4()
        unique_filename = f"{id}_{file.filename}"
        s3_key = f"uploads/draft_pictures/{unique_filename}"
        try:
            self.s3.upload_fileobj(file.file, S3_BUCKET_NAME, s3_key)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to upload file to S3")


        file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
    
        PictureRepository().create_picture(picture_link=file_url, picture_id = id)
        print("image_upload good")
        self.repository.create_draft(draft_id = 1, user_id = 1, picture_id = id, description = description, created_at = datetime.now())
        print("db upload good")
        return {"status":"success"}

