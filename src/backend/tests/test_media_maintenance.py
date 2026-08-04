import argparse
import sqlite3

import pytest

from app.modules.media.storage import MediaObjectInfo, StoredMediaObject
from app.modules.media import maintenance


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
            "files/default/brand-certificates/cert.jpg": StoredMediaObject(
                b"cert-image",
                "image/jpeg",
            ),
            "files/default/brand-certificates/extra.webp": StoredMediaObject(
                b"cert-extra",
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


def test_apply_requires_confirm_backup():
    args = maintenance.build_parser().parse_args(
        ["backfill-brand-certificate-thumbnails", "--apply"]
    )

    with pytest.raises(ValueError, match="--apply requires --confirm-backup"):
        maintenance.run(args)


def test_read_only_audit_rejects_apply_even_with_backup_confirmation():
    args = maintenance.build_parser().parse_args(
        ["object-key-audit", "--apply", "--confirm-backup"]
    )

    with pytest.raises(ValueError, match="does not support apply"):
        maintenance.run(args)


def test_bug_0116_aggregate_apply_requires_confirm_backup():
    args = maintenance.build_parser().parse_args(["bug-0116-media-drift", "--apply"])

    with pytest.raises(ValueError, match="--apply requires --confirm-backup"):
        maintenance.run(args)


def test_sensitive_output_guard_blocks_secret_keys():
    with pytest.raises(ValueError, match="sensitive output key blocked"):
        maintenance._assert_no_sensitive_output(
            {"summary": {"OBJECT_STORAGE_SECRET_KEY": "example"}}
        )


def test_sensitive_output_guard_blocks_embedded_credentials():
    with pytest.raises(ValueError, match="sensitive output value blocked"):
        maintenance._assert_no_sensitive_output(
            {"summary": {"database": "mysql://user:password@example/db"}}
        )


def test_safe_object_ref_hides_raw_object_key():
    ref = maintenance._safe_object_ref("images/default/tiles/pending/demo.jpg")

    assert ref == {
        "object_key_hash": maintenance._fingerprint(
            "images/default/tiles/pending/demo.jpg"
        ),
        "object_key_prefix": "images/default/tiles/pending",
    }
    assert "demo.jpg" not in ref.values()


def test_pending_tile_formalization_dry_run_uses_acceptance_summary(monkeypatch):
    args = argparse.Namespace(apply=False, limit=1, confirm_backup=False)
    monkeypatch.setattr(
        maintenance,
        "_pending_tile_rows",
        lambda limit: [
            {
                "tile_id": 42,
                "sku_code": "SKU-42",
                "image_id": 7,
                "object_key": "images/default/tiles/pending/demo.jpg",
            }
        ],
    )
    monkeypatch.setattr(maintenance, "_object_exists", lambda object_key: True)

    result = maintenance.run_pending_tile_formalization(args)

    assert result["mode"] == "dry_run"
    assert result["summary"]["total"] == 1
    assert result["items"][0]["source"]["object_key_prefix"] == (
        "images/default/tiles/pending"
    )
    assert result["acceptance_summary"]["render"]["status"] == "blocked"


def test_thumbnail_backfill_counts_same_size_and_same_bytes(monkeypatch):
    args = argparse.Namespace(apply=False, limit=None, confirm_backup=False)
    storage = _Storage()
    storage.objects = {
        "images/default/brands/logos/logo.jpg": StoredMediaObject(b"same", "image/jpeg"),
        "images/default/brands/logos/logo.thumb.jpg": StoredMediaObject(
            b"same",
            "image/jpeg",
        ),
    }
    monkeypatch.setattr(maintenance, "get_media_storage_client", lambda: storage)
    monkeypatch.setattr(
        maintenance,
        "_thumbnail_source_rows",
        lambda limit: [
            {
                "source_type": "brand_logo",
                "source_id": 1,
                "object_key": "images/default/brands/logos/logo.jpg",
                "mime_type": "image/jpeg",
            }
        ],
    )

    result = maintenance.run_thumbnail_backfill(args)

    assert result["summary"]["retry_candidates"] == 1
    assert result["summary"]["same_size"] == 1
    assert result["summary"]["same_bytes"] == 1
    assert result["items"][0]["reason"] == "thumbnail_copied_original"


def _prepare_certificate_db(path) -> None:
    connection = sqlite3.connect(path)
    try:
        connection.executescript(
            """
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
            INSERT INTO brand_certificates VALUES (
                1,
                NULL,
                'files/default/brand-certificates/cert.jpg',
                'image/jpeg'
            );
            INSERT INTO brand_certificates VALUES (
                2,
                NULL,
                'files/default/brand-certificates/report.pdf',
                'application/pdf'
            );
            INSERT INTO brand_certificate_images VALUES (
                9,
                'files/default/brand-certificates/extra.webp',
                'image/webp'
            );
            """
        )
        connection.commit()
    finally:
        connection.close()


def test_certificate_image_key_migration_dry_run_apply_and_repeat(tmp_path, monkeypatch):
    db_path = tmp_path / "catalog.db"
    _prepare_certificate_db(db_path)
    storage = _Storage()
    monkeypatch.setattr(maintenance, "get_media_storage_client", lambda: storage)
    monkeypatch.setattr(
        maintenance,
        "get_session_factory",
        lambda: lambda: _Session(sqlite3.connect(db_path)),
    )

    dry_run = maintenance.run_certificate_image_key_migration(
        argparse.Namespace(apply=False, limit=None)
    )
    assert dry_run["summary"]["image_candidates"] == 2
    assert dry_run["summary"]["document_skipped"] == 1
    assert {item["status"] for item in dry_run["items"]} == {"dry_run", "skipped"}
    assert storage.puts == []

    applied = maintenance.run_certificate_image_key_migration(
        argparse.Namespace(apply=True, limit=None)
    )
    assert applied["summary"]["success"] == 2
    assert [put[0] for put in storage.puts] == [
        "images/default/brand-certificates/extra.webp",
        "images/default/brand-certificates/cert.jpg",
    ]

    connection = sqlite3.connect(db_path)
    try:
        assert connection.execute(
            "SELECT file_key FROM brand_certificates WHERE id = 1"
        ).fetchone()[0] == "images/default/brand-certificates/cert.jpg"
        assert connection.execute(
            "SELECT file_key FROM brand_certificates WHERE id = 2"
        ).fetchone()[0] == "files/default/brand-certificates/report.pdf"
        assert connection.execute(
            "SELECT file_key FROM brand_certificate_images WHERE id = 9"
        ).fetchone()[0] == "images/default/brand-certificates/extra.webp"
    finally:
        connection.close()

    repeated = maintenance.run_certificate_image_key_migration(
        argparse.Namespace(apply=True, limit=None)
    )
    assert repeated["summary"]["image_candidates"] == 0
    assert repeated["summary"]["document_skipped"] == 1
