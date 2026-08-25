"""Media storage adapters and controlled media object access."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import hashlib
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
IMAGE_CACHE_CONTROL = "public, max-age=604800, stale-while-revalidate=86400"
DISPLAY_IMAGE_MAX_WIDTH = 1600
DISPLAY_IMAGE_MAX_HEIGHT = 1600
DISPLAY_IMAGE_TARGET_MAX_SIZE_KB = 768
DISPLAY_IMAGE_JPEG_QUALITY = 86
DISPLAY_IMAGE_WEBP_QUALITY = 86
WEBP_DERIVATIVE_CONTENT_TYPE = "image/webp"
WEBP_DERIVATIVE_FORMAT = "WEBP"
WEBP_DERIVATIVE_EXTENSION = "webp"
WEBP_ORIGINAL_FALLBACK_EXTENSIONS = ("jpg", "jpeg", "png", "webp")
OBJECT_MISSING_ERROR_CODES = {"NoSuchKey", "NoSuchObject", "NoSuchResource"}

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


def _object_storage_error_code(exc: BaseException) -> str:
    for accessor_name in ("get_error_code", "get_code"):
        accessor = getattr(exc, accessor_name, None)
        if callable(accessor):
            try:
                code = accessor()
            except Exception:
                code = None
            if code:
                return str(code)
    return str(getattr(exc, "code", "") or "")


def _is_object_missing_error(exc: BaseException) -> bool:
    return _object_storage_error_code(exc) in OBJECT_MISSING_ERROR_CODES


@dataclass(frozen=True)
class StoredMediaObject:
    content: bytes
    content_type: str | None = None
    total_size: int | None = None


@dataclass(frozen=True)
class MediaObjectInfo:
    content_type: str | None
    total_size: int


@dataclass(frozen=True)
class ImageThumbnailResult:
    content: bytes
    content_type: str
    width: int
    height: int
    original_width: int
    original_height: int
    original_size: int
    size: int
    resized: bool


def _image_format_for_content_type(content_type: str | None) -> tuple[str, str] | None:
    normalized = (content_type or "").lower().split(";", 1)[0].strip()
    if normalized in {"image/jpeg", "image/jpg"}:
        return "JPEG", "image/jpeg"
    if normalized == "image/png":
        return "PNG", "image/png"
    if normalized == "image/webp":
        return "WEBP", "image/webp"
    return None


def generate_image_thumbnail(
    content: bytes,
    content_type: str | None,
    *,
    max_width: int = 480,
    max_height: int = 480,
    jpeg_quality: int = 82,
    webp_quality: int = 82,
    target_max_size_kb: int = 0,
    output_format: str = WEBP_DERIVATIVE_FORMAT,
) -> ImageThumbnailResult:
    """Generate a WebP image variant without upscaling small images."""

    image_format = _image_format_for_content_type(content_type) or _image_format_for_content_type(
        _detect_content_type(content)
    )
    if image_format is None:
        raise ValueError("unsupported image content type")

    try:
        from PIL import Image, ImageOps, UnidentifiedImageError
    except ModuleNotFoundError as exc:
        raise RuntimeError("Pillow is required to generate image thumbnails") from exc

    try:
        with Image.open(BytesIO(content)) as image:
            image = ImageOps.exif_transpose(image)
            original_width, original_height = image.size
            thumbnail = image.copy()
            thumbnail.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            resized = thumbnail.size != (original_width, original_height)
            _, source_content_type = image_format
            output_format = output_format.upper()
            output_content_type = (
                WEBP_DERIVATIVE_CONTENT_TYPE if output_format == WEBP_DERIVATIVE_FORMAT else source_content_type
            )
            target_size_bytes = max(0, int(target_max_size_kb or 0)) * 1024
            thumbnail, thumbnail_content = _encode_thumbnail_with_target(
                thumbnail=thumbnail,
                output_format=output_format,
                jpeg_quality=jpeg_quality,
                webp_quality=webp_quality,
                target_size_bytes=target_size_bytes,
                max_width=max_width,
                max_height=max_height,
            )
            if target_size_bytes and len(thumbnail_content) > target_size_bytes:
                logger.warning(
                    "thumbnail target not reached: content_type=%s target=%s actual=%s size=%sx%s",
                    output_content_type,
                    target_size_bytes,
                    len(thumbnail_content),
                    thumbnail.size[0],
                    thumbnail.size[1],
                )
    except UnidentifiedImageError as exc:
        raise ValueError("invalid image content") from exc

    return ImageThumbnailResult(
        content=thumbnail_content,
        content_type=output_content_type,
        width=thumbnail.size[0],
        height=thumbnail.size[1],
        original_width=original_width,
        original_height=original_height,
        original_size=len(content),
        size=len(thumbnail_content),
        resized=resized,
    )


def _thumbnail_save_kwargs(
    output_format: str,
    *,
    jpeg_quality: int,
    webp_quality: int,
) -> dict[str, object]:
    if output_format == "JPEG":
        return {
            "format": "JPEG",
            "quality": jpeg_quality,
            "optimize": True,
            "progressive": True,
        }
    if output_format == "WEBP":
        return {"format": "WEBP", "quality": webp_quality, "method": 6}
    return {"format": "PNG", "optimize": True}


def _save_thumbnail_bytes(thumbnail: Any, output_format: str, save_kwargs: dict[str, object]) -> bytes:
    if output_format == "JPEG" and thumbnail.mode not in {"RGB", "L"}:
        thumbnail = thumbnail.convert("RGB")
    if output_format == "WEBP" and thumbnail.mode not in {"RGB", "RGBA"}:
        thumbnail = thumbnail.convert("RGBA" if "A" in thumbnail.getbands() else "RGB")
    output = BytesIO()
    thumbnail.save(output, **save_kwargs)
    return output.getvalue()


def _encode_thumbnail_with_target(
    *,
    thumbnail: Any,
    output_format: str,
    jpeg_quality: int,
    webp_quality: int,
    target_size_bytes: int,
    max_width: int,
    max_height: int,
) -> tuple[Any, bytes]:
    save_kwargs = _thumbnail_save_kwargs(
        output_format,
        jpeg_quality=jpeg_quality,
        webp_quality=webp_quality,
    )
    best_image = thumbnail
    best_content = _save_thumbnail_bytes(thumbnail, output_format, save_kwargs)
    if target_size_bytes <= 0 or len(best_content) <= target_size_bytes:
        return best_image, best_content

    if output_format in {"JPEG", "WEBP"}:
        quality_key = "quality"
        default_quality = jpeg_quality if output_format == "JPEG" else webp_quality
        start_quality = int(save_kwargs.get(quality_key, default_quality))
        for quality in range(min(start_quality, 78), 34, -8):
            candidate_kwargs = dict(save_kwargs)
            candidate_kwargs[quality_key] = quality
            candidate_content = _save_thumbnail_bytes(thumbnail, output_format, candidate_kwargs)
            if len(candidate_content) < len(best_content):
                best_content = candidate_content
                best_image = thumbnail
            if len(candidate_content) <= target_size_bytes:
                return thumbnail, candidate_content

    min_edge = 160
    current_width, current_height = thumbnail.size
    while max(current_width, current_height) > min_edge:
        scale = 0.85
        current_width = max(min_edge, int(current_width * scale))
        current_height = max(min_edge, int(current_height * scale))
        if (current_width, current_height) == thumbnail.size:
            break
        candidate = thumbnail.copy()
        candidate.thumbnail((min(current_width, max_width), min(current_height, max_height)))
        candidate_content = _save_thumbnail_bytes(candidate, output_format, save_kwargs)
        if len(candidate_content) < len(best_content):
            best_content = candidate_content
            best_image = candidate
        if len(candidate_content) <= target_size_bytes:
            return candidate, candidate_content
        thumbnail = candidate
    return best_image, best_content


class MediaStorageClient(Protocol):
    def put_object(self, object_key: str, content: bytes, content_type: str | None) -> None:
        """Persist object bytes under the configured object key."""

    def get_object(self, object_key: str) -> StoredMediaObject:
        """Return object bytes and optional content type."""

    def get_object_info(self, object_key: str) -> MediaObjectInfo:
        """Return object metadata without reading object bytes."""

    def get_object_range(self, object_key: str, offset: int, length: int) -> StoredMediaObject:
        """Return a byte range and total object size."""

    def build_direct_read_url(self, object_key: str, expires_seconds: int) -> str:
        """Return an expiring object-storage read URL for controlled direct delivery."""


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
            if _is_object_missing_error(exc):
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
            if _is_object_missing_error(exc):
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
            if _is_object_missing_error(exc):
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

    def build_direct_read_url(self, object_key: str, expires_seconds: int) -> str:
        validate_object_key(object_key)
        try:
            return self._get_client().presigned_get_object(
                settings.effective_object_storage_bucket(),
                object_key,
                expires=timedelta(seconds=expires_seconds),
            )
        except Exception as exc:
            raise AppError(
                status_code=502,
                code=STORAGE_UNAVAILABLE,
                message="对象存储不可用",
            ) from exc


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
            if _is_object_missing_error(exc):
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
            if _is_object_missing_error(exc):
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
            if _is_object_missing_error(exc):
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

    def build_direct_read_url(self, object_key: str, expires_seconds: int) -> str:
        validate_object_key(object_key)
        try:
            return self._get_client().get_presigned_url(
                Method="GET",
                Bucket=settings.effective_object_storage_bucket(),
                Key=object_key,
                Expired=expires_seconds,
            )
        except Exception as exc:
            raise AppError(
                status_code=502,
                code=STORAGE_UNAVAILABLE,
                message="对象存储不可用",
            ) from exc


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


def build_brand_certificate_upload_object_key(content_type: str | None) -> str:
    if content_type and content_type.startswith("image/"):
        return build_image_upload_object_key("brand-certificates", content_type)
    return build_file_upload_object_key("brand-certificates", content_type)


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


def _is_image_media_type(media_type: str | None) -> bool:
    return bool(media_type and media_type.startswith("image/"))


def _cache_headers(resolved_key: str, media_type: str | None, total_size: int | None) -> dict[str, str]:
    if not _is_image_media_type(media_type):
        return {}
    fingerprint = hashlib.sha256(f"{resolved_key}:{total_size or 0}".encode("utf-8")).hexdigest()[:16]
    return {
        "Cache-Control": IMAGE_CACHE_CONTROL,
        "ETag": f'W/"{fingerprint}"',
    }


def _media_key_fingerprint(object_key: str) -> str:
    return hashlib.sha256(object_key.encode("utf-8")).hexdigest()[:12]


def thumbnail_object_key(object_key: str) -> str:
    key = str(resolve_media_path(object_key))
    if key.startswith("thumbnails/"):
        return key
    if key.startswith(("original/", "images/")):
        _, _, rest = key.partition("/")
        return f"thumbnails/{rest}"
    return f"thumbnails/{key}"


def same_directory_thumbnail_object_key(object_key: str, suffix: str = ".thumb") -> str:
    key = str(resolve_media_path(object_key))
    path = PurePosixPath(key)
    derivative_suffix = f"{suffix}.{WEBP_DERIVATIVE_EXTENSION}"
    if path.name.endswith(derivative_suffix):
        return key
    if path.suffix:
        thumbnail_name = f"{path.stem}{derivative_suffix}"
    else:
        thumbnail_name = f"{path.name}{derivative_suffix}"
    return str(path.with_name(thumbnail_name))


def same_directory_display_object_key(object_key: str) -> str:
    return same_directory_thumbnail_object_key(object_key, suffix=".display")


def media_variant_object_key(object_key: str, variant: str) -> str:
    if variant == "original":
        return str(resolve_media_path(object_key))
    if variant == "thumbnail":
        return same_directory_thumbnail_object_key(object_key)
    if variant == "display":
        return same_directory_display_object_key(object_key)
    raise ValueError(f"unsupported media variant: {variant}")


def media_url_for_object_key(object_key: str, *, direct: bool | None = None) -> str:
    key = str(resolve_media_path(object_key))
    should_direct = (
        settings.effective_object_storage_direct_read_enabled() if direct is None else direct
    )
    if not should_direct:
        return f"/media/{key}"
    return get_media_storage_client().build_direct_read_url(
        key,
        settings.effective_object_storage_direct_read_expires_seconds(),
    )


def media_variant_urls(object_key: str, *, direct: bool | None = None) -> dict[str, str]:
    original_key = str(resolve_media_path(object_key))
    thumbnail_key = media_variant_object_key(original_key, "thumbnail")
    display_key = media_variant_object_key(original_key, "display")
    return {
        "original_url": media_url_for_object_key(original_key, direct=direct),
        "thumbnail_url": media_url_for_object_key(thumbnail_key, direct=direct),
        "display_url": media_url_for_object_key(display_key, direct=direct),
    }


def _thumbnail_origin_candidates(object_key: str) -> list[str]:
    if not object_key.startswith("thumbnails/"):
        return []
    rest = object_key.removeprefix("thumbnails/")
    candidates = [rest]
    if not rest.startswith(("original/", "images/")):
        candidates.extend([f"original/{rest}", f"images/{rest}"])
    return candidates


def _same_directory_variant_origin_candidates(object_key: str) -> list[str]:
    try:
        key = str(resolve_media_path(object_key))
    except AppError:
        return []
    path = PurePosixPath(key)
    suffix = path.suffix
    if not suffix:
        return []
    for marker in (".thumb", ".display"):
        if path.stem.endswith(marker):
            original_stem = path.stem.removesuffix(marker)
            if suffix == f".{WEBP_DERIVATIVE_EXTENSION}":
                return [
                    str(path.with_name(f"{original_stem}.{extension}"))
                    for extension in WEBP_ORIGINAL_FALLBACK_EXTENSIONS
                ]
            return [str(path.with_name(f"{original_stem}{suffix}"))]
    return []


def _resolve_candidate_keys(object_key: str) -> list[str]:
    candidate_keys = [object_key]
    for thumbnail_fallback in _same_directory_variant_origin_candidates(object_key):
        if thumbnail_fallback not in candidate_keys:
            candidate_keys.append(thumbnail_fallback)
    for thumbnail_fallback in _thumbnail_origin_candidates(object_key):
        if thumbnail_fallback not in candidate_keys:
            candidate_keys.append(thumbnail_fallback)
    legacy_key = map_legacy_object_key(object_key)
    if legacy_key and legacy_key not in candidate_keys:
        candidate_keys.append(legacy_key)
    return candidate_keys


def _log_media_read(
    *,
    object_key: str,
    resolved_key: str | None,
    status_code: int,
    started_at: float,
    media_type: str | None = None,
    total_size: int | None = None,
    range_requested: bool = False,
    cacheable: bool = False,
) -> None:
    fallback_used = bool(resolved_key and resolved_key != object_key)
    logger.info(
        (
            "media_read status=%s elapsed_ms=%s object_key_hash=%s resolved_key_hash=%s "
            "media_type=%s size_bytes=%s range=%s cacheable=%s fallback=%s"
        ),
        status_code,
        _elapsed_ms(started_at),
        _media_key_fingerprint(object_key),
        _media_key_fingerprint(resolved_key) if resolved_key else None,
        media_type,
        total_size,
        range_requested,
        cacheable,
        fallback_used,
    )


def _observability_headers(requested_key: str, resolved_key: str) -> dict[str, str]:
    return {
        "X-Media-Resolved-Key-Hash": _media_key_fingerprint(resolved_key),
        "X-Media-Fallback": "1" if requested_key != resolved_key else "0",
    }


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
    thumbnail_key: str | None = None,
    thumbnail_max_size_kb: int = 0,
    display_key: str | None = None,
    display_max_size_kb: int = DISPLAY_IMAGE_TARGET_MAX_SIZE_KB,
) -> int:
    resolve_media_path(object_key)
    if thumbnail_key is not None:
        resolve_media_path(thumbnail_key)
    if display_key is not None:
        resolve_media_path(display_key)
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
    client = get_media_storage_client()
    client.put_object(object_key, content, file.content_type)
    _log_upload_stage(timing, "storage_put_done", stage_started_at, size_bytes=len(content))
    if thumbnail_key:
        _put_generated_image_variant(
            client=client,
            content=content,
            content_type=file.content_type,
            object_key=object_key,
            variant_key=thumbnail_key,
            variant="thumbnail",
            timing=timing,
            target_max_size_kb=thumbnail_max_size_kb,
        )
    if display_key:
        _put_generated_image_variant(
            client=client,
            content=content,
            content_type=file.content_type,
            object_key=object_key,
            variant_key=display_key,
            variant="display",
            timing=timing,
            max_width=DISPLAY_IMAGE_MAX_WIDTH,
            max_height=DISPLAY_IMAGE_MAX_HEIGHT,
            jpeg_quality=DISPLAY_IMAGE_JPEG_QUALITY,
            webp_quality=DISPLAY_IMAGE_WEBP_QUALITY,
            target_max_size_kb=display_max_size_kb,
        )
    return len(content)


def _put_generated_image_variant(
    *,
    client: MediaStorageClient,
    content: bytes,
    content_type: str | None,
    object_key: str,
    variant_key: str,
    variant: str,
    timing: UploadTimingContext | None,
    max_width: int = 480,
    max_height: int = 480,
    jpeg_quality: int = 82,
    webp_quality: int = 82,
    target_max_size_kb: int = 0,
) -> None:
    stage_started_at = perf_counter()
    _log_upload_stage(timing, f"{variant}_put_start", stage_started_at, size_bytes=len(content))
    try:
        generated = generate_image_thumbnail(
            content,
            content_type,
            max_width=max_width,
            max_height=max_height,
            jpeg_quality=jpeg_quality,
            webp_quality=webp_quality,
            target_max_size_kb=target_max_size_kb,
        )
    except (RuntimeError, ValueError, OSError) as exc:
        logger.warning(
            "media_image_variant_generation_failed object_key_hash=%s variant=%s variant_key_hash=%s reason=%s",
            _media_key_fingerprint(object_key),
            variant,
            _media_key_fingerprint(variant_key),
            exc.__class__.__name__,
        )
        _log_upload_stage(timing, f"{variant}_generation_skipped", stage_started_at, size_bytes=0)
        return
    client.put_object(variant_key, generated.content, generated.content_type)
    _log_upload_stage(
        timing,
        f"{variant}_put_done",
        stage_started_at,
        size_bytes=generated.size,
        width=generated.width,
        height=generated.height,
        original_width=generated.original_width,
        original_height=generated.original_height,
        resized=generated.resized,
    )


def _resolve_media_object(object_key: str) -> tuple[str, StoredMediaObject]:
    resolve_media_path(object_key)
    client = get_media_storage_client()
    candidate_keys = _resolve_candidate_keys(object_key)

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
    candidate_keys = _resolve_candidate_keys(object_key)

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
    started_at = perf_counter()
    try:
        if range_header:
            resolved_key, info = _resolve_media_info(object_key)
            media_type = info.content_type or mimetypes.guess_type(resolved_key)[0]
            if _is_video_media_type(media_type):
                total_size = info.total_size
                byte_range = _parse_byte_range(range_header, total_size)
                if byte_range is None:
                    _log_media_read(
                        object_key=object_key,
                        resolved_key=resolved_key,
                        status_code=416,
                        started_at=started_at,
                        media_type=media_type,
                        total_size=total_size,
                        range_requested=True,
                    )
                    return _range_not_satisfiable_response(total_size)

                start, end = byte_range
                length = end - start + 1
                ranged_object = get_media_storage_client().get_object_range(resolved_key, start, length)
                range_media_type = ranged_object.content_type or media_type
                _log_media_read(
                    object_key=object_key,
                    resolved_key=resolved_key,
                    status_code=206,
                    started_at=started_at,
                    media_type=range_media_type,
                    total_size=total_size,
                    range_requested=True,
                )
                return Response(
                    content=ranged_object.content,
                    status_code=206,
                    media_type=range_media_type,
                    headers={
                        "Accept-Ranges": "bytes",
                        "Content-Range": f"bytes {start}-{end}/{total_size}",
                        "Content-Length": str(length),
                        **_observability_headers(object_key, resolved_key),
                    },
                )

        resolved_key, stored_object = _resolve_media_object(object_key)
        media_type = (
            _detect_content_type(stored_object.content)
            or stored_object.content_type
            or mimetypes.guess_type(resolved_key)[0]
        )
        total_size = stored_object.total_size or len(stored_object.content)
        headers = {
            **_cache_headers(resolved_key, media_type, total_size),
            **_observability_headers(object_key, resolved_key),
        }
        _log_media_read(
            object_key=object_key,
            resolved_key=resolved_key,
            status_code=200,
            started_at=started_at,
            media_type=media_type,
            total_size=total_size,
            cacheable=bool(headers),
        )
        return Response(content=stored_object.content, media_type=media_type, headers=headers)
    except AppError as exc:
        _log_media_read(
            object_key=object_key,
            resolved_key=None,
            status_code=exc.status_code,
            started_at=started_at,
            media_type=None,
            total_size=None,
            range_requested=bool(range_header),
        )
        raise


def get_media_head_response(object_key: str, range_header: str | None = None) -> Response:
    resolved_key, info = _resolve_media_info(object_key)
    media_type = info.content_type or mimetypes.guess_type(resolved_key)[0] or "application/octet-stream"
    headers = {
        "Content-Length": str(info.total_size),
        **_cache_headers(resolved_key, media_type, info.total_size),
        **_observability_headers(object_key, resolved_key),
    }

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
