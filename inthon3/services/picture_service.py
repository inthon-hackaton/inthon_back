from fastapi import Depends, UploadFile, HTTPException
from repository.picture_repository import PictureRepository
from schemas.picture_schema import PictureOutput
import boto3
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

# AWS 환경 변수
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = "leaf-bucket"

class PictureService:
    def __init__(self, repository: PictureRepository = Depends()) -> None:
        self.repository = repository
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

    def upload_picture(self, file: UploadFile) -> PictureOutput:
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        s3_key = f"uploads/pictures/{unique_filename}"

        try:
            self.s3.upload_fileobj(file.file, S3_BUCKET_NAME, s3_key)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to upload file to S3")


        file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

        return self.repository.create_picture(picture_link=file_url)
