# from typing import List
# from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
# from sqlalchemy.orm import Session
# from config.database import get_db
# from schemas.picture_schema import PictureOutput
# from services.picture_service import PictureService

# router = APIRouter(
#     prefix="/picture",
#     tags=["picture"]
# )

# @router.post("/upload", response_model=PictureOutput)
# async def upload_picture(
#     file: UploadFile = File(...),
#     service: PictureService = Depends()
# ):
#     return service.upload_picture(file)
