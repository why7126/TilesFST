from fastapi import APIRouter, UploadFile, File
from app.schemas.media import UploadResult

router = APIRouter()

@router.post(
    "",
    response_model=UploadResult,
    summary="上传图片",
    tags=["uploads"],
)
async def upload_image(file: UploadFile = File(...)) -> UploadResult:
    return UploadResult(object_key=f"tiles/{file.filename}", url=f"/media/tiles/{file.filename}")
