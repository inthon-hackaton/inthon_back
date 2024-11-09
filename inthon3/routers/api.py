from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from routers.v1 import picture, auth

router = APIRouter(
    prefix="/api/v1",
    tags=["sample"],
    responses={404: {"description": "Not Found"}},
)

router.include_router(picture.router)
router.include_router(auth.router)

@router.get("/")
async def read_root():
    return {"message": "Hello!"}