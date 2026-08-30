"""Helpers for formalizing pending media under business object ids."""

from __future__ import annotations

from pathlib import PurePosixPath

from app.core.exceptions import AppError
from app.modules.media.storage import (
    get_media_storage_client,
    resolve_media_path,
    same_directory_display_object_key,
    same_directory_thumbnail_object_key,
)


def is_pending_business_media_key(object_key: str) -> bool:
    key = str(resolve_media_path(object_key))
    return "/pending/" in key


def deterministic_business_media_key(
    *,
    object_key: str,
    resource_type: str,
    business_id: int | str,
    usage: str,
    prefix: str,
) -> str:
    key = str(resolve_media_path(object_key))
    filename = PurePosixPath(key).name
    return f"{prefix}/default/{resource_type}/{business_id}/{filename}"


def formalize_business_media_object(
    *,
    object_key: str,
    resource_type: str,
    business_id: int | str,
    usage: str,
    media_kind: str,
) -> str:
    source_key = str(resolve_media_path(object_key))
    if not is_pending_business_media_key(source_key):
        return source_key

    if media_kind == "image":
        target_key = deterministic_business_media_key(
            object_key=source_key,
            resource_type=resource_type,
            business_id=business_id,
            usage=usage,
            prefix="images",
        )
    elif media_kind == "file":
        target_key = deterministic_business_media_key(
            object_key=source_key,
            resource_type=resource_type,
            business_id=business_id,
            usage=usage,
            prefix="files",
        )
    elif media_kind == "video":
        target_key = deterministic_business_media_key(
            object_key=source_key,
            resource_type=resource_type,
            business_id=business_id,
            usage=usage,
            prefix="videos",
        )
    else:
        target_key = deterministic_business_media_key(
            object_key=source_key,
            resource_type=resource_type,
            business_id=business_id,
            usage=usage,
            prefix=media_kind,
        )

    storage = get_media_storage_client()
    original = storage.get_object(source_key)
    storage.put_object(target_key, original.content, original.content_type)

    if media_kind == "image":
        for source_variant, target_variant in (
            (same_directory_thumbnail_object_key(source_key), same_directory_thumbnail_object_key(target_key)),
            (same_directory_display_object_key(source_key), same_directory_display_object_key(target_key)),
        ):
            try:
                variant = storage.get_object(source_variant)
            except AppError:
                continue
            storage.put_object(target_variant, variant.content, variant.content_type)

    return target_key
