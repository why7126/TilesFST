"""Tests for scripts/clean-legacy-uploads.py"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from clean_legacy_uploads import (  # noqa: E402
    apply_cleanup,
    collect_referenced_object_keys,
    scan_legacy_uploads,
)


def _init_db(db_path: Path) -> None:
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(
            """
            CREATE TABLE brands (
              id INTEGER PRIMARY KEY,
              logo_object_key TEXT
            );
            CREATE TABLE users (
              id TEXT PRIMARY KEY,
              avatar_object_key TEXT
            );
            CREATE TABLE tile_images (
              id INTEGER PRIMARY KEY,
              object_key TEXT
            );
            CREATE TABLE tile_videos (
              id INTEGER PRIMARY KEY,
              object_key TEXT
            );
            """
        )
        connection.execute(
            "INSERT INTO brands (id, logo_object_key) VALUES (1, ?)",
            ("original/default/brands/logos/2026/06/kept.png",),
        )
        connection.commit()
    finally:
        connection.close()


def test_collect_referenced_object_keys(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    _init_db(db_path)
    keys = collect_referenced_object_keys(db_path)
    assert keys == {"original/default/brands/logos/2026/06/kept.png"}


def test_scan_legacy_uploads_finds_orphans(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    uploads_root = tmp_path / "uploads"
    _init_db(db_path)

    kept = uploads_root / "original/default/brands/logos/2026/06/kept.png"
    orphan = uploads_root / "original/default/brands/logos/2026/06/orphan.png"
    kept.parent.mkdir(parents=True)
    kept.write_bytes(b"kept")
    orphan.write_bytes(b"orphan")

    result = scan_legacy_uploads(db_path=db_path, uploads_root=uploads_root)
    assert orphan in result.orphan_files
    assert kept not in result.orphan_files


def test_apply_cleanup_deletes_orphans(tmp_path: Path) -> None:
    orphan = tmp_path / "orphan.png"
    orphan.write_bytes(b"x")
    deleted = apply_cleanup((orphan,), dry_run=False)
    assert deleted == 1
    assert not orphan.exists()


def test_scan_skips_gitkeep(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    uploads_root = tmp_path / "uploads"
    _init_db(db_path)
    gitkeep = uploads_root / "images" / ".gitkeep"
    gitkeep.parent.mkdir(parents=True)
    gitkeep.write_text("")

    result = scan_legacy_uploads(db_path=db_path, uploads_root=uploads_root)
    assert result.orphan_files == ()
