from __future__ import annotations

import importlib.util
from io import BytesIO
from pathlib import Path
import sqlite3

from PIL import Image

from app.modules.media.storage import MediaObjectInfo, StoredMediaObject


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "audit-miniapp-card-images.py"
spec = importlib.util.spec_from_file_location("audit_miniapp_card_images", SCRIPT_PATH)
audit_script = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(audit_script)


def _image_bytes(fmt: str = "JPEG", size: tuple[int, int] = (960, 640)) -> bytes:
    image = Image.new("RGB", size, (120, 30, 200))
    output = BytesIO()
    image.save(output, format=fmt, quality=95)
    return output.getvalue()


class _Session:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def execute(self, statement, params=None):
        cursor = self.connection.execute(str(statement), params or {})
        return _Result(cursor)

    def close(self) -> None:
        self.connection.close()


class _Result:
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        self.cursor = cursor

    def mappings(self) -> "_Result":
        return self

    def all(self) -> list[dict[str, object]]:
        columns = [column[0] for column in self.cursor.description or []]
        return [dict(zip(columns, row, strict=True)) for row in self.cursor.fetchall()]


class _Storage:
    def __init__(self) -> None:
        image = _image_bytes()
        self.objects = {
            "images/default/tiles/pending/abc.jpg": StoredMediaObject(
                image,
                "image/jpeg",
            )
        }
        self.puts: list[tuple[str, bytes, str | None]] = []

    def get_object_info(self, object_key: str) -> MediaObjectInfo:
        if object_key not in self.objects:
            from app.core.exceptions import AppError
            from app.modules.media.storage import MEDIA_NOT_FOUND

            raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体文件不存在")
        stored = self.objects[object_key]
        return MediaObjectInfo(content_type=stored.content_type, total_size=len(stored.content))

    def get_object(self, object_key: str) -> StoredMediaObject:
        return self.objects[object_key]

    def put_object(self, object_key: str, content: bytes, content_type: str | None) -> None:
        self.puts.append((object_key, content, content_type))
        self.objects[object_key] = StoredMediaObject(content, content_type)


def _prepare_db(path: Path) -> None:
    connection = sqlite3.connect(path)
    try:
        connection.executescript(
            """
            CREATE TABLE tiles (
                id INTEGER PRIMARY KEY,
                sku_code TEXT,
                status TEXT,
                brand_id INTEGER,
                category_id INTEGER,
                spec_id INTEGER
            );
            CREATE TABLE tile_images (tile_id INTEGER, object_key TEXT, is_main INTEGER);
            CREATE TABLE brands (id INTEGER PRIMARY KEY, status TEXT);
            CREATE TABLE tile_categories (id INTEGER PRIMARY KEY, status TEXT);
            CREATE TABLE tile_specs (id INTEGER PRIMARY KEY, status TEXT);
            INSERT INTO brands VALUES (1, 'ENABLED');
            INSERT INTO tile_categories VALUES (1, 'ENABLED');
            INSERT INTO tiles VALUES (1, 'FST-001', 'PUBLISHED', 1, 1, NULL);
            INSERT INTO tile_images VALUES (
                1,
                'images/default/tiles/pending/abc.jpg',
                1
            );
            """
        )
        connection.commit()
    finally:
        connection.close()


def test_audit_reports_pending_same_directory_thumbnail_and_backfills(
    tmp_path: Path,
    monkeypatch,
) -> None:
    db_path = tmp_path / "catalog.db"
    _prepare_db(db_path)
    storage = _Storage()
    monkeypatch.setattr(audit_script, "get_media_storage_client", lambda: storage)
    monkeypatch.setattr(
        audit_script,
        "get_session_factory",
        lambda: lambda: _Session(sqlite3.connect(db_path)),
    )

    dry_run = audit_script.audit(limit=None, backfill=True, execute=False)
    assert dry_run["pending_main_image"] == 1
    assert dry_run["missing_thumbnail_object"] == 1
    assert dry_run["needs_thumbnail_regeneration"] == 1
    assert dry_run["items"][0]["thumbnail_key"] == "images/default/tiles/pending/abc.thumb.jpg"
    assert dry_run["items"][0]["backfill_status"] == "dry_run"
    assert storage.puts == []

    executed = audit_script.audit(limit=None, backfill=True, execute=True)
    assert executed["backfill"]["success"] == 1
    assert storage.puts[0][0] == "images/default/tiles/pending/abc.thumb.jpg"
    assert storage.puts[0][1] != storage.objects["images/default/tiles/pending/abc.jpg"].content
    assert storage.puts[0][2] == "image/jpeg"

    repeated = audit_script.audit(limit=None, backfill=True, execute=True)
    assert repeated["backfill"]["success"] == 0
    assert repeated["skipped_valid_thumbnail"] == 1


def test_audit_regenerates_same_bytes_thumbnail(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "catalog.db"
    _prepare_db(db_path)
    storage = _Storage()
    original = storage.objects["images/default/tiles/pending/abc.jpg"]
    storage.objects["images/default/tiles/pending/abc.thumb.jpg"] = original
    monkeypatch.setattr(audit_script, "get_media_storage_client", lambda: storage)
    monkeypatch.setattr(
        audit_script,
        "get_session_factory",
        lambda: lambda: _Session(sqlite3.connect(db_path)),
    )

    dry_run = audit_script.audit(limit=None, backfill=True, execute=False)
    assert dry_run["missing_thumbnail_object"] == 0
    assert dry_run["same_size_thumbnail_object"] == 1
    assert dry_run["same_bytes_thumbnail_object"] == 1
    assert dry_run["needs_thumbnail_regeneration"] == 1
    assert dry_run["items"][0]["backfill_status"] == "dry_run"

    executed = audit_script.audit(limit=None, backfill=True, execute=True)
    assert executed["backfill"]["success"] == 1
    regenerated = storage.objects["images/default/tiles/pending/abc.thumb.jpg"]
    assert regenerated.content != original.content
    assert len(regenerated.content) < len(original.content)
