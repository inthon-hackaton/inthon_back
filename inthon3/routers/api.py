from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from routers.v1 import picture, draft, auth, piece, likes, completion, leaf_user

router = APIRouter(
    prefix="/api/v1",
    tags=["sample"],
    responses={404: {"description": "Not Found"}},
)


router.include_router(draft.router)

router.include_router(auth.router)
router.include_router(piece.router)
router.include_router(likes.router)
router.include_router(completion.router)
router.include_router(leaf_user.router)


@router.get("/")
async def read_root():
    return {"message": "Hello!"}