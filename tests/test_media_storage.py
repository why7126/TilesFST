from __future__ import annotations

from app.core.exceptions import AppError
from app.modules.media.storage import (
    MEDIA_NOT_FOUND,
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
