from __future__ import annotations

from io import BytesIO
import asyncio

import pytest
from fastapi.testclient import TestClient
from fastapi import UploadFile
from PIL import Image

from app.core.config import settings
from app.core.exceptions import AppError
from app.main import app
from app.modules.media.storage import (
    MEDIA_NOT_FOUND,
    MediaObjectInfo,
    S3CompatibleMediaStorageClient,
    StoredMediaObject,
    TencentCOSMediaStorageClient,
    generate_image_thumbnail,
    get_media_file_response,
    get_media_head_response,
    get_media_storage_client,
    media_variant_urls,
    same_directory_display_object_key,
    same_directory_thumbnail_object_key,
    save_upload_file,
    set_media_storage_client,
)


def _image_bytes(
    fmt: str,
    size: tuple[int, int],
    *,
    mode: str = "RGB",
    color: tuple[int, ...] = (90, 120, 180),
) -> bytes:
    image = Image.new(mode, size, color)
    output = BytesIO()
    save_kwargs: dict[str, object] = {"format": fmt}
    if fmt == "JPEG":
        save_kwargs["quality"] = 95
    if fmt == "WEBP":
        save_kwargs["quality"] = 95
    image.save(output, **save_kwargs)
    return output.getvalue()


def test_generate_image_thumbnail_resizes_large_image_and_changes_bytes() -> None:
    original = _image_bytes("JPEG", (1200, 800), color=(120, 30, 200))

    thumbnail = generate_image_thumbnail(original, "image/jpeg", max_width=480, max_height=480)

    assert thumbnail.width <= 480
    assert thumbnail.height <= 480
    assert thumbnail.width < thumbnail.original_width
    assert thumbnail.height < thumbnail.original_height
    assert thumbnail.content != original
    assert thumbnail.size < len(original)
    assert thumbnail.content_type == "image/webp"
    with Image.open(BytesIO(thumbnail.content)) as image:
        assert image.format == "WEBP"


@pytest.mark.parametrize(
    ("fmt", "content_type", "size"),
    [
        ("JPEG", "image/jpeg", (900, 300)),
        ("PNG", "image/png", (300, 900)),
        ("WEBP", "image/webp", (900, 900)),
    ],
)
def test_generate_image_thumbnail_supports_common_formats(
    fmt: str,
    content_type: str,
    size: tuple[int, int],
) -> None:
    original = _image_bytes(fmt, size)

    thumbnail = generate_image_thumbnail(original, content_type, max_width=360, max_height=360)

    assert thumbnail.width <= 360
    assert thumbnail.height <= 360
    assert thumbnail.content != original
    assert thumbnail.content_type == "image/webp"
    with Image.open(BytesIO(thumbnail.content)) as image:
        assert image.format == "WEBP"


def test_generate_image_thumbnail_does_not_upscale_small_images() -> None:
    original = _image_bytes("PNG", (120, 80))

    thumbnail = generate_image_thumbnail(original, "image/png", max_width=480, max_height=480)

    assert (thumbnail.width, thumbnail.height) == (120, 80)
    assert thumbnail.resized is False


def test_generate_image_thumbnail_preserves_transparent_png_alpha() -> None:
    original = _image_bytes("PNG", (640, 320), mode="RGBA", color=(90, 120, 180, 0))

    thumbnail = generate_image_thumbnail(original, "image/png", max_width=320, max_height=320)

    with Image.open(BytesIO(thumbnail.content)) as image:
        assert image.format == "WEBP"
        assert image.mode in {"LA", "RGBA", "P"}
        assert image.getpixel((0, 0))[-1] == 0


def test_generate_image_thumbnail_rejects_invalid_image_bytes() -> None:
    with pytest.raises(ValueError):
        generate_image_thumbnail(b"not-an-image", "image/jpeg")


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

    def build_direct_read_url(self, object_key: str, expires_seconds: int) -> str:
        return f"https://storage.example.test/{object_key}?expires={expires_seconds}"


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


def test_media_file_response_falls_back_from_thumbnail_to_original_key() -> None:
    png_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16
    storage = _MemoryMediaStorageClient.from_objects(
        {
            "original/default/tiles/1/images/2026/06/1.png": StoredMediaObject(
                png_bytes,
                "image/png",
            )
        }
    )
    set_media_storage_client(storage)
    try:
        response = get_media_file_response(
            "thumbnails/default/tiles/1/images/2026/06/1.png"
        )
    finally:
        set_media_storage_client(None)

    assert response.media_type == "image/png"
    assert response.headers["cache-control"].startswith("public, max-age=604800")
    assert response.headers["etag"].startswith('W/"')
    assert response.headers["x-media-fallback"] == "1"
    assert response.headers["x-media-resolved-key-hash"]
    assert storage.requested_keys == [
        "thumbnails/default/tiles/1/images/2026/06/1.png",
        "default/tiles/1/images/2026/06/1.png",
        "original/default/tiles/1/images/2026/06/1.png",
    ]


def test_same_directory_thumbnail_key_uses_filename_suffix() -> None:
    assert (
        same_directory_thumbnail_object_key("images/default/tiles/pending/abc.jpg")
        == "images/default/tiles/pending/abc.thumb.webp"
    )
    assert (
        same_directory_thumbnail_object_key("images/default/tiles/42/abc.webp")
        == "images/default/tiles/42/abc.thumb.webp"
    )


def test_media_variant_urls_use_stable_same_directory_keys() -> None:
    urls = media_variant_urls("images/default/tiles/42/abc.webp")

    assert urls == {
        "original_url": "/media/images/default/tiles/42/abc.webp",
        "thumbnail_url": "/media/images/default/tiles/42/abc.thumb.webp",
        "display_url": "/media/images/default/tiles/42/abc.display.webp",
    }


def test_media_variant_urls_can_use_controlled_direct_object_storage_urls(monkeypatch) -> None:
    set_media_storage_client(_MemoryMediaStorageClient.from_objects({}))
    monkeypatch.setattr(settings, "object_storage_direct_read_expires_seconds", 180)
    try:
        urls = media_variant_urls("images/default/tiles/42/abc.webp", direct=True)
    finally:
        set_media_storage_client(None)

    assert urls == {
        "original_url": "https://storage.example.test/images/default/tiles/42/abc.webp?expires=180",
        "thumbnail_url": "https://storage.example.test/images/default/tiles/42/abc.thumb.webp?expires=180",
        "display_url": "https://storage.example.test/images/default/tiles/42/abc.display.webp?expires=180",
    }
    assert (
        same_directory_display_object_key("images/default/tiles/42/abc.webp")
        == "images/default/tiles/42/abc.display.webp"
    )


def test_media_file_response_falls_back_from_same_directory_thumbnail_to_original() -> None:
    jpg_bytes = b"\xff\xd8\xff" + b"\x00" * 16
    storage = _MemoryMediaStorageClient.from_objects(
        {
            "images/default/tiles/pending/abc.jpg": StoredMediaObject(
                jpg_bytes,
                "image/jpeg",
            )
        }
    )
    set_media_storage_client(storage)
    try:
        response = get_media_file_response("images/default/tiles/pending/abc.thumb.jpg")
    finally:
        set_media_storage_client(None)

    assert response.media_type == "image/jpeg"
    assert response.headers["x-media-fallback"] == "1"
    assert response.headers["x-media-resolved-key-hash"]
    assert storage.requested_keys == [
        "images/default/tiles/pending/abc.thumb.jpg",
        "images/default/tiles/pending/abc.jpg",
    ]


def test_media_file_response_falls_back_from_webp_thumbnail_to_jpg_original() -> None:
    jpg_bytes = b"\xff\xd8\xff" + b"\x00" * 16
    storage = _MemoryMediaStorageClient.from_objects(
        {
            "images/default/tiles/pending/abc.jpg": StoredMediaObject(
                jpg_bytes,
                "image/jpeg",
            )
        }
    )
    set_media_storage_client(storage)
    try:
        response = get_media_file_response("images/default/tiles/pending/abc.thumb.webp")
    finally:
        set_media_storage_client(None)

    assert response.media_type == "image/jpeg"
    assert response.headers["x-media-fallback"] == "1"
    assert storage.requested_keys == [
        "images/default/tiles/pending/abc.thumb.webp",
        "images/default/tiles/pending/abc.jpg",
    ]


def test_media_file_response_falls_back_from_same_directory_display_to_original() -> None:
    jpg_bytes = b"\xff\xd8\xff" + b"\x00" * 16
    storage = _MemoryMediaStorageClient.from_objects(
        {
            "images/default/tiles/pending/abc.jpg": StoredMediaObject(
                jpg_bytes,
                "image/jpeg",
            )
        }
    )
    set_media_storage_client(storage)
    try:
        response = get_media_file_response("images/default/tiles/pending/abc.display.jpg")
    finally:
        set_media_storage_client(None)

    assert response.media_type == "image/jpeg"
    assert response.headers["x-media-fallback"] == "1"
    assert storage.requested_keys == [
        "images/default/tiles/pending/abc.display.jpg",
        "images/default/tiles/pending/abc.jpg",
    ]


def test_save_upload_file_generates_thumbnail_and_display_variants() -> None:
    original = _image_bytes("JPEG", (2200, 1600), color=(120, 30, 200))
    storage = _MemoryMediaStorageClient.from_objects({})
    file = UploadFile(filename="demo.jpg", file=BytesIO(original))
    file.headers = {"content-type": "image/jpeg"}
    set_media_storage_client(storage)
    try:
        size = asyncio.run(
            save_upload_file(
                file,
                "images/default/tiles/pending/demo.jpg",
                5,
                thumbnail_key="images/default/tiles/pending/demo.thumb.webp",
                display_key="images/default/tiles/pending/demo.display.webp",
            )
        )
    finally:
        set_media_storage_client(None)

    assert size == len(original)
    assert set(storage.objects) == {
        "images/default/tiles/pending/demo.jpg",
        "images/default/tiles/pending/demo.thumb.webp",
        "images/default/tiles/pending/demo.display.webp",
    }
    assert storage.objects["images/default/tiles/pending/demo.thumb.webp"].content_type == "image/webp"
    assert storage.objects["images/default/tiles/pending/demo.display.webp"].content_type == "image/webp"
    assert len(storage.objects["images/default/tiles/pending/demo.thumb.webp"].content) < len(original)
    assert len(storage.objects["images/default/tiles/pending/demo.display.webp"].content) < len(original)


def test_media_head_response_returns_image_cache_headers() -> None:
    png_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16
    storage = _MemoryMediaStorageClient.from_objects(
        {"images/default/tiles/1/1.png": StoredMediaObject(png_bytes, "image/png")}
    )
    set_media_storage_client(storage)
    try:
        response = get_media_head_response("images/default/tiles/1/1.png")
    finally:
        set_media_storage_client(None)

    assert response.headers["cache-control"].startswith("public, max-age=604800")
    assert response.headers["etag"].startswith('W/"')
    assert response.headers["x-media-fallback"] == "0"
    assert response.headers["x-media-resolved-key-hash"]


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


def test_tencent_cos_storage_head_no_such_resource_is_media_not_found() -> None:
    class _FakeTencentCOSMissingResource(Exception):
        def get_error_code(self) -> str:
            return "NoSuchResource"

    class _FakeTencentCOSClient:
        def head_object(self, **kwargs):
            raise _FakeTencentCOSMissingResource("The Resource You Head Not Exist")

    client = TencentCOSMediaStorageClient()
    client._client = _FakeTencentCOSClient()

    with pytest.raises(AppError) as exc_info:
        client.get_object_info("images/default/brands/logos/demo.thumb.webp")

    assert exc_info.value.status_code == 404
    assert exc_info.value.code == MEDIA_NOT_FOUND


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
            method="PUT",
            region="ap-guangzhou",
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
