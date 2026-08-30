"""Object key generation utilities for MinIO single-bucket storage."""

from uuid import uuid4


def _normalize_segment(value: str | int, *, name: str) -> str:
    segment = str(value).strip().strip("/")
    if not segment or segment in {".", ".."} or "/" in segment or "\\" in segment:
        raise ValueError(f"Invalid media object key {name}")
    return segment


def _normalize_resource_type(resource_type: str) -> str:
    segments = [
        _normalize_segment(segment, name="resource_type")
        for segment in resource_type.strip("/").split("/")
        if segment
    ]
    if not segments:
        raise ValueError("Invalid media object key resource_type")
    return "/".join(segments)


def build_object_key(prefix: str, resource_type: str, extension: str, tenant_id: str = "default") -> str:
    """Build a normalized object key.

    Example:
        images/default/user-avatars/<uuid>.jpg
    """
    normalized_prefix = prefix if prefix.endswith("/") else f"{prefix}/"
    normalized_extension = extension.lstrip(".").lower()
    normalized_resource_type = _normalize_resource_type(resource_type)
    return (
        f"{normalized_prefix}"
        f"{tenant_id}/"
        f"{normalized_resource_type}/"
        f"{uuid4()}.{normalized_extension}"
    )


def build_business_media_object_key(
    prefix: str,
    resource_type: str,
    business_id: str | int,
    usage: str,
    extension: str,
    tenant_id: str = "default",
) -> str:
    """Build a key under resource/business-id.

    ``usage`` is kept in the signature for existing call sites, but the
    flattened business-media layout no longer writes it as a directory segment.
    """

    normalized_resource_type = _normalize_resource_type(resource_type)
    normalized_business_id = _normalize_segment(business_id, name="business_id")
    _normalize_segment(usage, name="usage")
    return build_object_key(
        prefix,
        f"{normalized_resource_type}/{normalized_business_id}",
        extension,
        tenant_id=tenant_id,
    )


def build_pending_media_object_key(
    prefix: str,
    resource_type: str,
    usage: str,
    extension: str,
    tenant_id: str = "default",
) -> str:
    """Build a key under resource/pending for uploads before an id exists."""

    normalized_resource_type = _normalize_resource_type(resource_type)
    _normalize_segment(usage, name="usage")
    return build_object_key(
        prefix,
        f"{normalized_resource_type}/pending",
        extension,
        tenant_id=tenant_id,
    )
