from __future__ import annotations

from app.core.config import settings
from app.core.exceptions import AppError
from app.modules.media.storage import (
    MEDIA_NOT_FOUND,
    S3CompatibleMediaStorageClient,
    StoredMediaObject,
    get_media_file_response,
    set_media_storage_client,
)


class _MemoryMediaStorageClient:
    def __init__(self, content: bytes, content_type: str | None = None) -> None:
        self.objects = {"default": StoredMediaObject(content=content, content_type=content_type)}
        self.requested_keys: list[str] = []

    @classmethod
    def from_objects(cls, objects: dict[str, StoredMediaObject]) -> "_MemoryMediaStorageClient":
        client = cls(b"")
        client.objects = objects
        return client

    def put_object(self, object_key: str, content: bytes, content_type: str | None) -> None:
        self.objects[object_key] = StoredMediaObject(content=content, content_type=content_type)

    def get_object(self, object_key: str) -> StoredMediaObject:
        self.requested_keys.append(object_key)
        if object_key in self.objects:
            return self.objects[object_key]
        if "default" in self.objects:
            return self.objects["default"]
        raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体文件不存在")


class _FakeObjectStorageBackend:
    def __init__(self, bucket_exists: bool) -> None:
        self.bucket_exists_result = bucket_exists
        self.bucket_exists_calls: list[str] = []
        self.created_buckets: list[str] = []
        self.puts: list[tuple[str, str, bytes, str | None]] = []

    def bucket_exists(self, bucket: str) -> bool:
        self.bucket_exists_calls.append(bucket)
        return self.bucket_exists_result or bucket in self.created_buckets

    def make_bucket(self, bucket: str) -> None:
        self.created_buckets.append(bucket)

    def put_object(self, bucket: str, object_key: str, stream, length: int, content_type: str | None) -> None:
        self.puts.append((bucket, object_key, stream.read(length), content_type))


def test_media_file_response_detects_webp_content_even_when_key_suffix_is_png() -> None:
    webp_bytes = b"RIFF\x10\x00\x00\x00WEBPVP8X" + b"\x00" * 16
    set_media_storage_client(_MemoryMediaStorageClient(webp_bytes))
    try:
        response = get_media_file_response("images/default/tiles/1/wrong-suffix.png")
    finally:
        set_media_storage_client(None)

    assert response.media_type == "image/webp"


def test_media_file_response_falls_back_to_migrated_legacy_tile_image_key() -> None:
    png_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16
    storage = _MemoryMediaStorageClient.from_objects(
        {
            "images/default/tiles/2/816a4aea-97dc-4464-beeb-2354fd42cf9b.png": StoredMediaObject(
                png_bytes,
                "image/png",
            )
        }
    )
    set_media_storage_client(storage)
    try:
        response = get_media_file_response(
            "original/default/tiles/2/images/2026/06/816a4aea-97dc-4464-beeb-2354fd42cf9b.png"
        )
    finally:
        set_media_storage_client(None)

    assert response.media_type == "image/png"
    assert storage.requested_keys == [
        "original/default/tiles/2/images/2026/06/816a4aea-97dc-4464-beeb-2354fd42cf9b.png",
        "images/default/tiles/2/816a4aea-97dc-4464-beeb-2354fd42cf9b.png",
    ]


def test_s3_compatible_storage_auto_creates_bucket_when_enabled() -> None:
    original = {
        "object_storage_bucket": settings.object_storage_bucket,
        "object_storage_provider": settings.object_storage_provider,
        "object_storage_auto_create_bucket": settings.object_storage_auto_create_bucket,
    }
    settings.object_storage_bucket = "tilesfst"
    settings.object_storage_provider = "minio"
    settings.object_storage_auto_create_bucket = True
    backend = _FakeObjectStorageBackend(bucket_exists=False)
    client = S3CompatibleMediaStorageClient()
    client._client = backend
    try:
        client.put_object("images/default/brands/logos/logo.webp", b"logo", "image/webp")
    finally:
        for key, value in original.items():
            setattr(settings, key, value)

    assert backend.created_buckets == ["tilesfst"]
    assert backend.puts == [
        ("tilesfst", "images/default/brands/logos/logo.webp", b"logo", "image/webp")
    ]


def test_s3_compatible_storage_skips_bucket_probe_when_auto_create_disabled() -> None:
    original = {
        "object_storage_bucket": settings.object_storage_bucket,
        "object_storage_provider": settings.object_storage_provider,
        "object_storage_auto_create_bucket": settings.object_storage_auto_create_bucket,
    }
    settings.object_storage_bucket = "tiles-cos"
    settings.object_storage_provider = "tencent-cos"
    settings.object_storage_auto_create_bucket = False
    backend = _FakeObjectStorageBackend(bucket_exists=False)
    client = S3CompatibleMediaStorageClient()
    client._client = backend
    try:
        client.put_object("images/default/brands/logos/logo.webp", b"logo", "image/webp")
    finally:
        for key, value in original.items():
            setattr(settings, key, value)

    assert backend.bucket_exists_calls == []
    assert backend.created_buckets == []
    assert backend.puts == [
        ("tiles-cos", "images/default/brands/logos/logo.webp", b"logo", "image/webp")
    ]


def test_s3_compatible_storage_keeps_provider_endpoint_for_virtual_host_style() -> None:
    original = {
        "object_storage_bucket": settings.object_storage_bucket,
        "object_storage_endpoint": settings.object_storage_endpoint,
        "object_storage_path_style": settings.object_storage_path_style,
    }
    settings.object_storage_bucket = "tiles-cos-123"
    settings.object_storage_endpoint = "cos.ap-guangzhou.myqcloud.com"
    settings.object_storage_path_style = False
    try:
        client = S3CompatibleMediaStorageClient()
        assert client._client_endpoint() == "cos.ap-guangzhou.myqcloud.com"
    finally:
        for key, value in original.items():
            setattr(settings, key, value)


def test_s3_compatible_storage_enables_virtual_host_flag_for_custom_provider() -> None:
    original = {
        "object_storage_bucket": settings.object_storage_bucket,
        "object_storage_endpoint": settings.object_storage_endpoint,
        "object_storage_access_key": settings.object_storage_access_key,
        "object_storage_secret_key": settings.object_storage_secret_key,
        "object_storage_secure": settings.object_storage_secure,
        "object_storage_region": settings.object_storage_region,
        "object_storage_path_style": settings.object_storage_path_style,
    }
    settings.object_storage_bucket = "tiles-cos-123"
    settings.object_storage_endpoint = "cos.ap-guangzhou.myqcloud.com"
    settings.object_storage_access_key = "access"
    settings.object_storage_secret_key = "secret"
    settings.object_storage_secure = True
    settings.object_storage_region = "ap-guangzhou"
    settings.object_storage_path_style = False
    try:
        client = S3CompatibleMediaStorageClient()
        sdk_client = client._get_client()
        url = sdk_client._base_url.build(
            "PUT",
            "ap-guangzhou",
            bucket_name="tiles-cos-123",
            object_name="images/default/a.webp",
        )
    finally:
        for key, value in original.items():
            setattr(settings, key, value)

    assert url.netloc == "tiles-cos-123.cos.ap-guangzhou.myqcloud.com"
    assert url.path == "/images/default/a.webp"


def test_s3_compatible_storage_keeps_endpoint_for_path_style() -> None:
    original = {
        "object_storage_bucket": settings.object_storage_bucket,
        "object_storage_endpoint": settings.object_storage_endpoint,
        "object_storage_path_style": settings.object_storage_path_style,
    }
    settings.object_storage_bucket = "tilesfst"
    settings.object_storage_endpoint = "minio:9000"
    settings.object_storage_path_style = True
    try:
        client = S3CompatibleMediaStorageClient()
        assert client._client_endpoint() == "minio:9000"
    finally:
        for key, value in original.items():
            setattr(settings, key, value)
