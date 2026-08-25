from __future__ import annotations

import importlib.util
from pathlib import Path
import sqlite3

from app.modules.media.storage import MediaObjectInfo, StoredMediaObject, set_media_storage_client


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "migrate-pending-tile-images.py"
spec = importlib.util.spec_from_file_location("migrate_pending_tile_images", SCRIPT_PATH)
migrate_script = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(migrate_script)


class _Session:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def execute(self, statement, params=None):
        cursor = self.connection.execute(str(statement), params or {})
        return _Result(cursor)

    def commit(self) -> None:
        self.connection.commit()

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
        self.objects = {
            "images/default/tiles/pending/abc.jpg": StoredMediaObject(
                b"image",
                "image/jpeg",
            ),
            "images/default/tiles/pending/abc.thumb.webp": StoredMediaObject(
                b"thumb",
                "image/webp",
            ),
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
        if object_key not in self.objects:
            from app.core.exceptions import AppError
            from app.modules.media.storage import MEDIA_NOT_FOUND

            raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体文件不存在")
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
            CREATE TABLE tile_images (
                id INTEGER PRIMARY KEY,
                tile_id INTEGER,
                object_key TEXT,
                url TEXT,
                is_main INTEGER
            );
            CREATE TABLE brands (id INTEGER PRIMARY KEY, status TEXT);
            CREATE TABLE tile_categories (id INTEGER PRIMARY KEY, status TEXT);
            CREATE TABLE tile_specs (id INTEGER PRIMARY KEY, status TEXT);
            INSERT INTO brands VALUES (1, 'ENABLED');
            INSERT INTO tile_categories VALUES (1, 'ENABLED');
            INSERT INTO tiles VALUES (42, 'FST-042', 'PUBLISHED', 1, 1, NULL);
            INSERT INTO tile_images VALUES (
                7,
                42,
                'images/default/tiles/pending/abc.jpg',
                '/media/images/default/tiles/pending/abc.jpg',
                1
            );
            """
        )
        connection.commit()
    finally:
        connection.close()


def _db_key(path: Path) -> str:
    connection = sqlite3.connect(path)
    try:
        return str(
            connection.execute("SELECT object_key FROM tile_images WHERE id = 7").fetchone()[0]
        )
    finally:
        connection.close()


def test_migrate_pending_tile_images_dry_run_and_apply_are_idempotent(
    tmp_path: Path,
    monkeypatch,
) -> None:
    db_path = tmp_path / "catalog.db"
    _prepare_db(db_path)
    storage = _Storage()
    set_media_storage_client(storage)
    monkeypatch.setattr(migrate_script, "get_media_storage_client", lambda: storage)
    monkeypatch.setattr(migrate_script.maintenance, "_effective_thumbnail_max_size_kb", lambda: 0)
    monkeypatch.setattr(migrate_script.maintenance, "_effective_display_max_size_kb", lambda: 0)
    monkeypatch.setattr(
        migrate_script,
        "get_session_factory",
        lambda: lambda: _Session(sqlite3.connect(db_path)),
    )

    try:
        dry_run = migrate_script.migrate(apply=False)
        assert dry_run["dry_run"] is True
        assert dry_run["total"] == 1
        assert dry_run["success"] == 0
        assert dry_run["items"][0]["target_key"] == "images/default/tiles/42/abc.jpg"
        assert storage.puts == []
        assert _db_key(db_path) == "images/default/tiles/pending/abc.jpg"

        applied = migrate_script.migrate(apply=True)
        assert applied["success"] == 1
        assert storage.puts == [
            ("images/default/tiles/42/abc.jpg", b"image", "image/jpeg"),
            ("images/default/tiles/42/abc.thumb.webp", b"thumb", "image/webp"),
        ]
        assert _db_key(db_path) == "images/default/tiles/42/abc.jpg"

        repeat = migrate_script.migrate(apply=True)
        assert repeat["total"] == 0
        assert repeat["success"] == 0
    finally:
        set_media_storage_client(None)
