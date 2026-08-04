from __future__ import annotations

import importlib.util
from io import BytesIO
from pathlib import Path
import sqlite3

from PIL import Image

from app.modules.media.storage import MediaObjectInfo, StoredMediaObject


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "backfill-brand-certificate-thumbnails.py"
spec = importlib.util.spec_from_file_location("backfill_brand_certificate_thumbnails", SCRIPT_PATH)
backfill_script = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(backfill_script)


def _image_bytes(fmt: str = "WEBP", size: tuple[int, int] = (960, 640)) -> bytes:
    image = Image.new("RGB", size, (90, 120, 180))
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
        brand_logo = _image_bytes()
        cert_image = _image_bytes()
        self.objects = {
            "images/default/brands/logos/logo.webp": StoredMediaObject(brand_logo, "image/webp"),
            "images/default/brand-certificates/cover.webp": StoredMediaObject(cert_image, "image/webp"),
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
            CREATE TABLE brands (
                id INTEGER PRIMARY KEY,
                logo_object_key TEXT
            );
            CREATE TABLE brand_certificates (
                id INTEGER PRIMARY KEY,
                deleted_at TEXT,
                file_key TEXT,
                file_mime_type TEXT
            );
            CREATE TABLE brand_certificate_images (
                id INTEGER PRIMARY KEY,
                file_key TEXT,
                file_mime_type TEXT
            );
            INSERT INTO brands VALUES (1, 'images/default/brands/logos/logo.webp');
            INSERT INTO brand_certificates VALUES (
                1,
                NULL,
                'images/default/brand-certificates/cover.webp',
                'image/webp'
            );
            INSERT INTO brand_certificates VALUES (
                2,
                NULL,
                'files/default/brand-certificates/report.pdf',
                'application/pdf'
            );
            INSERT INTO brand_certificate_images VALUES (
                1,
                'images/default/brand-certificates/cover.webp',
                'image/webp'
            );
            """
        )
        connection.commit()
    finally:
        connection.close()


def test_brand_certificate_thumbnail_backfill_dry_run_apply_and_repeat(
    tmp_path: Path,
    monkeypatch,
) -> None:
    db_path = tmp_path / "catalog.db"
    _prepare_db(db_path)
    storage = _Storage()
    monkeypatch.setattr(backfill_script, "get_media_storage_client", lambda: storage)
    monkeypatch.setattr(
        backfill_script,
        "get_session_factory",
        lambda: lambda: _Session(sqlite3.connect(db_path)),
    )

    dry_run = backfill_script.audit(limit=None, execute=False)
    assert dry_run["summary"]["total"] == 2
    assert dry_run["summary"]["retry_candidates"] == 2
    assert {item["status"] for item in dry_run["items"]} == {"dry_run"}
    assert storage.puts == []

    executed = backfill_script.audit(limit=None, execute=True)
    assert executed["summary"]["success"] == 2
    assert [put[0] for put in storage.puts] == [
        "images/default/brands/logos/logo.thumb.webp",
        "images/default/brand-certificates/cover.thumb.webp",
    ]

    repeated = backfill_script.audit(limit=None, execute=True)
    assert repeated["summary"]["success"] == 0
    assert repeated["summary"]["skipped"] == 2
