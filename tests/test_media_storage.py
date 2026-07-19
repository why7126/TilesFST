from __future__ import annotations

from app.modules.media.storage import StoredMediaObject, get_media_file_response, set_media_storage_client


class _MemoryMediaStorageClient:
    def __init__(self, content: bytes, content_type: str | None = None) -> None:
        self._content = content
        self._content_type = content_type

    def put_object(self, object_key: str, content: bytes, content_type: str | None) -> None:
        self._content = content
        self._content_type = content_type

    def get_object(self, object_key: str) -> StoredMediaObject:
        return StoredMediaObject(content=self._content, content_type=self._content_type)


def test_media_file_response_detects_webp_content_even_when_key_suffix_is_png() -> None:
    webp_bytes = b"RIFF\x10\x00\x00\x00WEBPVP8X" + b"\x00" * 16
    set_media_storage_client(_MemoryMediaStorageClient(webp_bytes))
    try:
        response = get_media_file_response("images/default/tiles/1/wrong-suffix.png")
    finally:
        set_media_storage_client(None)

    assert response.media_type == "image/webp"
