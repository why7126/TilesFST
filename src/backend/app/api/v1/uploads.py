from fastapi import APIRouter, Depends, File, Query, UploadFile

from app.core.deps import require_admin_access, require_system_admin
from app.core.exceptions import AppError
from app.core.error_codes import FILE_TYPE_NOT_ALLOWED
from app.repositories.user_repository import UserRecord
from app.schemas.common import ApiResponse
from app.schemas.media import UploadResult

router = APIRouter()

ALLOWED_IMAGE_TYPES = frozenset(
    {"image/jpeg", "image/png", "image/webp", "image/jpg"},
)
ALLOWED_VIDEO_TYPES = frozenset({"video/mp4"})


def _validate_image_type(content_type: str | None) -> None:
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise AppError(
            status_code=400,
            code=FILE_TYPE_NOT_ALLOWED,
            message="仅支持 JPG、PNG、WebP 格式",
        )


def _validate_video_type(content_type: str | None) -> None:
    if content_type not in ALLOWED_VIDEO_TYPES:
        raise AppError(
            status_code=400,
            code=FILE_TYPE_NOT_ALLOWED,
            message="仅支持 MP4 格式",
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
    safe_name = (file.filename or "avatar").replace("/", "_")
    object_key = f"avatars/{safe_name}"
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
    safe_name = (file.filename or "logo").replace("/", "_")
    object_key = f"brands/logos/{safe_name}"
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
    safe_name = (file.filename or "image").replace("/", "_")
    prefix = f"tiles/{tile_id}/images" if tile_id else "tiles/pending/images"
    object_key = f"{prefix}/{safe_name}"
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
    safe_name = (file.filename or "video.mp4").replace("/", "_")
    prefix = f"tiles/{tile_id}/videos" if tile_id else "tiles/pending/videos"
    object_key = f"{prefix}/{safe_name}"
    return ApiResponse(
        data=UploadResult(object_key=object_key, url=f"/media/{object_key}"),
    )
