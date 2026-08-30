import argparse
import sqlite3

import pytest

from app.modules.media.storage import ImageThumbnailResult, MediaObjectInfo, StoredMediaObject
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


def test_media_drift_reconcile_apply_requires_confirm_backup():
    args = maintenance.build_parser().parse_args(["media-drift-reconcile", "--apply"])

    with pytest.raises(ValueError, match="--apply requires --confirm-backup"):
        maintenance.run(args)


def test_bug_0116_aggregate_alias_remains_supported():
    args = maintenance.build_parser().parse_args(["bug-0116-media-drift", "--apply"])

    with pytest.raises(ValueError, match="--apply requires --confirm-backup"):
        maintenance.run(args)


def test_media_drift_reconcile_reports_semantic_task_name(monkeypatch):
    args = maintenance.build_parser().parse_args(["media-drift-reconcile", "--limit", "5"])
    monkeypatch.setattr(
        maintenance,
        "run_pending_tile_formalization",
        lambda _args: {
            "summary": {"total": 0, "failed": 0, "retry_candidates": 0},
            "acceptance_summary": {},
        },
    )
    monkeypatch.setattr(
        maintenance,
        "run_business_id_media_key_migration",
        lambda _args: {
            "summary": {"candidates": 0, "failed": 0, "retry_candidates": 0},
            "acceptance_summary": {},
        },
    )
    monkeypatch.setattr(
        maintenance,
        "run_certificate_image_key_migration",
        lambda _args: {
            "summary": {"image_candidates": 0, "failed": 0, "retry_candidates": 0},
            "acceptance_summary": {},
        },
    )
    monkeypatch.setattr(
        maintenance,
        "run_thumbnail_backfill",
        lambda _args: {
            "summary": {"retry_candidates": 0, "failed": 0},
            "acceptance_summary": {},
        },
    )
    monkeypatch.setattr(
        maintenance,
        "run_object_key_audit",
        lambda _args: {
            "summary": {"non_standard": 0, "failed": 0, "retry_candidates": 0},
            "acceptance_summary": {},
        },
    )

    result = maintenance.run(args)

    assert result["task"] == "media-drift-reconcile"
    assert result["acceptance_summary"]["task"] == "media-drift-reconcile"


def test_media_drift_reconcile_reports_banner_thumbnail_candidates(monkeypatch):
    args = maintenance.build_parser().parse_args(["media-drift-reconcile", "--limit", "5"])
    monkeypatch.setattr(
        maintenance,
        "run_pending_tile_formalization",
        lambda _args: {
            "summary": {"total": 0, "failed": 0, "retry_candidates": 0},
            "acceptance_summary": {},
        },
    )
    monkeypatch.setattr(
        maintenance,
        "run_business_id_media_key_migration",
        lambda _args: {
            "summary": {"candidates": 0, "failed": 0, "retry_candidates": 0},
            "acceptance_summary": {},
        },
    )
    monkeypatch.setattr(
        maintenance,
        "run_certificate_image_key_migration",
        lambda _args: {
            "summary": {"image_candidates": 0, "failed": 0, "retry_candidates": 0},
            "acceptance_summary": {},
        },
    )
    monkeypatch.setattr(
        maintenance,
        "run_thumbnail_backfill",
        lambda _args: {
            "summary": {"retry_candidates": 2, "failed": 0},
            "items": [{"source_type": "banner_image"}],
            "acceptance_summary": {},
        },
    )
    monkeypatch.setattr(
        maintenance,
        "run_object_key_audit",
        lambda _args: {
            "summary": {"non_standard": 0, "failed": 0, "retry_candidates": 0},
            "acceptance_summary": {},
        },
    )

    result = maintenance.run(args)

    assert result["summary"]["thumbnail_candidates"] == 2
    assert result["summary"]["retry_candidates"] == 2


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


def test_business_id_media_key_migration_copies_objects_and_updates_reference(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "media.db"
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(
            """
            CREATE TABLE users (id TEXT PRIMARY KEY, avatar_object_key TEXT);
            CREATE TABLE brands (id INTEGER PRIMARY KEY, logo_object_key TEXT);
            CREATE TABLE banners (
              id INTEGER PRIMARY KEY,
              image_object_key TEXT,
              image_source TEXT
            );
            CREATE TABLE tile_images (
              id INTEGER PRIMARY KEY,
              tile_id INTEGER,
              object_key TEXT,
              url TEXT
            );
            CREATE TABLE tile_videos (
              id INTEGER PRIMARY KEY,
              tile_id INTEGER,
              object_key TEXT
            );
            CREATE TABLE brand_certificates (
              id INTEGER PRIMARY KEY,
              file_key TEXT,
              file_mime_type TEXT,
              file_url TEXT,
              deleted_at TEXT
            );
            CREATE TABLE brand_certificate_images (
              id INTEGER PRIMARY KEY,
              certificate_id INTEGER,
              file_key TEXT,
              file_mime_type TEXT,
              file_url TEXT
            );
            INSERT INTO brands VALUES (7, 'images/default/brands/logos/logo.webp');
            INSERT INTO users VALUES (
              '21357eda-dd12-454b-bd4a-3d3423e4d155',
              'images/default/users/avatars/avatar.webp'
            );
            """
        )
        connection.commit()
    finally:
        connection.close()

    storage = _Storage()
    storage.objects = {
        "images/default/brands/logos/logo.webp": StoredMediaObject(b"logo", "image/webp"),
        "images/default/brands/logos/logo.thumb.webp": StoredMediaObject(b"thumb", "image/webp"),
        "images/default/brands/logos/logo.display.webp": StoredMediaObject(b"display", "image/webp"),
        "images/default/users/avatars/avatar.webp": StoredMediaObject(b"avatar", "image/webp"),
    }
    monkeypatch.setattr(
        maintenance,
        "get_session_factory",
        lambda: lambda: _Session(sqlite3.connect(db_path)),
    )
    monkeypatch.setattr(maintenance, "get_media_storage_client", lambda: storage)

    args = maintenance.build_parser().parse_args(["migrate-business-id-media-keys"])
    dry_run = maintenance.run(args)
    assert dry_run["summary"]["candidates"] == 2
    assert dry_run["items"][0]["target"]["object_key_prefix"] == "images/default/brand-logos/7"
    assert dry_run["items"][1]["target"]["object_key_prefix"] == (
        "images/default/user-avatars/21357eda-dd12-454b-bd4a-3d3423e4d155"
    )

    apply_args = maintenance.build_parser().parse_args(
        ["migrate-business-id-media-keys", "--apply", "--confirm-backup"]
    )
    applied = maintenance.run(apply_args)

    assert applied["summary"]["success"] == 2
    assert (
        "images/default/brand-logos/7/logo.webp",
        b"logo",
        "image/webp",
    ) in storage.puts
    assert (
        "images/default/brand-logos/7/logo.thumb.webp",
        b"thumb",
        "image/webp",
    ) in storage.puts
    with sqlite3.connect(db_path) as check:
        key = check.execute("SELECT logo_object_key FROM brands WHERE id = 7").fetchone()[0]
        avatar_key = check.execute(
            "SELECT avatar_object_key FROM users WHERE id = ?",
            ("21357eda-dd12-454b-bd4a-3d3423e4d155",),
        ).fetchone()[0]
    assert key == "images/default/brand-logos/7/logo.webp"
    assert avatar_key == (
        "images/default/user-avatars/21357eda-dd12-454b-bd4a-3d3423e4d155/avatar.webp"
    )


def test_object_key_audit_reports_invalid_avatar_spelling() -> None:
    assert (
        maintenance._object_key_issue(
            source_type="user_avatar",
            object_key="images/default/users/1/avartars/avatar.webp",
        )
        == "invalid_avatar_directory_spelling"
    )


def test_pending_tile_formalization_dry_run_uses_acceptance_summary(monkeypatch):
    args = argparse.Namespace(apply=False, limit=1, confirm_backup=False)
    monkeypatch.setattr(maintenance, "_effective_thumbnail_max_size_kb", lambda: 20)
    monkeypatch.setattr(maintenance, "_effective_display_max_size_kb", lambda: 512)
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
    assert result["summary"]["thumbnail_max_size_kb"] == 20
    assert result["summary"]["display_max_size_kb"] == 512
    assert result["items"][0]["source"]["object_key_prefix"] == (
        "images/default/tiles/pending"
    )
    assert result["acceptance_summary"]["render"]["status"] == "blocked"


def test_thumbnail_backfill_counts_same_size_and_same_bytes(monkeypatch):
    args = argparse.Namespace(apply=False, limit=None, confirm_backup=False)
    monkeypatch.setattr(maintenance, "_effective_thumbnail_max_size_kb", lambda: 20)
    storage = _Storage()
    storage.objects = {
        "images/default/brands/logos/logo.jpg": StoredMediaObject(b"same", "image/jpeg"),
        "images/default/brands/logos/logo.thumb.webp": StoredMediaObject(
            b"same",
            "image/webp",
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
    assert result["summary"]["estimated_writes"] == 1
    assert result["summary"]["thumbnail_max_size_kb"] == 20
    assert result["summary"]["same_size"] == 1
    assert result["summary"]["same_bytes"] == 1
    assert result["items"][0]["reason"] == "thumbnail_copied_original"


def test_thumbnail_backfill_counts_existing_thumbnail_above_target(monkeypatch):
    args = argparse.Namespace(apply=False, limit=None, confirm_backup=False)
    monkeypatch.setattr(maintenance, "_effective_thumbnail_max_size_kb", lambda: 20)
    storage = _Storage()
    storage.objects = {
        "images/default/brands/logos/logo.jpg": StoredMediaObject(
            b"original-content" * 4096,
            "image/jpeg",
        ),
        "images/default/brands/logos/logo.thumb.webp": StoredMediaObject(
            b"thumb-content" * 2048,
            "image/webp",
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
    assert result["summary"]["estimated_writes"] == 1
    assert result["summary"]["exceeds_target_size"] == 1
    assert result["summary"]["already_conformant"] == 0
    assert result["items"][0]["reason"] == "thumbnail_exceeds_target_size"


def test_image_variant_backfill_uses_display_target(monkeypatch):
    args = argparse.Namespace(apply=False, limit=None, confirm_backup=False)
    monkeypatch.setattr(maintenance, "_effective_thumbnail_max_size_kb", lambda: 20)
    monkeypatch.setattr(maintenance, "_effective_display_max_size_kb", lambda: 512)
    storage = _Storage()
    storage.objects = {
        "images/default/brands/logos/logo.jpg": StoredMediaObject(
            b"original-content" * 4096,
            "image/jpeg",
        ),
        "images/default/brands/logos/logo.thumb.webp": StoredMediaObject(
            b"thumb-content",
            "image/webp",
        ),
        "images/default/brands/logos/logo.display.webp": StoredMediaObject(
            b"display-content" * 1024,
            "image/webp",
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

    result = maintenance.run_image_variant_backfill(args)

    assert result["summary"]["display_max_size_kb"] == 512
    assert result["summary"]["display_no_benefit"] == 0
    assert result["items"][0]["display_max_size_kb"] == 512


def test_thumbnail_source_rows_include_sku_brand_and_certificate_images(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "catalog.db"
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(
            """
            CREATE TABLE tile_images (
                id INTEGER PRIMARY KEY,
                object_key TEXT
            );
            CREATE TABLE brands (
                id INTEGER PRIMARY KEY,
                logo_object_key TEXT
            );
            CREATE TABLE banners (
                id INTEGER PRIMARY KEY,
                image_object_key TEXT,
                image_source TEXT
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
            INSERT INTO tile_images VALUES (
                1,
                'images/default/tiles/42/main.webp'
            );
            INSERT INTO brands VALUES (
                2,
                'images/default/brands/logos/logo.webp'
            );
            INSERT INTO banners VALUES (
                5,
                'images/default/banners/banner.png',
                'custom_upload'
            );
            INSERT INTO banners VALUES (
                6,
                'images/default/banners/imported.png',
                'seed'
            );
            INSERT INTO banners VALUES (
                7,
                'images/default/brands/logos/reused-banner.png',
                'brand_logo'
            );
            INSERT INTO brand_certificates VALUES (
                3,
                NULL,
                'images/default/brand-certificates/cert.webp',
                'image/webp'
            );
            INSERT INTO brand_certificate_images VALUES (
                4,
                'images/default/brand-certificates/extra.webp',
                'image/webp'
            );
            """
        )
        connection.commit()
    finally:
        connection.close()
    monkeypatch.setattr(
        maintenance,
        "get_session_factory",
        lambda: lambda: _Session(sqlite3.connect(db_path)),
    )

    rows = maintenance._thumbnail_source_rows(limit=None)

    assert {row["source_type"] for row in rows} == {
        "sku_image",
        "banner_image",
        "brand_logo",
        "certificate_file",
        "certificate_image",
    }
    assert {row["object_key"] for row in rows} == {
        "images/default/tiles/42/main.webp",
        "images/default/banners/banner.png",
        "images/default/banners/imported.png",
        "images/default/brands/logos/logo.webp",
        "images/default/brand-certificates/cert.webp",
        "images/default/brand-certificates/extra.webp",
    }
    assert "images/default/brands/logos/reused-banner.png" not in {
        row["object_key"] for row in rows
    }


def test_image_variant_backfill_includes_banner_thumbnail_and_display(monkeypatch):
    args = argparse.Namespace(apply=False, limit=None, confirm_backup=False)
    monkeypatch.setattr(maintenance, "_effective_thumbnail_max_size_kb", lambda: 20)
    monkeypatch.setattr(maintenance, "_effective_display_max_size_kb", lambda: 768)
    storage = _Storage()
    storage.objects = {
        "images/default/banners/banner.png": StoredMediaObject(b"original", "image/png"),
    }
    monkeypatch.setattr(maintenance, "get_media_storage_client", lambda: storage)
    monkeypatch.setattr(
        maintenance,
        "_thumbnail_source_rows",
        lambda limit: [
            {
                "source_type": "banner_image",
                "source_id": 5,
                "object_key": "images/default/banners/banner.png",
                "mime_type": "image/png",
            }
        ],
    )

    result = maintenance.run_image_variant_backfill(args)

    assert result["summary"]["total"] == 1
    assert result["summary"]["thumbnail_missing"] == 1
    assert result["summary"]["display_missing"] == 1
    assert result["summary"]["retry_candidates"] == 1
    assert result["summary"]["estimated_writes"] == 2
    assert result["items"][0]["source_type"] == "banner_image"
    assert result["items"][0]["needs"]["thumbnail"] is True
    assert result["items"][0]["needs"]["display"] is True
    assert result["items"][0]["needs"]["banner_legacy_thumbnail"] is False
    assert result["items"][0]["needs"]["banner_legacy_display"] is False
    payload = str(result)
    assert "banner.png" not in payload


def test_image_variant_backfill_apply_generates_banner_webp_variants(monkeypatch):
    args = argparse.Namespace(apply=True, limit=None, confirm_backup=True)
    monkeypatch.setattr(maintenance, "_effective_thumbnail_max_size_kb", lambda: 20)
    monkeypatch.setattr(maintenance, "_effective_display_max_size_kb", lambda: 768)
    storage = _Storage()
    storage.objects = {
        "images/default/banners/banner.png": StoredMediaObject(b"original", "image/png"),
    }
    monkeypatch.setattr(maintenance, "get_media_storage_client", lambda: storage)
    monkeypatch.setattr(
        maintenance,
        "_thumbnail_source_rows",
        lambda limit: [
            {
                "source_type": "banner_image",
                "source_id": 5,
                "object_key": "images/default/banners/banner.png",
                "mime_type": "image/png",
            }
        ],
    )
    monkeypatch.setattr(
        maintenance,
        "generate_image_thumbnail",
        lambda content, content_type, **kwargs: ImageThumbnailResult(
            content=b"webp-variant",
            content_type="image/webp",
            width=100,
            height=100,
            original_width=200,
            original_height=200,
            original_size=len(content),
            size=len(b"webp-variant"),
            resized=True,
        ),
    )

    result = maintenance.run_image_variant_backfill(args)

    assert result["summary"]["success"] == 2
    assert [put[0] for put in storage.puts] == [
        "images/default/banners/banner.thumb.webp",
        "images/default/banners/banner.display.webp",
    ]
    assert {put[2] for put in storage.puts} == {"image/webp"}


def test_image_variant_backfill_generates_legacy_banner_aliases(monkeypatch):
    args = argparse.Namespace(apply=True, limit=None, confirm_backup=True)
    monkeypatch.setattr(maintenance, "_effective_thumbnail_max_size_kb", lambda: 20)
    monkeypatch.setattr(maintenance, "_effective_display_max_size_kb", lambda: 768)
    storage = _Storage()
    storage.objects = {
        "images/default/banners/14/banner.png": StoredMediaObject(b"original", "image/png"),
        "images/default/banners/14/banner.thumb.webp": StoredMediaObject(
            b"canonical-thumb",
            "image/webp",
        ),
        "images/default/banners/14/banner.display.webp": StoredMediaObject(
            b"canonical-display",
            "image/webp",
        ),
    }
    monkeypatch.setattr(maintenance, "get_media_storage_client", lambda: storage)
    monkeypatch.setattr(
        maintenance,
        "_thumbnail_source_rows",
        lambda limit: [
            {
                "source_type": "banner_image",
                "source_id": 14,
                "object_key": "images/default/banners/14/banner.png",
                "mime_type": "image/png",
            }
        ],
    )

    result = maintenance.run_image_variant_backfill(args)

    assert result["summary"]["retry_candidates"] == 1
    assert result["summary"]["estimated_writes"] == 2
    assert result["summary"]["banner_legacy_alias_missing"] == 1
    assert result["summary"]["banner_legacy_alias_writes"] == 2
    assert result["summary"]["success"] == 2
    assert result["items"][0]["needs"] == {
        "thumbnail": False,
        "display": False,
        "banner_legacy_thumbnail": True,
        "banner_legacy_display": True,
    }
    assert [put[0] for put in storage.puts] == [
        "images/default/banners/banner.thumb.webp",
        "images/default/banners/banner.display.webp",
    ]
    assert storage.objects["images/default/banners/banner.thumb.webp"].content == b"canonical-thumb"
    assert storage.objects["images/default/banners/banner.display.webp"].content == b"canonical-display"


def test_thumbnail_backfill_includes_banner_candidate(monkeypatch):
    args = argparse.Namespace(apply=False, limit=None, confirm_backup=False)
    monkeypatch.setattr(maintenance, "_effective_thumbnail_max_size_kb", lambda: 20)
    storage = _Storage()
    storage.objects = {
        "images/default/banners/banner.png": StoredMediaObject(b"original", "image/png"),
    }
    monkeypatch.setattr(maintenance, "get_media_storage_client", lambda: storage)
    monkeypatch.setattr(
        maintenance,
        "_thumbnail_source_rows",
        lambda limit: [
            {
                "source_type": "banner_image",
                "source_id": 5,
                "object_key": "images/default/banners/banner.png",
                "mime_type": "image/png",
            }
        ],
    )

    result = maintenance.run_thumbnail_backfill(args)

    assert result["summary"]["total"] == 1
    assert result["summary"]["missing_thumbnail"] == 1
    assert result["summary"]["retry_candidates"] == 1
    assert result["summary"]["estimated_writes"] == 1
    assert result["items"][0]["source_type"] == "banner_image"


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
