"""Admin upload endpoints."""

from fastapi import APIRouter, Depends, File, Query, UploadFile

from app.core.deps import get_effective_settings_service, require_admin_access, require_system_admin
from app.core.exceptions import AppError
from app.core.error_codes import (
    CERTIFICATE_FILE_TOO_LARGE,
    CERTIFICATE_FILE_TYPE_INVALID,
    FILE_SIZE_EXCEEDED,
    FILE_TYPE_NOT_ALLOWED,
)
from app.repositories.user_repository import UserRecord
from app.modules.media.storage import (
    build_image_upload_object_key,
    build_file_upload_object_key,
    build_video_upload_object_key,
    save_upload_file,
)
from app.schemas.common import ApiResponse, VALIDATION_ERROR_RESPONSE
from app.schemas.media import UploadResult
from app.services.effective_settings_service import EffectiveSettingsService

router = APIRouter()

CERTIFICATE_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp", "application/pdf"}
CERTIFICATE_MAX_SIZE_MB = 20


def _validate_image_type(content_type: str | None, effective: EffectiveSettingsService) -> None:
    if content_type not in effective.allowed_image_type_set():
        raise AppError(
            status_code=400,
            code=FILE_TYPE_NOT_ALLOWED,
            message="仅支持 JPG、PNG、WebP 格式",
        )


def _validate_video_type(content_type: str | None, effective: EffectiveSettingsService) -> None:
    if content_type not in effective.allowed_video_type_set():
        raise AppError(
            status_code=400,
            code=FILE_TYPE_NOT_ALLOWED,
            message="仅支持允许的 MP4 等视频格式",
        )


def _validate_certificate_type(content_type: str | None) -> None:
    if content_type not in CERTIFICATE_TYPES:
        raise AppError(
            status_code=400,
            code=CERTIFICATE_FILE_TYPE_INVALID,
            message="仅支持 JPG、PNG、WebP、PDF 格式",
        )


def _upload_result(
    *,
    object_key: str,
    size: int,
    file: UploadFile,
) -> UploadResult:
    url = f"/media/{object_key}"
    return UploadResult(
        object_key=object_key,
        url=url,
        file_key=object_key,
        file_url=url,
        file_name=file.filename or "certificate",
        mime_type=file.content_type,
        size=size,
    )


@router.post(
    "",
    response_model=ApiResponse[UploadResult],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="上传头像",
)
async def upload_image(
    file: UploadFile = File(...),
    _: UserRecord = Depends(require_admin_access),
    effective: EffectiveSettingsService = Depends(get_effective_settings_service),
) -> ApiResponse[UploadResult]:
    _validate_image_type(file.content_type, effective)
    object_key = build_image_upload_object_key("user/avatars", file.content_type)
    await save_upload_file(file, object_key, effective.max_image_size_mb())
    return ApiResponse(
        data=UploadResult(object_key=object_key, url=f"/media/{object_key}"),
    )


@router.post(
    "/brand-logos",
    response_model=ApiResponse[UploadResult],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="上传品牌 Logo",
)
async def upload_brand_logo(
    file: UploadFile = File(...),
    _: UserRecord = Depends(require_admin_access),
    effective: EffectiveSettingsService = Depends(get_effective_settings_service),
) -> ApiResponse[UploadResult]:
    _validate_image_type(file.content_type, effective)
    object_key = build_image_upload_object_key("brands/logos", file.content_type)
    await save_upload_file(file, object_key, effective.max_image_size_mb())
    return ApiResponse(
        data=UploadResult(object_key=object_key, url=f"/media/{object_key}"),
    )


@router.post(
    "/banner-images",
    response_model=ApiResponse[UploadResult],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="上传 Banner 图片",
)
async def upload_banner_image(
    file: UploadFile = File(...),
    _: UserRecord = Depends(require_admin_access),
    effective: EffectiveSettingsService = Depends(get_effective_settings_service),
) -> ApiResponse[UploadResult]:
    _validate_image_type(file.content_type, effective)
    object_key = build_image_upload_object_key("banners", file.content_type)
    await save_upload_file(file, object_key, effective.max_image_size_mb())
    return ApiResponse(
        data=UploadResult(object_key=object_key, url=f"/media/{object_key}"),
    )


@router.post(
    "/tile-images",
    response_model=ApiResponse[UploadResult],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="上传 SKU 图片",
)
async def upload_tile_image(
    file: UploadFile = File(...),
    tile_id: int | None = Query(None),
    _: UserRecord = Depends(require_admin_access),
    effective: EffectiveSettingsService = Depends(get_effective_settings_service),
) -> ApiResponse[UploadResult]:
    _validate_image_type(file.content_type, effective)
    resource_type = f"tiles/{tile_id}" if tile_id else "tiles/pending"
    object_key = build_image_upload_object_key(resource_type, file.content_type)
    await save_upload_file(file, object_key, effective.max_image_size_mb())
    return ApiResponse(
        data=UploadResult(object_key=object_key, url=f"/media/{object_key}"),
    )


@router.post(
    "/tile-videos",
    response_model=ApiResponse[UploadResult],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="上传 SKU 视频",
)
async def upload_tile_video(
    file: UploadFile = File(...),
    tile_id: int | None = Query(None),
    _: UserRecord = Depends(require_admin_access),
    effective: EffectiveSettingsService = Depends(get_effective_settings_service),
) -> ApiResponse[UploadResult]:
    _validate_video_type(file.content_type, effective)
    resource_type = f"tiles/{tile_id}" if tile_id else "tiles/pending"
    object_key = build_video_upload_object_key(resource_type, file.content_type)
    await save_upload_file(file, object_key, effective.max_video_size_mb())
    return ApiResponse(
        data=UploadResult(object_key=object_key, url=f"/media/{object_key}"),
    )


@router.post(
    "/brand-certificates",
    response_model=ApiResponse[UploadResult],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="上传品牌证书文件",
)
async def upload_brand_certificate(
    file: UploadFile = File(...),
    _: UserRecord = Depends(require_system_admin),
) -> ApiResponse[UploadResult]:
    _validate_certificate_type(file.content_type)
    object_key = build_file_upload_object_key("brand-certificates", file.content_type)
    try:
        size = await save_upload_file(file, object_key, CERTIFICATE_MAX_SIZE_MB)
    except AppError as exc:
        if exc.code == FILE_SIZE_EXCEEDED:
            raise AppError(
                status_code=400,
                code=CERTIFICATE_FILE_TOO_LARGE,
                message="证书文件不能超过 20MB",
            ) from exc
        raise
    return ApiResponse(data=_upload_result(object_key=object_key, size=size, file=file))
