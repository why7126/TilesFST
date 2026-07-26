from __future__ import annotations

from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.exceptions import AppError
from app.main import app
from app.modules.media.storage import (
    MEDIA_NOT_FOUND,
    MediaObjectInfo,
    S3CompatibleMediaStorageClient,
    StoredMediaObject,
    TencentCOSMediaStorageClient,
    get_media_file_response,
    get_media_head_response,
    get_media_storage_client,
    set_media_storage_client,
)


class _MemoryMediaStorageClient:
    def __init__(self, content: bytes, content_type: str | None = None) -> None:
        self.objects = {"default": StoredMediaObject(content=content, content_type=content_type)}
        self.requested_keys: list[str] = []
        self.info_keys: list[str] = []
        self.range_requests: list[tuple[str, int, int]] = []

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

    def get_object_info(self, object_key: str) -> MediaObjectInfo:
        self.info_keys.append(object_key)
        if object_key in self.objects:
            stored_object = self.objects[object_key]
        elif "default" in self.objects:
            stored_object = self.objects["default"]
        else:
            raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体文件不存在")
        return MediaObjectInfo(
            content_type=stored_object.content_type,
            total_size=len(stored_object.content),
        )

    def get_object_range(self, object_key: str, offset: int, length: int) -> StoredMediaObject:
        self.range_requests.append((object_key, offset, length))
        stored_object = self.get_object(object_key)
        return StoredMediaObject(
            content=stored_object.content[offset : offset + length],
            content_type=stored_object.content_type,
            total_size=len(stored_object.content),
        )


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


def test_media_file_response_returns_partial_content_for_video_range() -> None:
    video_bytes = b"0123456789abcdef"
    storage = _MemoryMediaStorageClient.from_objects(
        {
            "videos/default/tiles/1/demo.mp4": StoredMediaObject(
                video_bytes,
                "video/mp4",
            )
        }
    )
    set_media_storage_client(storage)
    try:
        response = get_media_file_response("videos/default/tiles/1/demo.mp4", "bytes=2-5")
    finally:
        set_media_storage_client(None)

    assert response.status_code == 206
    assert response.body == b"2345"
    assert response.media_type == "video/mp4"
    assert response.headers["accept-ranges"] == "bytes"
    assert response.headers["content-range"] == "bytes 2-5/16"
    assert response.headers["content-length"] == "4"
    assert storage.info_keys == ["videos/default/tiles/1/demo.mp4"]
    assert storage.range_requests == [("videos/default/tiles/1/demo.mp4", 2, 4)]


def test_media_head_response_returns_video_metadata_without_body() -> None:
    video_bytes = b"0123456789abcdef"
    storage = _MemoryMediaStorageClient.from_objects(
        {
            "videos/default/tiles/1/demo.mp4": StoredMediaObject(
                video_bytes,
                "video/mp4",
            )
        }
    )
    set_media_storage_client(storage)
    try:
        response = get_media_head_response("videos/default/tiles/1/demo.mp4")
    finally:
        set_media_storage_client(None)

    assert response.status_code == 200
    assert response.body == b""
    assert response.media_type == "video/mp4"
    assert response.headers["content-length"] == "16"
    assert response.headers["accept-ranges"] == "bytes"
    assert storage.info_keys == ["videos/default/tiles/1/demo.mp4"]
    assert storage.requested_keys == []


def test_media_head_route_allows_video_metadata_probe() -> None:
    storage = _MemoryMediaStorageClient.from_objects(
        {
            "videos/default/tiles/1/demo.mp4": StoredMediaObject(
                b"0123456789abcdef",
                "video/mp4",
            )
        }
    )
    set_media_storage_client(storage)
    try:
        response = TestClient(app).head("/media/videos/default/tiles/1/demo.mp4")
    finally:
        set_media_storage_client(None)

    assert response.status_code == 200
    assert response.content == b""
    assert response.headers["content-type"].startswith("video/mp4")
    assert response.headers["content-length"] == "16"
    assert response.headers["accept-ranges"] == "bytes"


def test_media_file_response_returns_416_for_invalid_video_range() -> None:
    video_bytes = b"0123456789abcdef"
    storage = _MemoryMediaStorageClient.from_objects(
        {
            "videos/default/tiles/1/demo.mp4": StoredMediaObject(
                video_bytes,
                "video/mp4",
            )
        }
    )
    set_media_storage_client(storage)
    try:
        response = get_media_file_response("videos/default/tiles/1/demo.mp4", "bytes=99-120")
    finally:
        set_media_storage_client(None)

    assert response.status_code == 416
    assert response.body == b""
    assert response.headers["accept-ranges"] == "bytes"
    assert response.headers["content-range"] == "bytes */16"
    assert storage.range_requests == []


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


def test_media_storage_client_uses_tencent_cos_sdk_for_tencent_provider() -> None:
    original = {
        "object_storage_provider": settings.object_storage_provider,
    }
    settings.object_storage_provider = "tencent-cos"
    set_media_storage_client(None)
    try:
        client = get_media_storage_client()
    finally:
        settings.object_storage_provider = original["object_storage_provider"]
        set_media_storage_client(None)

    assert isinstance(client, TencentCOSMediaStorageClient)


def test_tencent_cos_storage_put_object_uses_official_sdk() -> None:
    original = {
        "object_storage_bucket": settings.object_storage_bucket,
        "object_storage_provider": settings.object_storage_provider,
        "object_storage_endpoint": settings.object_storage_endpoint,
        "object_storage_access_key": settings.object_storage_access_key,
        "object_storage_secret_key": settings.object_storage_secret_key,
        "object_storage_secure": settings.object_storage_secure,
        "object_storage_region": settings.object_storage_region,
    }
    settings.object_storage_bucket = "tiles-cos-123"
    settings.object_storage_provider = "tencent-cos"
    settings.object_storage_endpoint = "cos.ap-guangzhou.myqcloud.com"
    settings.object_storage_access_key = "access"
    settings.object_storage_secret_key = "secret"
    settings.object_storage_secure = True
    settings.object_storage_region = "ap-guangzhou"

    class _FakeTencentCOSClient:
        def __init__(self) -> None:
            self.puts = []

        def put_object(self, **kwargs):
            self.puts.append(
                {
                    **kwargs,
                    "Body": kwargs["Body"].read(),
                }
            )

    backend = _FakeTencentCOSClient()
    client = TencentCOSMediaStorageClient()
    client._client = backend
    try:
        client.put_object("videos/default/tiles/pending/demo.mp4", b"video", "video/mp4")
    finally:
        for key, value in original.items():
            setattr(settings, key, value)

    assert backend.puts == [
        {
            "Bucket": "tiles-cos-123",
            "Key": "videos/default/tiles/pending/demo.mp4",
            "Body": b"video",
            "ContentType": "video/mp4",
            "EnableMD5": False,
        }
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
