from fastapi import APIRouter, Depends, File, Query, UploadFile

from app.core.config import settings
from app.core.deps import require_admin_access, require_system_admin
from app.core.exceptions import AppError
from app.core.error_codes import FILE_TYPE_NOT_ALLOWED
from app.repositories.user_repository import UserRecord
from app.modules.media.storage import build_upload_object_key, save_upload_file
from app.schemas.common import ApiResponse
from app.schemas.media import UploadResult

router = APIRouter()


def _validate_image_type(content_type: str | None) -> None:
    if content_type not in settings.allowed_image_type_set():
        raise AppError(
            status_code=400,
            code=FILE_TYPE_NOT_ALLOWED,
            message="仅支持 JPG、PNG、WebP 格式",
        )


def _validate_video_type(content_type: str | None) -> None:
    if content_type not in settings.allowed_video_type_set():
        raise AppError(
            status_code=400,
            code=FILE_TYPE_NOT_ALLOWED,
            message="仅支持允许的 MP4 等视频格式",
        )


@router.post(
    "",
    response_model=ApiResponse[UploadResult],
    summary="上传头像",
    tags=["uploads"],
)
async def upload_image(
    file: UploadFile = File(...),
    _: UserRecord = Depends(require_system_admin),
) -> ApiResponse[UploadResult]:
    _validate_image_type(file.content_type)
    object_key = build_upload_object_key("original", "avatars", file.content_type)
    await save_upload_file(file, object_key, settings.max_image_size_mb)
    return ApiResponse(
        data=UploadResult(object_key=object_key, url=f"/media/{object_key}"),
    )


@router.post(
    "/brand-logos",
    response_model=ApiResponse[UploadResult],
    summary="上传品牌 Logo",
    tags=["uploads"],
)
async def upload_brand_logo(
    file: UploadFile = File(...),
    _: UserRecord = Depends(require_admin_access),
) -> ApiResponse[UploadResult]:
    _validate_image_type(file.content_type)
    object_key = build_upload_object_key("original", "brands/logos", file.content_type)
    await save_upload_file(file, object_key, settings.max_image_size_mb)
    return ApiResponse(
        data=UploadResult(object_key=object_key, url=f"/media/{object_key}"),
    )


@router.post(
    "/tile-images",
    response_model=ApiResponse[UploadResult],
    summary="上传 SKU 图片",
    tags=["uploads"],
)
async def upload_tile_image(
    file: UploadFile = File(...),
    tile_id: int | None = Query(None),
    _: UserRecord = Depends(require_admin_access),
) -> ApiResponse[UploadResult]:
    _validate_image_type(file.content_type)
    resource_type = f"tiles/{tile_id}/images" if tile_id else "tiles/pending/images"
    object_key = build_upload_object_key("original", resource_type, file.content_type)
    await save_upload_file(file, object_key, settings.max_image_size_mb)
    return ApiResponse(
        data=UploadResult(object_key=object_key, url=f"/media/{object_key}"),
    )


@router.post(
    "/tile-videos",
    response_model=ApiResponse[UploadResult],
    summary="上传 SKU 视频",
    tags=["uploads"],
)
async def upload_tile_video(
    file: UploadFile = File(...),
    tile_id: int | None = Query(None),
    _: UserRecord = Depends(require_admin_access),
) -> ApiResponse[UploadResult]:
    _validate_video_type(file.content_type)
    resource_type = f"tiles/{tile_id}" if tile_id else "tiles/pending"
    object_key = build_upload_object_key("videos", resource_type, file.content_type)
    await save_upload_file(file, object_key, settings.max_video_size_mb)
    return ApiResponse(
        data=UploadResult(object_key=object_key, url=f"/media/{object_key}"),
    )
