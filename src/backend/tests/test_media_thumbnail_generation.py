"""Thumbnail generation target-size behavior."""

from __future__ import annotations

from io import BytesIO

import pytest

from app.modules.media.storage import generate_image_thumbnail, same_directory_thumbnail_object_key

pytest.importorskip("PIL")


def _jpeg_bytes(width: int = 1200, height: int = 900) -> bytes:
    from PIL import Image

    image = Image.new("RGB", (width, height))
    pixels = image.load()
    for x in range(width):
        for y in range(height):
            pixels[x, y] = ((x * 7 + y) % 256, (x + y * 11) % 256, (x * y) % 256)
    output = BytesIO()
    image.save(output, format="JPEG", quality=95)
    return output.getvalue()


def test_thumbnail_default_mode_preserves_current_key_and_generates_smaller_image() -> None:
    content = _jpeg_bytes()
    thumbnail = generate_image_thumbnail(content, "image/jpeg")

    assert same_directory_thumbnail_object_key("images/default/tiles/1/main.webp") == (
        "images/default/tiles/1/main.thumb.webp"
    )
    assert thumbnail.size < len(content)
    assert thumbnail.width <= 480
    assert thumbnail.height <= 480


def test_thumbnail_target_size_compresses_jpeg_when_possible() -> None:
    content = _jpeg_bytes()
    default_thumbnail = generate_image_thumbnail(content, "image/jpeg")
    targeted_thumbnail = generate_image_thumbnail(
        content,
        "image/jpeg",
        target_max_size_kb=20,
    )

    assert targeted_thumbnail.size <= default_thumbnail.size
    assert targeted_thumbnail.size <= 20 * 1024


def test_thumbnail_tiny_target_returns_best_effort_without_failing() -> None:
    content = _jpeg_bytes()
    thumbnail = generate_image_thumbnail(content, "image/jpeg", target_max_size_kb=1)

    assert thumbnail.size > 0
    assert thumbnail.content_type == "image/jpeg"
