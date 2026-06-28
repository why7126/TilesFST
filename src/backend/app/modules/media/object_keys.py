"""Object key generation utilities for MinIO single-bucket storage."""

from uuid import uuid4


def build_object_key(prefix: str, resource_type: str, extension: str, tenant_id: str = "default") -> str:
    """Build a normalized object key.

    Example:
        images/default/user/avatars/<uuid>.jpg
    """
    normalized_prefix = prefix if prefix.endswith("/") else f"{prefix}/"
    normalized_extension = extension.lstrip(".").lower()
    normalized_resource_type = resource_type.strip("/")
    return (
        f"{normalized_prefix}"
        f"{tenant_id}/"
        f"{normalized_resource_type}/"
        f"{uuid4()}.{normalized_extension}"
    )
