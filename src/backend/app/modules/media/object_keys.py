"""Object key generation utilities for MinIO single-bucket storage."""

from datetime import datetime, timezone
from uuid import uuid4


def build_object_key(prefix: str, resource_type: str, extension: str, tenant_id: str = "default") -> str:
    """Build a normalized object key.

    Example:
        original/default/tiles/2026/06/<uuid>.jpg
    """
    now = datetime.now(timezone.utc)
    normalized_prefix = prefix if prefix.endswith("/") else f"{prefix}/"
    normalized_extension = extension.lstrip(".").lower()
    return (
        f"{normalized_prefix}"
        f"{tenant_id}/"
        f"{resource_type}/"
        f"{now:%Y}/"
        f"{now:%m}/"
        f"{uuid4()}.{normalized_extension}"
    )
