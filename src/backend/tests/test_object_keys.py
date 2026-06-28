"""Unit tests for object key generation and migration mapping."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from app.modules.media.key_migration import collect_migrations, map_legacy_object_key
from app.modules.media.object_keys import build_object_key


def test_build_object_key_uses_semantic_layout_without_date_segments() -> None:
    key = build_object_key("images", "user/avatars", "jpg")
    assert key.startswith("images/default/user/avatars/")
    assert key.endswith(".jpg")
    assert "/20" not in key.split("/")[-2:]  # no YYYY/MM before filename


def test_build_object_key_normalizes_prefix_and_extension() -> None:
    key = build_object_key("videos/", "tiles/pending", ".MP4")
    assert key.startswith("videos/default/tiles/pending/")
    assert key.endswith(".mp4")


def test_map_legacy_avatar_key() -> None:
    old = "original/default/avatars/2026/06/abc-123.webp"
    assert map_legacy_object_key(old) == "images/default/user/avatars/abc-123.webp"


def test_map_legacy_brand_logo_key() -> None:
    old = "original/default/brands/logos/2026/06/logo.webp"
    assert map_legacy_object_key(old) == "images/default/brands/logos/logo.webp"


def test_map_legacy_tile_image_key() -> None:
    old = "original/default/tiles/pending/images/2026/06/tile.jpg"
    assert map_legacy_object_key(old) == "images/default/tiles/pending/tile.jpg"


def test_map_legacy_tile_video_key() -> None:
    old = "videos/default/tiles/42/2026/06/clip.mp4"
    assert map_legacy_object_key(old) == "videos/default/tiles/42/clip.mp4"


def test_map_legacy_returns_none_for_current_key() -> None:
    current = "images/default/brands/logos/logo.webp"
    assert map_legacy_object_key(current) is None


def test_collect_migrations_from_sqlite(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    connection = sqlite3.connect(db_path)
    try:
        connection.execute(
            "CREATE TABLE brands (logo_object_key TEXT)"
        )
        connection.execute(
            "INSERT INTO brands (logo_object_key) VALUES (?)",
            ("original/default/brands/logos/2026/06/logo.webp",),
        )
        connection.commit()
    finally:
        connection.close()

    migrations = collect_migrations(db_path)
    assert len(migrations) == 1
    assert migrations[0].new_key == "images/default/brands/logos/logo.webp"


def test_collect_migrations_empty_db(tmp_path: Path) -> None:
    db_path = tmp_path / "empty.db"
    sqlite3.connect(db_path).close()
    assert collect_migrations(db_path) == []
