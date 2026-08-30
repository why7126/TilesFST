"""Admin upload endpoints."""

import hashlib
import logging
from time import perf_counter
from typing import Callable

from fastapi import APIRouter, Depends, File, Query, Request, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_effective_settings_service, require_admin_access, require_system_admin
from app.db.session import get_db
from app.core.exceptions import AppError
from app.core.error_codes import (
    CERTIFICATE_FILE_TOO_LARGE,
    CERTIFICATE_FILE_TYPE_INVALID,
    FILE_SIZE_EXCEEDED,
    FILE_TYPE_NOT_ALLOWED,
)
from app.repositories.user_repository import UserRecord
from app.repositories.task_trace_repository import TaskTraceRepository
from app.modules.media.storage import (
    build_brand_certificate_upload_object_key,
    build_business_image_upload_object_key,
    build_business_video_upload_object_key,
    build_pending_image_upload_object_key,
    build_pending_video_upload_object_key,
    media_url_for_object_key,
    media_variant_urls,
    same_directory_display_object_key,
    save_upload_file,
    same_directory_thumbnail_object_key,
)
from app.schemas.common import ApiResponse, VALIDATION_ERROR_RESPONSE
from app.schemas.media import UploadResult
from app.services.effective_settings_service import EffectiveSettingsService
from app.services.task_trace_service import TaskTraceService, elapsed_ms

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

CERTIFICATE_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp", "application/pdf"}


def _elapsed_ms(started_at: float) -> int:
    return round((perf_counter() - started_at) * 1000)


def _fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def _object_key_prefix(object_key: str | None) -> str | None:
    if not object_key:
        return None
    return object_key.rsplit("/", 1)[0] if "/" in object_key else ""


def _log_tile_video_stage(
    *,
    started_at: float,
    stage: str,
    object_key: str | None = None,
    file: UploadFile,
    tile_id: int | None,
    max_size_mb: int,
    size_bytes: int | None = None,
) -> None:
    logger.info(
        (
            "media_upload_timing upload_type=tile_video stage=%s elapsed_ms=%s "
            "object_key_hash=%s object_key_prefix=%s file_name_present=%s content_type=%s "
            "size_bytes=%s max_size_mb=%s tile_id=%s provider=%s bucket_hash=%s region=%s "
            "path_style=%s auto_create_bucket=%s"
        ),
        stage,
        _elapsed_ms(started_at),
        _fingerprint(object_key) if object_key else None,
        _object_key_prefix(object_key),
        bool(file.filename),
        file.content_type,
        size_bytes,
        max_size_mb,
        tile_id,
        settings.effective_object_storage_provider(),
        _fingerprint(settings.effective_object_storage_bucket()),
        settings.effective_object_storage_region(),
        settings.effective_object_storage_path_style(),
        settings.effective_object_storage_auto_create_bucket(),
    )


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
        task_trace_id=getattr(file, "_task_trace_id", None),
        task_type=getattr(file, "_task_type", None),
        file_key=object_key,
        file_url=url,
        file_name=file.filename or "certificate",
        mime_type=file.content_type,
        size=size,
    )


def _variant_result_fields(
    *,
    object_key: str,
    thumbnail_key: str | None,
    display_key: str | None,
) -> dict[str, str | None]:
    urls = media_variant_urls(object_key)
    return {
        "thumbnail_key": thumbnail_key,
        "thumbnail_url": media_url_for_object_key(thumbnail_key) if thumbnail_key else None,
        "display_key": display_key,
        "display_url": media_url_for_object_key(display_key) if display_key else None,
        "original_url": urls["original_url"],
    }


def _begin_upload_trace(
    *,
    request: Request,
    db: Session,
    current_user: UserRecord,
    file: UploadFile,
    task_type: str,
    business_type: str,
    max_size_mb: int,
    resource_type: str | None = None,
    resource_id: str | None = None,
) -> tuple[TaskTraceService, str, float]:
    request_id = getattr(request.state, "request_id", None)
    service = TaskTraceService(TaskTraceRepository(db), default_request_id=request_id)
    task_trace_id = service.generate_task_trace_id(task_type)
    request.state.task_trace_id = task_trace_id
    request.state.task_type = task_type
    setattr(file, "_task_trace_id", task_trace_id)
    setattr(file, "_task_type", task_type)
    started_at = perf_counter()
    base_metadata = {
        "business_type": business_type,
        "content_type": file.content_type,
        "max_size_mb": max_size_mb,
    }
    _record_upload_span(
        db=db,
        service=service,
        task_trace_id=task_trace_id,
        task_type=task_type,
        span_name="frontend_upload_start",
        sequence=10,
        actor_user_id=current_user.id,
        resource_type=resource_type,
        resource_id=resource_id,
        summary="上传任务开始",
        metadata=base_metadata,
    )
    _record_upload_span(
        db=db,
        service=service,
        task_trace_id=task_trace_id,
        task_type=task_type,
        span_name="frontend_upload_body_done",
        sequence=20,
        actor_user_id=current_user.id,
        resource_type=resource_type,
        resource_id=resource_id,
        summary="请求体已到达后端，前端 99% 阶段开始",
        metadata=base_metadata,
    )
    _record_upload_span(
        db=db,
        service=service,
        task_trace_id=task_trace_id,
        task_type=task_type,
        span_name="api_receive",
        sequence=30,
        actor_user_id=current_user.id,
        resource_type=resource_type,
        resource_id=resource_id,
        summary="后端接收上传请求",
        metadata=base_metadata,
    )
    return service, task_trace_id, started_at


def _record_upload_span(
    *,
    db: Session,
    service: TaskTraceService,
    task_trace_id: str,
    task_type: str,
    span_name: str,
    sequence: int,
    actor_user_id: str | None,
    resource_type: str | None,
    resource_id: str | None,
    status: str = "success",
    duration_ms: int | None = None,
    started_at: str | None = None,
    ended_at: str | None = None,
    error_code: str | None = None,
    summary: str | None = None,
    metadata: dict | None = None,
) -> None:
    try:
        service.record_span(
            task_trace_id=task_trace_id,
            task_type=task_type,
            span_name=span_name,
            status=status,
            sequence=sequence,
            started_at=started_at,
            ended_at=ended_at,
            duration_ms=duration_ms,
            actor_user_id=actor_user_id,
            client_type="web_admin",
            resource_type=resource_type,
            resource_id=resource_id,
            error_code=error_code,
            summary=summary,
            metadata=metadata,
        )
    except Exception:
        db.rollback()


def _upload_stage_recorder(
    *,
    db: Session,
    service: TaskTraceService,
    task_trace_id: str,
    task_type: str,
    actor_user_id: str | None,
    resource_type: str | None,
    resource_id: str | None,
) -> Callable[[str, str, int, str, str, str | None, dict | None], None]:
    sequence_by_span = {
        "file_read": 45,
        "original_put_object": 50,
        "thumbnail_generate": 55,
        "thumbnail_put_object": 56,
        "display_generate": 65,
        "display_put_object": 66,
    }

    def record(
        span_name: str,
        status: str,
        duration_ms: int,
        started_at: str,
        ended_at: str,
        error_code: str | None,
        metadata: dict | None,
    ) -> None:
        _record_upload_span(
            db=db,
            service=service,
            task_trace_id=task_trace_id,
            task_type=task_type,
            span_name=span_name,
            sequence=sequence_by_span.get(span_name, 59),
            actor_user_id=actor_user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            status=status,
            duration_ms=duration_ms,
            started_at=started_at,
            ended_at=ended_at,
            error_code=error_code,
            summary=f"上传阶段 {span_name} {status}",
            metadata=metadata,
        )

    return record


def _finish_upload_trace(
    *,
    db: Session,
    service: TaskTraceService,
    task_trace_id: str,
    task_type: str,
    actor_user_id: str | None,
    resource_type: str | None,
    resource_id: str | None,
    started_at: float,
    object_key: str | None,
    size: int | None,
    error_code: str | None = None,
) -> None:
    failed = error_code is not None
    metadata = {"object_key_prefix": object_key.rsplit("/", 1)[0] if object_key else None, "size_bytes": size}
    _record_upload_span(
        db=db,
        service=service,
        task_trace_id=task_trace_id,
        task_type=task_type,
        span_name="api_response",
        sequence=80,
        actor_user_id=actor_user_id,
        resource_type=resource_type,
        resource_id=resource_id,
        status="failed" if failed else "success",
        duration_ms=elapsed_ms(started_at),
        error_code=error_code,
        summary="后端返回上传响应" if not failed else "上传失败响应",
        metadata=metadata,
    )
    _record_upload_span(
        db=db,
        service=service,
        task_trace_id=task_trace_id,
        task_type=task_type,
        span_name="frontend_failed" if failed else "frontend_done",
        sequence=90,
        actor_user_id=actor_user_id,
        resource_type=resource_type,
        resource_id=resource_id,
        status="failed" if failed else "success",
        error_code=error_code,
        summary="前端可展示上传失败" if failed else "前端可即时回显上传结果",
        metadata=metadata,
    )


async def _save_traced_upload(
    *,
    request: Request,
    db: Session,
    current_user: UserRecord,
    file: UploadFile,
    task_type: str,
    business_type: str,
    resource_type: str,
    resource_id: str | None,
    max_size_mb: int,
    validate_file: Callable[[], None],
    object_key: str,
    thumbnail_key: str | None = None,
    thumbnail_max_size_kb: int = 0,
    display_key: str | None = None,
    display_max_size_kb: int = 768,
) -> UploadResult:
    trace_service, task_trace_id, trace_started = _begin_upload_trace(
        request=request,
        db=db,
        current_user=current_user,
        file=file,
        task_type=task_type,
        business_type=business_type,
        max_size_mb=max_size_mb,
        resource_type=resource_type,
        resource_id=resource_id,
    )
    try:
        validate_file()
        _record_upload_span(
            db=db,
            service=trace_service,
            task_trace_id=task_trace_id,
            task_type=task_type,
            span_name="validate_file",
            sequence=40,
            actor_user_id=current_user.id,
            resource_type=resource_type,
            resource_id=resource_id,
            summary="文件类型与大小限制校验通过",
            metadata={"content_type": file.content_type, "max_size_mb": max_size_mb},
        )
        size = await save_upload_file(
            file,
            object_key,
            max_size_mb,
            stage_recorder=_upload_stage_recorder(
                db=db,
                service=trace_service,
                task_trace_id=task_trace_id,
                task_type=task_type,
                actor_user_id=current_user.id,
                resource_type=resource_type,
                resource_id=resource_id,
            ),
            thumbnail_key=thumbnail_key,
            thumbnail_max_size_kb=thumbnail_max_size_kb,
            display_key=display_key,
            display_max_size_kb=display_max_size_kb,
        )
    except AppError as exc:
        _finish_upload_trace(
            db=db,
            service=trace_service,
            task_trace_id=task_trace_id,
            task_type=task_type,
            actor_user_id=current_user.id,
            resource_type=resource_type,
            resource_id=resource_id,
            started_at=trace_started,
            object_key=object_key,
            size=None,
            error_code=str(exc.code),
        )
        raise
    _record_upload_span(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type=task_type,
        span_name="storage_put_object",
        sequence=50,
        actor_user_id=current_user.id,
        resource_type=resource_type,
        resource_id=resource_id,
        duration_ms=elapsed_ms(trace_started),
        summary="对象存储写入完成",
        metadata={"object_key_prefix": object_key.rsplit("/", 1)[0], "size_bytes": size},
    )
    _record_upload_span(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type=task_type,
        span_name="db_create_media",
        sequence=60,
        actor_user_id=current_user.id,
        resource_type=resource_type,
        resource_id=resource_id,
        status="skipped",
        summary="上传接口返回对象 key，业务保存阶段落库",
    )
    _record_upload_span(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type=task_type,
        span_name="post_process",
        sequence=70,
        actor_user_id=current_user.id,
        resource_type=resource_type,
        resource_id=resource_id,
        summary="图片派生规格生成完成或已按降级策略跳过",
    )
    _finish_upload_trace(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type=task_type,
        actor_user_id=current_user.id,
        resource_type=resource_type,
        resource_id=resource_id,
        started_at=trace_started,
        object_key=object_key,
        size=size,
    )
    return UploadResult(
        object_key=object_key,
        url=f"/media/{object_key}",
        **_variant_result_fields(
            object_key=object_key,
            thumbnail_key=thumbnail_key,
            display_key=display_key,
        ),
        task_trace_id=task_trace_id,
        task_type=task_type,
        file_key=object_key,
        file_url=f"/media/{object_key}",
        file_name=file.filename,
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
    request: Request,
    file: UploadFile = File(...),
    current_user: UserRecord = Depends(require_admin_access),
    effective: EffectiveSettingsService = Depends(get_effective_settings_service),
    db: Session = Depends(get_db),
) -> ApiResponse[UploadResult]:
    max_size_mb = effective.max_image_size_mb()
    trace_service, task_trace_id, trace_started = _begin_upload_trace(
        request=request,
        db=db,
        current_user=current_user,
        file=file,
        task_type="upload_image",
        business_type="user_avatar",
        max_size_mb=max_size_mb,
        resource_type="user_avatar",
        resource_id=current_user.id,
    )
    object_key = None
    try:
        _validate_image_type(file.content_type, effective)
        _record_upload_span(
            db=db,
            service=trace_service,
            task_trace_id=task_trace_id,
            task_type="upload_image",
            span_name="validate_file",
            sequence=40,
            actor_user_id=current_user.id,
            resource_type="user_avatar",
            resource_id=current_user.id,
            summary="图片 MIME 与大小限制校验通过",
            metadata={"content_type": file.content_type, "max_size_mb": max_size_mb},
        )
        object_key = build_business_image_upload_object_key(
            "user-avatars",
            current_user.id,
            "avatars",
            file.content_type,
        )
        thumbnail_key = same_directory_thumbnail_object_key(object_key)
        display_key = same_directory_display_object_key(object_key)
        size = await save_upload_file(
            file,
            object_key,
            max_size_mb,
            stage_recorder=_upload_stage_recorder(
                db=db,
                service=trace_service,
                task_trace_id=task_trace_id,
                task_type="upload_image",
                actor_user_id=current_user.id,
                resource_type="user_avatar",
                resource_id=current_user.id,
            ),
            thumbnail_key=thumbnail_key,
            thumbnail_max_size_kb=effective.thumbnail_max_size_kb(),
            display_key=display_key,
            display_max_size_kb=effective.display_max_size_kb(),
        )
    except AppError as exc:
        _finish_upload_trace(
            db=db,
            service=trace_service,
            task_trace_id=task_trace_id,
            task_type="upload_image",
            actor_user_id=current_user.id,
            resource_type="user_avatar",
            resource_id=current_user.id,
            started_at=trace_started,
            object_key=object_key,
            size=None,
            error_code=str(exc.code),
        )
        raise
    _record_upload_span(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type="upload_image",
        span_name="storage_put_object",
        sequence=50,
        actor_user_id=current_user.id,
        resource_type="user_avatar",
        resource_id=current_user.id,
        duration_ms=elapsed_ms(trace_started),
        summary="对象存储写入完成",
        metadata={"object_key_prefix": object_key.rsplit("/", 1)[0], "size_bytes": size},
    )
    _record_upload_span(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type="upload_image",
        span_name="db_create_media",
        sequence=60,
        actor_user_id=current_user.id,
        resource_type="user_avatar",
        resource_id=current_user.id,
        status="skipped",
        summary="头像上传返回对象 key，业务表单保存阶段落库",
    )
    _record_upload_span(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type="upload_image",
        span_name="post_process",
        sequence=70,
        actor_user_id=current_user.id,
        resource_type="user_avatar",
        resource_id=current_user.id,
        summary="头像图片派生规格生成完成或已按降级策略跳过",
    )
    _finish_upload_trace(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type="upload_image",
        actor_user_id=current_user.id,
        resource_type="user_avatar",
        resource_id=current_user.id,
        started_at=trace_started,
        object_key=object_key,
        size=size,
    )
    return ApiResponse(
        data=UploadResult(
            object_key=object_key,
            url=f"/media/{object_key}",
            **_variant_result_fields(
                object_key=object_key,
                thumbnail_key=thumbnail_key,
                display_key=display_key,
            ),
            task_trace_id=task_trace_id,
            task_type="upload_image",
        ),
    )


@router.post(
    "/brand-logos",
    response_model=ApiResponse[UploadResult],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="上传品牌 Logo",
)
async def upload_brand_logo(
    request: Request,
    brand_id: int | None = Query(None),
    file: UploadFile = File(...),
    current_user: UserRecord = Depends(require_admin_access),
    effective: EffectiveSettingsService = Depends(get_effective_settings_service),
    db: Session = Depends(get_db),
    ) -> ApiResponse[UploadResult]:
    object_key = (
        build_business_image_upload_object_key("brand-logos", brand_id, "logos", file.content_type)
        if brand_id
        else build_pending_image_upload_object_key("brand-logos", "logos", file.content_type)
    )
    return ApiResponse(
        data=await _save_traced_upload(
            request=request,
            db=db,
            current_user=current_user,
            file=file,
            task_type="upload_image",
            business_type="brand_logo",
            resource_type="brand_logo",
            resource_id=str(brand_id) if brand_id else None,
            max_size_mb=effective.max_image_size_mb(),
            validate_file=lambda: _validate_image_type(file.content_type, effective),
            object_key=object_key,
            thumbnail_key=same_directory_thumbnail_object_key(object_key),
            display_key=same_directory_display_object_key(object_key),
            thumbnail_max_size_kb=effective.thumbnail_max_size_kb(),
            display_max_size_kb=effective.display_max_size_kb(),
        ),
    )


@router.post(
    "/banner-images",
    response_model=ApiResponse[UploadResult],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="上传 Banner 图片",
)
async def upload_banner_image(
    request: Request,
    banner_id: int | None = Query(None),
    file: UploadFile = File(...),
    current_user: UserRecord = Depends(require_admin_access),
    effective: EffectiveSettingsService = Depends(get_effective_settings_service),
    db: Session = Depends(get_db),
) -> ApiResponse[UploadResult]:
    object_key = (
        build_business_image_upload_object_key("banners", banner_id, "images", file.content_type)
        if banner_id
        else build_pending_image_upload_object_key("banners", "images", file.content_type)
    )
    return ApiResponse(
        data=await _save_traced_upload(
            request=request,
            db=db,
            current_user=current_user,
            file=file,
            task_type="upload_image",
            business_type="banner_image",
            resource_type="banner",
            resource_id=str(banner_id) if banner_id else None,
            max_size_mb=effective.max_image_size_mb(),
            validate_file=lambda: _validate_image_type(file.content_type, effective),
            object_key=object_key,
            thumbnail_key=same_directory_thumbnail_object_key(object_key),
            display_key=same_directory_display_object_key(object_key),
            thumbnail_max_size_kb=effective.thumbnail_max_size_kb(),
            display_max_size_kb=effective.display_max_size_kb(),
        ),
    )


@router.post(
    "/tile-images",
    response_model=ApiResponse[UploadResult],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="上传 SKU 图片",
)
async def upload_tile_image(
    request: Request,
    file: UploadFile = File(...),
    tile_id: int | None = Query(None),
    current_user: UserRecord = Depends(require_admin_access),
    effective: EffectiveSettingsService = Depends(get_effective_settings_service),
    db: Session = Depends(get_db),
) -> ApiResponse[UploadResult]:
    object_key = (
        build_business_image_upload_object_key("tiles", tile_id, "images", file.content_type)
        if tile_id
        else build_pending_image_upload_object_key("tiles", "images", file.content_type)
    )
    return ApiResponse(
        data=await _save_traced_upload(
            request=request,
            db=db,
            current_user=current_user,
            file=file,
            task_type="upload_image",
            business_type="tile_image",
            resource_type="tile",
            resource_id=str(tile_id) if tile_id else None,
            max_size_mb=effective.max_image_size_mb(),
            validate_file=lambda: _validate_image_type(file.content_type, effective),
            object_key=object_key,
            thumbnail_key=same_directory_thumbnail_object_key(object_key),
            display_key=same_directory_display_object_key(object_key),
            thumbnail_max_size_kb=effective.thumbnail_max_size_kb(),
            display_max_size_kb=effective.display_max_size_kb(),
        ),
    )


@router.post(
    "/tile-videos",
    response_model=ApiResponse[UploadResult],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="上传 SKU 视频",
)
async def upload_tile_video(
    request: Request,
    file: UploadFile = File(...),
    tile_id: int | None = Query(None),
    current_user: UserRecord = Depends(require_admin_access),
    effective: EffectiveSettingsService = Depends(get_effective_settings_service),
    db: Session = Depends(get_db),
) -> ApiResponse[UploadResult]:
    started_at = perf_counter()
    max_size_mb = effective.max_video_size_mb()
    trace_service, task_trace_id, trace_started = _begin_upload_trace(
        request=request,
        db=db,
        current_user=current_user,
        file=file,
        task_type="upload_video",
        business_type="tile_video",
        max_size_mb=max_size_mb,
        resource_type="tile",
        resource_id=str(tile_id) if tile_id else None,
    )
    _log_tile_video_stage(
        started_at=started_at,
        stage="request_received",
        file=file,
        tile_id=tile_id,
        max_size_mb=max_size_mb,
    )
    object_key = None
    try:
        _validate_video_type(file.content_type, effective)
    except AppError as exc:
        _finish_upload_trace(
            db=db,
            service=trace_service,
            task_trace_id=task_trace_id,
            task_type="upload_video",
            actor_user_id=current_user.id,
            resource_type="tile",
            resource_id=str(tile_id) if tile_id else None,
            started_at=trace_started,
            object_key=None,
            size=None,
            error_code=str(exc.code),
        )
        raise
    _record_upload_span(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type="upload_video",
        span_name="validate_file",
        sequence=40,
        actor_user_id=current_user.id,
        resource_type="tile",
        resource_id=str(tile_id) if tile_id else None,
        summary="视频 MIME 与大小限制校验通过",
        metadata={"content_type": file.content_type, "max_size_mb": max_size_mb},
    )
    _log_tile_video_stage(
        started_at=started_at,
        stage="type_validation_done",
        file=file,
        tile_id=tile_id,
        max_size_mb=max_size_mb,
    )
    object_key = (
        build_business_video_upload_object_key("tiles", tile_id, "videos", file.content_type)
        if tile_id
        else build_pending_video_upload_object_key("tiles", "videos", file.content_type)
    )
    _log_tile_video_stage(
        started_at=started_at,
        stage="object_key_built",
        object_key=object_key,
        file=file,
        tile_id=tile_id,
        max_size_mb=max_size_mb,
    )
    try:
        size = await save_upload_file(
            file,
            object_key,
            max_size_mb,
            timing={
                "started_at": started_at,
                "upload_type": "tile_video",
                "object_key": object_key,
                "object_key_prefix": _object_key_prefix(object_key),
                "file_name_present": bool(file.filename),
                "content_type": file.content_type,
                "max_size_mb": max_size_mb,
                "provider": settings.effective_object_storage_provider(),
                "bucket_hash": _fingerprint(settings.effective_object_storage_bucket()),
                "region": settings.effective_object_storage_region(),
                "path_style": settings.effective_object_storage_path_style(),
                "auto_create_bucket": settings.effective_object_storage_auto_create_bucket(),
            },
        )
    except AppError as exc:
        _finish_upload_trace(
            db=db,
            service=trace_service,
            task_trace_id=task_trace_id,
            task_type="upload_video",
            actor_user_id=current_user.id,
            resource_type="tile",
            resource_id=str(tile_id) if tile_id else None,
            started_at=trace_started,
            object_key=object_key,
            size=None,
            error_code=str(exc.code),
        )
        raise
    _record_upload_span(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type="upload_video",
        span_name="storage_put_object",
        sequence=50,
        actor_user_id=current_user.id,
        resource_type="tile",
        resource_id=str(tile_id) if tile_id else None,
        duration_ms=elapsed_ms(trace_started),
        summary="对象存储写入完成",
        metadata={"object_key_prefix": object_key.rsplit("/", 1)[0], "size_bytes": size},
    )
    _record_upload_span(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type="upload_video",
        span_name="db_create_media",
        sequence=60,
        actor_user_id=current_user.id,
        resource_type="tile",
        resource_id=str(tile_id) if tile_id else None,
        status="skipped",
        summary="SKU 视频上传返回对象 key，SKU 保存阶段落库",
    )
    _record_upload_span(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type="upload_video",
        span_name="post_process",
        sequence=70,
        actor_user_id=current_user.id,
        resource_type="tile",
        resource_id=str(tile_id) if tile_id else None,
        status="skipped",
        summary="本次上传无视频转码后处理",
    )
    _log_tile_video_stage(
        started_at=started_at,
        stage="response_ready",
        object_key=object_key,
        file=file,
        tile_id=tile_id,
        max_size_mb=max_size_mb,
        size_bytes=size,
    )
    _finish_upload_trace(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type="upload_video",
        actor_user_id=current_user.id,
        resource_type="tile",
        resource_id=str(tile_id) if tile_id else None,
        started_at=trace_started,
        object_key=object_key,
        size=size,
    )
    return ApiResponse(
        data=UploadResult(
            object_key=object_key,
            url=f"/media/{object_key}",
            task_trace_id=task_trace_id,
            task_type="upload_video",
            file_key=object_key,
            file_url=f"/media/{object_key}",
            file_name=file.filename,
            mime_type=file.content_type,
            size=size,
        ),
    )


@router.post(
    "/brand-certificates",
    response_model=ApiResponse[UploadResult],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="上传品牌证书文件",
)
async def upload_brand_certificate(
    request: Request,
    certificate_id: int | None = Query(None),
    file: UploadFile = File(...),
    current_user: UserRecord = Depends(require_system_admin),
    effective: EffectiveSettingsService = Depends(get_effective_settings_service),
    db: Session = Depends(get_db),
) -> ApiResponse[UploadResult]:
    max_size_mb = effective.max_file_size_mb()
    trace_service, task_trace_id, trace_started = _begin_upload_trace(
        request=request,
        db=db,
        current_user=current_user,
        file=file,
        task_type="upload_file",
        business_type="brand_certificate",
        max_size_mb=max_size_mb,
        resource_type="brand_certificate",
        resource_id=str(certificate_id) if certificate_id else None,
    )
    object_key = None
    try:
        _validate_certificate_type(file.content_type)
        _record_upload_span(
            db=db,
            service=trace_service,
            task_trace_id=task_trace_id,
            task_type="upload_file",
            span_name="validate_file",
            sequence=40,
            actor_user_id=current_user.id,
            resource_type="brand_certificate",
            resource_id=str(certificate_id) if certificate_id else None,
            summary="证书文件 MIME 与大小限制校验通过",
            metadata={"content_type": file.content_type, "max_size_mb": max_size_mb},
        )
        object_key = build_brand_certificate_upload_object_key(file.content_type, certificate_id)
        thumbnail_key = (
            same_directory_thumbnail_object_key(object_key)
            if file.content_type and file.content_type.startswith("image/")
            else None
        )
        display_key = (
            same_directory_display_object_key(object_key)
            if file.content_type and file.content_type.startswith("image/")
            else None
        )
        size = await save_upload_file(
            file,
            object_key,
            max_size_mb,
            stage_recorder=_upload_stage_recorder(
                db=db,
                service=trace_service,
                task_trace_id=task_trace_id,
                task_type="upload_file",
                actor_user_id=current_user.id,
                resource_type="brand_certificate",
                resource_id=str(certificate_id) if certificate_id else None,
            ),
            thumbnail_key=thumbnail_key,
            thumbnail_max_size_kb=effective.thumbnail_max_size_kb() if thumbnail_key else 0,
            display_key=display_key,
            display_max_size_kb=effective.display_max_size_kb() if display_key else 0,
        )
    except AppError as exc:
        error_code = CERTIFICATE_FILE_TOO_LARGE if exc.code == FILE_SIZE_EXCEEDED else exc.code
        _finish_upload_trace(
            db=db,
            service=trace_service,
            task_trace_id=task_trace_id,
            task_type="upload_file",
            actor_user_id=current_user.id,
            resource_type="brand_certificate",
            resource_id=str(certificate_id) if certificate_id else None,
            started_at=trace_started,
            object_key=object_key,
            size=None,
            error_code=str(error_code),
        )
        if exc.code == FILE_SIZE_EXCEEDED:
            raise AppError(
                status_code=400,
                code=CERTIFICATE_FILE_TOO_LARGE,
                message=f"证书文件不能超过 {max_size_mb}MB",
            ) from exc
        raise
    _record_upload_span(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type="upload_file",
        span_name="storage_put_object",
        sequence=50,
        actor_user_id=current_user.id,
        resource_type="brand_certificate",
        resource_id=str(certificate_id) if certificate_id else None,
        duration_ms=elapsed_ms(trace_started),
        summary="对象存储写入完成",
        metadata={"object_key_prefix": object_key.rsplit("/", 1)[0], "size_bytes": size},
    )
    _record_upload_span(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type="upload_file",
        span_name="db_create_media",
        sequence=60,
        actor_user_id=current_user.id,
        resource_type="brand_certificate",
        resource_id=str(certificate_id) if certificate_id else None,
        status="skipped",
        summary="证书上传返回对象 key，品牌证书保存阶段落库",
    )
    _record_upload_span(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type="upload_file",
        span_name="post_process",
        sequence=70,
        actor_user_id=current_user.id,
        resource_type="brand_certificate",
        resource_id=str(certificate_id) if certificate_id else None,
        status="success" if file.content_type and file.content_type.startswith("image/") else "skipped",
        summary="证书图片派生规格生成完成或文件类证书无需派生",
    )
    _finish_upload_trace(
        db=db,
        service=trace_service,
        task_trace_id=task_trace_id,
        task_type="upload_file",
        actor_user_id=current_user.id,
        resource_type="brand_certificate",
        resource_id=str(certificate_id) if certificate_id else None,
        started_at=trace_started,
        object_key=object_key,
        size=size,
    )
    return ApiResponse(
        data=UploadResult(
            object_key=object_key,
            url=f"/media/{object_key}",
            **_variant_result_fields(
                object_key=object_key,
                thumbnail_key=thumbnail_key,
                display_key=display_key,
            ),
            task_trace_id=task_trace_id,
            task_type="upload_file",
            file_key=object_key,
            file_url=f"/media/{object_key}",
            file_name=file.filename or "certificate",
            mime_type=file.content_type,
            size=size,
        )
    )
