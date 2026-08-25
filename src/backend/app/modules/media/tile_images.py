"""SKU image object lifecycle helpers."""

from __future__ import annotations

from dataclasses import dataclass
import mimetypes
from pathlib import PurePosixPath

from app.core.exceptions import AppError
from app.modules.media.storage import (
    build_image_upload_object_key,
    DISPLAY_IMAGE_JPEG_QUALITY,
    DISPLAY_IMAGE_MAX_HEIGHT,
    DISPLAY_IMAGE_MAX_WIDTH,
    DISPLAY_IMAGE_WEBP_QUALITY,
    DISPLAY_IMAGE_TARGET_MAX_SIZE_KB,
    generate_image_thumbnail,
    get_media_storage_client,
    same_directory_display_object_key,
    same_directory_thumbnail_object_key,
    resolve_media_path,
)

PENDING_TILE_IMAGE_PREFIX = "images/default/tiles/pending/"


@dataclass(frozen=True)
class FormalizedTileImage:
    source_key: str
    object_key: str
    thumbnail_key: str
    thumbnail_source_key: str
    display_key: str
    display_source_key: str


def is_pending_tile_image_key(object_key: str) -> bool:
    key = str(resolve_media_path(object_key))
    return key.startswith(PENDING_TILE_IMAGE_PREFIX)


def deterministic_formal_tile_image_key(tile_id: int, object_key: str) -> str:
    key = str(resolve_media_path(object_key))
    filename = PurePosixPath(key).name
    return f"images/default/tiles/{tile_id}/{filename}"


def _content_type_for_key(object_key: str, content_type: str | None) -> str | None:
    return content_type or mimetypes.guess_type(object_key)[0]


def _target_key(tile_id: int, source_key: str, target_key: str | None) -> str:
    if target_key:
        return str(resolve_media_path(target_key))
    content_type = mimetypes.guess_type(source_key)[0]
    return build_image_upload_object_key(f"tiles/{tile_id}", content_type)


def formalize_tile_image_object(
    *,
    tile_id: int,
    object_key: str,
    target_key: str | None = None,
    thumbnail_max_size_kb: int = 0,
    display_max_size_kb: int = DISPLAY_IMAGE_TARGET_MAX_SIZE_KB,
) -> FormalizedTileImage:
    source_key = str(resolve_media_path(object_key))
    if not source_key.startswith(PENDING_TILE_IMAGE_PREFIX):
        thumbnail_key = same_directory_thumbnail_object_key(source_key)
        display_key = same_directory_display_object_key(source_key)
        return FormalizedTileImage(
            source_key=source_key,
            object_key=source_key,
            thumbnail_key=thumbnail_key,
            thumbnail_source_key=thumbnail_key,
            display_key=display_key,
            display_source_key=display_key,
        )

    destination_key = _target_key(tile_id, source_key, target_key)
    destination_thumbnail_key = same_directory_thumbnail_object_key(destination_key)
    destination_display_key = same_directory_display_object_key(destination_key)
    source_thumbnail_key = same_directory_thumbnail_object_key(source_key)
    source_display_key = same_directory_display_object_key(source_key)
    storage = get_media_storage_client()

    original = storage.get_object(source_key)
    original_content_type = _content_type_for_key(source_key, original.content_type)
    storage.put_object(destination_key, original.content, original_content_type)

    try:
        thumbnail = storage.get_object(source_thumbnail_key)
        thumbnail_source_key = source_thumbnail_key
    except AppError:
        try:
            generated_thumbnail = generate_image_thumbnail(
                original.content,
                original_content_type,
                target_max_size_kb=thumbnail_max_size_kb,
            )
        except (RuntimeError, ValueError, OSError):
            thumbnail = None
            thumbnail_source_key = source_key
        else:
            thumbnail = type(original)(generated_thumbnail.content, generated_thumbnail.content_type)
            thumbnail_source_key = source_key
    if thumbnail is not None:
        thumbnail_content_type = _content_type_for_key(source_key, thumbnail.content_type)
        storage.put_object(destination_thumbnail_key, thumbnail.content, thumbnail_content_type)

    try:
        display = storage.get_object(source_display_key)
        display_source_key = source_display_key
    except AppError:
        try:
            generated_display = generate_image_thumbnail(
                original.content,
                original_content_type,
                max_width=DISPLAY_IMAGE_MAX_WIDTH,
                max_height=DISPLAY_IMAGE_MAX_HEIGHT,
                jpeg_quality=DISPLAY_IMAGE_JPEG_QUALITY,
                webp_quality=DISPLAY_IMAGE_WEBP_QUALITY,
                target_max_size_kb=display_max_size_kb,
            )
        except (RuntimeError, ValueError, OSError):
            display = None
            display_source_key = source_key
        else:
            display = type(original)(generated_display.content, generated_display.content_type)
            display_source_key = source_key
    if display is not None:
        display_content_type = _content_type_for_key(source_key, display.content_type)
        storage.put_object(destination_display_key, display.content, display_content_type)

    return FormalizedTileImage(
        source_key=source_key,
        object_key=destination_key,
        thumbnail_key=destination_thumbnail_key,
        thumbnail_source_key=thumbnail_source_key,
        display_key=destination_display_key,
        display_source_key=display_source_key,
    )
