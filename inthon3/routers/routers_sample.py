from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="",
    tags = [],
    responses = {
        404: {"description" : "Not Found"}
    }
)