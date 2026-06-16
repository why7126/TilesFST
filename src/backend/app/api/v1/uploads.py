from fastapi import APIRouter, Depends, File, UploadFile

from app.core.deps import require_system_admin
from app.repositories.user_repository import UserRecord
from app.schemas.common import ApiResponse
from app.schemas.media import UploadResult

router = APIRouter(dependencies=[Depends(require_system_admin)])


@router.post(
    "",
    response_model=ApiResponse[UploadResult],
    summary="上传图片",
    tags=["uploads"],
)
async def upload_image(
    file: UploadFile = File(...),
    _: UserRecord = Depends(require_system_admin),
) -> ApiResponse[UploadResult]:
    safe_name = (file.filename or "avatar").replace("/", "_")
    object_key = f"avatars/{safe_name}"
    return ApiResponse(
        data=UploadResult(object_key=object_key, url=f"/media/{object_key}"),
    )
