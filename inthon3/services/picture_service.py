from fastapi import Depends, UploadFile
from sqlalchemy.orm import Session
from repository.picture_repository import PictureRepository
from schemas.picture_schema import PictureOutput
import shutil
import uuid
import os

UPLOAD_DIRECTORY = "uploads/pictures"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

class PictureService:
    def __init__(self, repository: PictureRepository = Depends()) -> None:
        self.repository = repository

    def upload_picture(self, file: UploadFile) -> PictureOutput:
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer) # 파일 저장

        file_url = f"/{file_path.replace(os.sep, '/')}"  # 경로 구분자를 '/'로 변경

        return self.repository.create_picture(picture_link=file_url)
