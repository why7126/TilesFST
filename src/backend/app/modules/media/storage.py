"""Media storage adapters and controlled media object access."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
import logging
import mimetypes
from pathlib import PurePosixPath
from time import perf_counter
from typing import Any, Protocol

from fastapi import UploadFile
from fastapi.responses import Response

from app.core.config import settings
from app.core.error_codes import FILE_SIZE_EXCEEDED, STORAGE_UNAVAILABLE
from app.core.exceptions import AppError
from app.modules.media.key_migration import map_legacy_object_key
from app.modules.media.object_keys import build_object_key

MEDIA_NOT_FOUND = 40404
MEDIA_INVALID_OBJECT_KEY = 40040

logger = logging.getLogger("uvicorn.error")

_EXTENSIONS_BY_TYPE = {
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "application/pdf": "pdf",
    "video/mp4": "mp4",
    "video/quicktime": "mov",
    "video/x-msvideo": "avi",
    "video/webm": "webm",
    "video/x-matroska": "mkv",
    "video/x-m4v": "m4v",
}


def _extension_for_content_type(content_type: str | None) -> str:
    if content_type in _EXTENSIONS_BY_TYPE:
        return _EXTENSIONS_BY_TYPE[content_type]
    guessed = mimetypes.guess_extension(content_type or "")
    if guessed:
        return guessed.lstrip(".")
    return "bin"


def _detect_content_type(content: bytes) -> str | None:
    if content.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if len(content) >= 12 and content[:4] == b"RIFF" and content[8:12] == b"WEBP":
        return "image/webp"
    if content.startswith((b"GIF87a", b"GIF89a")):
        return "image/gif"
    return None


@dataclass(frozen=True)
class StoredMediaObject:
    content: bytes
    content_type: str | None = None
    total_size: int | None = None


@dataclass(frozen=True)
class MediaObjectInfo:
    content_type: str | None
    total_size: int


class MediaStorageClient(Protocol):
    def put_object(self, object_key: str, content: bytes, content_type: str | None) -> None:
        """Persist object bytes under the configured object key."""

    def get_object(self, object_key: str) -> StoredMediaObject:
        """Return object bytes and optional content type."""

    def get_object_info(self, object_key: str) -> MediaObjectInfo:
        """Return object metadata without reading object bytes."""

    def get_object_range(self, object_key: str, offset: int, length: int) -> StoredMediaObject:
        """Return a byte range and total object size."""


class S3CompatibleMediaStorageClient:
    def __init__(self) -> None:
        self._client = None

    def _client_endpoint(self) -> str:
        return settings.effective_object_storage_endpoint()

    def _get_client(self):
        if self._client is None:
            from minio import Minio

            self._client = Minio(
                self._client_endpoint(),
                access_key=settings.effective_object_storage_access_key(),
                secret_key=settings.effective_object_storage_secret_key(),
                secure=settings.effective_object_storage_secure(),
                region=settings.effective_object_storage_region(),
            )
            if not settings.effective_object_storage_path_style():
                # minio-py enables virtual-host style only for AWS/Aliyun by default.
                self._client._base_url._virtual_style_flag = True
        return self._client

    def _ensure_bucket(self) -> None:
        if not settings.effective_object_storage_auto_create_bucket():
            return

        client = self._get_client()
        bucket = settings.effective_object_storage_bucket()
        try:
            if client.bucket_exists(bucket):
                return
            client.make_bucket(bucket)
        except AppError:
            raise
        except Exception as exc:
            raise AppError(
                status_code=502,
                code=STORAGE_UNAVAILABLE,
                message="对象存储不可用",
            ) from exc

    def put_object(self, object_key: str, content: bytes, content_type: str | None) -> None:
        validate_object_key(object_key)
        self._ensure_bucket()
        client = self._get_client()
        try:
            client.put_object(
                settings.effective_object_storage_bucket(),
                object_key,
                BytesIO(content),
                length=len(content),
                content_type=content_type,
            )
        except Exception as exc:
            raise AppError(
                status_code=502,
                code=STORAGE_UNAVAILABLE,
                message="对象存储不可用",
            ) from exc

    def get_object(self, object_key: str) -> StoredMediaObject:
        validate_object_key(object_key)
        client = self._get_client()
        response = None
        try:
            response = client.get_object(settings.effective_object_storage_bucket(), object_key)
            content = response.read()
        except Exception as exc:
            code = getattr(exc, "code", "")
            if code in {"NoSuchKey", "NoSuchObject"}:
                raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体文件不存在") from exc
            raise AppError(
                status_code=502,
                code=STORAGE_UNAVAILABLE,
                message="对象存储不可用",
            ) from exc
        finally:
            if response is not None:
                response.close()
                response.release_conn()

        content_type = _detect_content_type(content) or mimetypes.guess_type(object_key)[0]
        return StoredMediaObject(content=content, content_type=content_type, total_size=len(content))

    def get_object_info(self, object_key: str) -> MediaObjectInfo:
        validate_object_key(object_key)
        client = self._get_client()
        try:
            stat = client.stat_object(settings.effective_object_storage_bucket(), object_key)
        except Exception as exc:
            code = getattr(exc, "code", "")
            if code in {"NoSuchKey", "NoSuchObject"}:
                raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体文件不存在") from exc
            raise AppError(
                status_code=502,
                code=STORAGE_UNAVAILABLE,
                message="对象存储不可用",
            ) from exc
        return MediaObjectInfo(
            content_type=getattr(stat, "content_type", None) or mimetypes.guess_type(object_key)[0],
            total_size=int(getattr(stat, "size", 0) or 0),
        )

    def get_object_range(self, object_key: str, offset: int, length: int) -> StoredMediaObject:
        validate_object_key(object_key)
        client = self._get_client()
        response = None
        try:
            stat = client.stat_object(settings.effective_object_storage_bucket(), object_key)
            response = client.get_object(
                settings.effective_object_storage_bucket(),
                object_key,
                offset=offset,
                length=length,
            )
            content = response.read(length)
        except Exception as exc:
            code = getattr(exc, "code", "")
            if code in {"NoSuchKey", "NoSuchObject"}:
                raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体文件不存在") from exc
            raise AppError(
                status_code=502,
                code=STORAGE_UNAVAILABLE,
                message="对象存储不可用",
            ) from exc
        finally:
            if response is not None:
                response.close()
                response.release_conn()

        content_type = getattr(stat, "content_type", None) or mimetypes.guess_type(object_key)[0]
        total_size = getattr(stat, "size", None)
        return StoredMediaObject(content=content, content_type=content_type, total_size=total_size)


class TencentCOSMediaStorageClient:
    def __init__(self) -> None:
        self._client = None

    def _get_client(self):
        if self._client is None:
            from qcloud_cos import CosConfig, CosS3Client

            self._client = CosS3Client(
                CosConfig(
                    Region=settings.effective_object_storage_region(),
                    SecretId=settings.effective_object_storage_access_key(),
                    SecretKey=settings.effective_object_storage_secret_key(),
                    Scheme="https" if settings.effective_object_storage_secure() else "http",
                    Endpoint=settings.effective_object_storage_endpoint(),
                    EnableInternalDomain="internal" in settings.effective_object_storage_endpoint(),
                    KeepAlive=True,
                )
            )
        return self._client

    def put_object(self, object_key: str, content: bytes, content_type: str | None) -> None:
        validate_object_key(object_key)
        try:
            self._get_client().put_object(
                Bucket=settings.effective_object_storage_bucket(),
                Key=object_key,
                Body=BytesIO(content),
                ContentType=content_type,
                EnableMD5=False,
            )
        except Exception as exc:
            raise AppError(
                status_code=502,
                code=STORAGE_UNAVAILABLE,
                message="对象存储不可用",
            ) from exc

    def get_object(self, object_key: str) -> StoredMediaObject:
        validate_object_key(object_key)
        try:
            response = self._get_client().get_object(
                Bucket=settings.effective_object_storage_bucket(),
                Key=object_key,
            )
            content = response["Body"].get_raw_stream().read()
        except Exception as exc:
            code = getattr(exc, "code", "")
            if code in {"NoSuchKey", "NoSuchObject"}:
                raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体文件不存在") from exc
            raise AppError(
                status_code=502,
                code=STORAGE_UNAVAILABLE,
                message="对象存储不可用",
            ) from exc

        content_type = _detect_content_type(content) or mimetypes.guess_type(object_key)[0]
        return StoredMediaObject(content=content, content_type=content_type, total_size=len(content))

    def get_object_info(self, object_key: str) -> MediaObjectInfo:
        validate_object_key(object_key)
        try:
            response = self._get_client().head_object(
                Bucket=settings.effective_object_storage_bucket(),
                Key=object_key,
            )
        except Exception as exc:
            code = getattr(exc, "code", "")
            if code in {"NoSuchKey", "NoSuchObject"}:
                raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体文件不存在") from exc
            raise AppError(
                status_code=502,
                code=STORAGE_UNAVAILABLE,
                message="对象存储不可用",
            ) from exc

        content_type = response.get("Content-Type") or response.get("content-type")
        content_length = response.get("Content-Length") or response.get("content-length") or 0
        return MediaObjectInfo(
            content_type=content_type or mimetypes.guess_type(object_key)[0],
            total_size=int(content_length or 0),
        )

    def get_object_range(self, object_key: str, offset: int, length: int) -> StoredMediaObject:
        validate_object_key(object_key)
        range_header = f"bytes={offset}-{offset + length - 1}"
        try:
            info = self.get_object_info(object_key)
            response = self._get_client().get_object(
                Bucket=settings.effective_object_storage_bucket(),
                Key=object_key,
                Range=range_header,
            )
            content = response["Body"].get_raw_stream().read(length)
        except AppError:
            raise
        except Exception as exc:
            code = getattr(exc, "code", "")
            if code in {"NoSuchKey", "NoSuchObject"}:
                raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体文件不存在") from exc
            raise AppError(
                status_code=502,
                code=STORAGE_UNAVAILABLE,
                message="对象存储不可用",
            ) from exc

        return StoredMediaObject(
            content=content,
            content_type=info.content_type,
            total_size=info.total_size,
        )


MinioMediaStorageClient = S3CompatibleMediaStorageClient

_media_storage_client: MediaStorageClient | None = None


def get_media_storage_client() -> MediaStorageClient:
    global _media_storage_client
    if _media_storage_client is None:
        if settings.effective_object_storage_provider() == "tencent-cos":
            _media_storage_client = TencentCOSMediaStorageClient()
        else:
            _media_storage_client = S3CompatibleMediaStorageClient()
    return _media_storage_client


def set_media_storage_client(client: MediaStorageClient | None) -> None:
    global _media_storage_client
    _media_storage_client = client


def build_upload_object_key(prefix: str, resource_type: str, content_type: str | None) -> str:
    extension = _extension_for_content_type(content_type)
    return build_object_key(prefix, resource_type, extension)


def build_image_upload_object_key(resource_type: str, content_type: str | None) -> str:
    prefix = settings.object_storage_prefix_images.rstrip("/")
    return build_upload_object_key(prefix, resource_type, content_type)


def build_video_upload_object_key(resource_type: str, content_type: str | None) -> str:
    prefix = settings.object_storage_prefix_video.rstrip("/")
    return build_upload_object_key(prefix, resource_type, content_type)


def build_file_upload_object_key(resource_type: str, content_type: str | None) -> str:
    prefix = settings.object_storage_prefix_files.rstrip("/")
    return build_upload_object_key(prefix, resource_type, content_type)


def validate_object_key(object_key: str) -> PurePosixPath:
    key = object_key.strip()
    if not key or key.startswith("/") or "\\" in key or "//" in key:
        raise ValueError("Invalid media object key")

    path = PurePosixPath(key)
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("Invalid media object key")
    return path


def resolve_media_path(object_key: str) -> PurePosixPath:
    try:
        return validate_object_key(object_key)
    except ValueError as exc:
        raise AppError(
            status_code=400,
            code=MEDIA_INVALID_OBJECT_KEY,
            message="非法媒体对象路径",
        ) from exc


def _is_video_media_type(media_type: str | None) -> bool:
    return bool(media_type and media_type.startswith("video/"))


def _range_not_satisfiable_response(total_size: int) -> Response:
    return Response(
        status_code=416,
        headers={
            "Accept-Ranges": "bytes",
            "Content-Range": f"bytes */{total_size}",
            "Content-Length": "0",
        },
    )


def _parse_byte_range(range_header: str, total_size: int) -> tuple[int, int] | None:
    value = range_header.strip()
    if not value.startswith("bytes=") or "," in value:
        return None
    start_text, separator, end_text = value[6:].partition("-")
    if not separator:
        return None
    start_text = start_text.strip()
    end_text = end_text.strip()

    if not start_text:
        if not end_text.isdigit():
            return None
        suffix_length = int(end_text)
        if suffix_length <= 0:
            return None
        start = max(total_size - suffix_length, 0)
        end = total_size - 1
    else:
        if not start_text.isdigit() or (end_text and not end_text.isdigit()):
            return None
        start = int(start_text)
        end = int(end_text) if end_text else total_size - 1

    if total_size <= 0 or start >= total_size or end < start:
        return None
    return start, min(end, total_size - 1)


UploadTimingContext = dict[str, Any]


def _elapsed_ms(started_at: float) -> int:
    return round((perf_counter() - started_at) * 1000)


def _log_upload_stage(
    timing: UploadTimingContext | None,
    stage: str,
    stage_started_at: float,
    **extra: object,
) -> None:
    if timing is None:
        return
    started_at = float(timing["started_at"])
    logger.info(
        (
            "media_upload_timing upload_type=%s stage=%s elapsed_ms=%s stage_ms=%s "
            "object_key=%s file_name=%s content_type=%s size_bytes=%s max_size_mb=%s "
            "provider=%s endpoint=%s bucket=%s region=%s path_style=%s auto_create_bucket=%s"
        ),
        timing.get("upload_type"),
        stage,
        _elapsed_ms(started_at),
        _elapsed_ms(stage_started_at),
        timing.get("object_key"),
        timing.get("file_name"),
        timing.get("content_type"),
        extra.get("size_bytes", timing.get("size_bytes")),
        timing.get("max_size_mb"),
        timing.get("provider"),
        timing.get("endpoint"),
        timing.get("bucket"),
        timing.get("region"),
        timing.get("path_style"),
        timing.get("auto_create_bucket"),
    )


async def save_upload_file(
    file: UploadFile,
    object_key: str,
    max_size_mb: int,
    timing: UploadTimingContext | None = None,
) -> int:
    resolve_media_path(object_key)
    stage_started_at = perf_counter()
    _log_upload_stage(timing, "file_read_start", stage_started_at)
    content = await file.read()
    _log_upload_stage(timing, "file_read_done", stage_started_at, size_bytes=len(content))
    max_size_bytes = max_size_mb * 1024 * 1024
    stage_started_at = perf_counter()
    if len(content) > max_size_bytes:
        _log_upload_stage(timing, "validation_failed_size", stage_started_at, size_bytes=len(content))
        raise AppError(status_code=400, code=FILE_SIZE_EXCEEDED, message="文件大小超限")
    _log_upload_stage(timing, "validation_done", stage_started_at, size_bytes=len(content))
    stage_started_at = perf_counter()
    _log_upload_stage(timing, "storage_put_start", stage_started_at, size_bytes=len(content))
    get_media_storage_client().put_object(object_key, content, file.content_type)
    _log_upload_stage(timing, "storage_put_done", stage_started_at, size_bytes=len(content))
    return len(content)


def _resolve_media_object(object_key: str) -> tuple[str, StoredMediaObject]:
    resolve_media_path(object_key)
    client = get_media_storage_client()
    candidate_keys = [object_key]
    legacy_key = map_legacy_object_key(object_key)
    if legacy_key and legacy_key not in candidate_keys:
        candidate_keys.append(legacy_key)

    stored_object: StoredMediaObject | None = None
    resolved_key = object_key
    last_not_found: AppError | None = None
    for candidate_key in candidate_keys:
        try:
            stored_object = client.get_object(candidate_key)
            resolved_key = candidate_key
            break
        except AppError as exc:
            if exc.code != MEDIA_NOT_FOUND:
                raise
            last_not_found = exc

    if stored_object is None:
        if last_not_found is not None:
            raise last_not_found
        raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体文件不存在")
    return resolved_key, stored_object


def _resolve_media_info(object_key: str) -> tuple[str, MediaObjectInfo]:
    resolve_media_path(object_key)
    client = get_media_storage_client()
    candidate_keys = [object_key]
    legacy_key = map_legacy_object_key(object_key)
    if legacy_key and legacy_key not in candidate_keys:
        candidate_keys.append(legacy_key)

    last_not_found: AppError | None = None
    for candidate_key in candidate_keys:
        try:
            return candidate_key, client.get_object_info(candidate_key)
        except AppError as exc:
            if exc.code != MEDIA_NOT_FOUND:
                raise
            last_not_found = exc

    if last_not_found is not None:
        raise last_not_found
    raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体文件不存在")


def get_media_file_response(object_key: str, range_header: str | None = None) -> Response:
    if range_header:
        resolved_key, info = _resolve_media_info(object_key)
        media_type = info.content_type or mimetypes.guess_type(resolved_key)[0]
        if _is_video_media_type(media_type):
            total_size = info.total_size
            byte_range = _parse_byte_range(range_header, total_size)
            if byte_range is None:
                return _range_not_satisfiable_response(total_size)

            start, end = byte_range
            length = end - start + 1
            ranged_object = get_media_storage_client().get_object_range(resolved_key, start, length)
            range_media_type = ranged_object.content_type or media_type
            return Response(
                content=ranged_object.content,
                status_code=206,
                media_type=range_media_type,
                headers={
                    "Accept-Ranges": "bytes",
                    "Content-Range": f"bytes {start}-{end}/{total_size}",
                    "Content-Length": str(length),
                },
            )

    resolved_key, stored_object = _resolve_media_object(object_key)
    media_type = (
        _detect_content_type(stored_object.content)
        or stored_object.content_type
        or mimetypes.guess_type(resolved_key)[0]
    )
    return Response(content=stored_object.content, media_type=media_type)


def get_media_head_response(object_key: str, range_header: str | None = None) -> Response:
    resolved_key, info = _resolve_media_info(object_key)
    media_type = info.content_type or mimetypes.guess_type(resolved_key)[0] or "application/octet-stream"
    headers = {"Content-Length": str(info.total_size)}

    if _is_video_media_type(media_type):
        headers["Accept-Ranges"] = "bytes"
        if range_header:
            byte_range = _parse_byte_range(range_header, info.total_size)
            if byte_range is None:
                return _range_not_satisfiable_response(info.total_size)
            start, end = byte_range
            headers["Content-Range"] = f"bytes {start}-{end}/{info.total_size}"
            headers["Content-Length"] = str(end - start + 1)
            return Response(content=b"", status_code=206, media_type=media_type, headers=headers)

    return Response(content=b"", media_type=media_type, headers=headers)
