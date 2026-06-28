"""MinIO-backed media storage and controlled media object access."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
import mimetypes
from pathlib import PurePosixPath
from typing import Protocol

from fastapi import UploadFile
from fastapi.responses import Response

from app.core.config import settings
from app.core.error_codes import FILE_SIZE_EXCEEDED, STORAGE_UNAVAILABLE
from app.core.exceptions import AppError
from app.modules.media.object_keys import build_object_key

MEDIA_NOT_FOUND = 40404
MEDIA_INVALID_OBJECT_KEY = 40040

_EXTENSIONS_BY_TYPE = {
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
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


@dataclass(frozen=True)
class StoredMediaObject:
    content: bytes
    content_type: str | None = None


class MediaStorageClient(Protocol):
    def put_object(self, object_key: str, content: bytes, content_type: str | None) -> None:
        """Persist object bytes under the configured object key."""

    def get_object(self, object_key: str) -> StoredMediaObject:
        """Return object bytes and optional content type."""


class MinioMediaStorageClient:
    def __init__(self) -> None:
        self._client = None

    def _get_client(self):
        if self._client is None:
            from minio import Minio

            self._client = Minio(
                settings.minio_endpoint,
                access_key=settings.minio_access_key,
                secret_key=settings.minio_secret_key,
                secure=settings.minio_secure,
            )
        return self._client

    def _ensure_bucket(self) -> None:
        client = self._get_client()
        try:
            if not client.bucket_exists(settings.minio_bucket):
                client.make_bucket(settings.minio_bucket)
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
                settings.minio_bucket,
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
            response = client.get_object(settings.minio_bucket, object_key)
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

        content_type, _ = mimetypes.guess_type(object_key)
        return StoredMediaObject(content=content, content_type=content_type)


_media_storage_client: MediaStorageClient | None = None


def get_media_storage_client() -> MediaStorageClient:
    global _media_storage_client
    if _media_storage_client is None:
        _media_storage_client = MinioMediaStorageClient()
    return _media_storage_client


def set_media_storage_client(client: MediaStorageClient | None) -> None:
    global _media_storage_client
    _media_storage_client = client


def build_upload_object_key(prefix: str, resource_type: str, content_type: str | None) -> str:
    extension = _extension_for_content_type(content_type)
    return build_object_key(prefix, resource_type, extension)


def build_image_upload_object_key(resource_type: str, content_type: str | None) -> str:
    prefix = settings.minio_prefix_images.rstrip("/")
    return build_upload_object_key(prefix, resource_type, content_type)


def build_video_upload_object_key(resource_type: str, content_type: str | None) -> str:
    prefix = settings.minio_prefix_video.rstrip("/")
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


async def save_upload_file(file: UploadFile, object_key: str, max_size_mb: int) -> None:
    resolve_media_path(object_key)
    content = await file.read()
    max_size_bytes = max_size_mb * 1024 * 1024
    if len(content) > max_size_bytes:
        raise AppError(status_code=400, code=FILE_SIZE_EXCEEDED, message="文件大小超限")
    get_media_storage_client().put_object(object_key, content, file.content_type)


def get_media_file_response(object_key: str) -> Response:
    resolve_media_path(object_key)
    stored_object = get_media_storage_client().get_object(object_key)
    media_type = stored_object.content_type or mimetypes.guess_type(object_key)[0]
    return Response(content=stored_object.content, media_type=media_type)
