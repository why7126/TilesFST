from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from app.core.error_codes import STORAGE_UNAVAILABLE
from app.core.exceptions import AppError
from app.modules.media.storage import MEDIA_NOT_FOUND, MediaObjectInfo


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "deploy" / "scripts" / "media-maintenance.sh"


def test_media_maintenance_script_has_valid_shell_syntax() -> None:
    result = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_media_maintenance_script_defaults_to_read_only_audit() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    assert 'DOMAIN="${1:-prod}"' in content
    assert 'ENVIRONMENT="${2:-mysql-tencent-cos}"' in content
    assert 'TASK="${3:-object-key-audit}"' in content
    assert "--apply --confirm-backup" in content
    assert "media-drift-reconcile 为生产推荐聚合入口" in content
    assert "bug-0116-media-drift 仅作为历史兼容别名" in content
    assert "不输出 env 内容、数据库连接串或对象存储密钥" in content


def test_media_maintenance_module_exposes_image_variant_backfill_task() -> None:
    from app.modules.media.maintenance import TASKS

    task = TASKS["backfill-image-variants"]

    assert task.supports_apply is True
    assert "thumbnail and display variants" in task.description
    assert TASKS["media-drift-reconcile"].supports_apply is True
    assert TASKS["bug-0116-media-drift"].description == "Historical alias for media-drift-reconcile."


class _StorageUnavailable:
    def get_object_info(self, object_key: str) -> MediaObjectInfo:
        raise AppError(status_code=502, code=STORAGE_UNAVAILABLE, message="对象存储不可用")


class _StorageMissing:
    def get_object_info(self, object_key: str) -> MediaObjectInfo:
        raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体文件不存在")


def test_media_maintenance_dry_run_blocks_when_object_storage_unreachable(monkeypatch) -> None:
    from app.core.config import settings
    from app.modules.media import maintenance

    monkeypatch.setattr(settings, "object_storage_bucket", "prod-private-bucket")
    monkeypatch.setattr(settings, "object_storage_provider", "tencent-cos")
    monkeypatch.setattr(settings, "object_storage_auto_create_bucket", False)
    monkeypatch.setattr(maintenance, "get_media_storage_client", lambda: _StorageUnavailable())
    monkeypatch.setattr(maintenance, "_effective_thumbnail_max_size_kb", lambda: 0)
    monkeypatch.setattr(
        maintenance,
        "_thumbnail_source_rows",
        lambda limit: [
            {
                "source_type": "brand_logo",
                "source_id": 1,
                "object_key": "images/default/brands/logos/private-logo.webp",
            }
        ],
    )

    result = maintenance.run_thumbnail_backfill(argparse.Namespace(apply=False, limit=None))

    assert result["status"] == "blocked"
    assert result["summary"]["failure_category"] == "object_storage_unreachable"
    assert result["summary"]["affected_tasks"] == ["backfill-brand-certificate-thumbnails"]
    assert result["summary"]["can_apply"] is False
    assert result["acceptance_summary"]["object"]["status"] == "blocked"
    assert result["acceptance_summary"]["thumbnail_benefit"]["status"] == "blocked"
    maintenance._assert_no_sensitive_output(result)

    payload = json.dumps(result, ensure_ascii=False)
    assert "prod-private-bucket" not in payload
    assert "private-logo.webp" not in payload
    assert "secret" not in payload.lower()


def test_media_maintenance_keeps_missing_objects_as_missing_statistics(monkeypatch) -> None:
    from app.modules.media import maintenance

    monkeypatch.setattr(maintenance, "get_media_storage_client", lambda: _StorageMissing())
    monkeypatch.setattr(maintenance, "_effective_thumbnail_max_size_kb", lambda: 0)
    monkeypatch.setattr(maintenance, "_effective_display_max_size_kb", lambda: 0)
    monkeypatch.setattr(
        maintenance,
        "_pending_tile_rows",
        lambda limit: [
            {
                "tile_id": 42,
                "image_id": 7,
                "object_key": "images/default/tiles/pending/missing-main.jpg",
            }
        ],
    )

    result = maintenance.run_pending_tile_formalization(argparse.Namespace(apply=False, limit=None))

    assert "status" not in result
    assert result["summary"]["missing_original"] == 1
    assert result["summary"]["missing_thumbnail"] == 1
    assert result["items"][0]["original_exists"] is False
    assert result["items"][0]["thumbnail_exists"] is False
    assert result["acceptance_summary"]["object"]["status"] == "pass"


def test_media_maintenance_aggregate_propagates_storage_block(monkeypatch) -> None:
    from app.modules.media import maintenance

    monkeypatch.setattr(maintenance, "get_media_storage_client", lambda: _StorageUnavailable())
    monkeypatch.setattr(maintenance, "_effective_thumbnail_max_size_kb", lambda: 0)
    monkeypatch.setattr(maintenance, "_effective_display_max_size_kb", lambda: 0)
    monkeypatch.setattr(
        maintenance,
        "_pending_tile_rows",
        lambda limit: [
            {
                "tile_id": 42,
                "image_id": 7,
                "object_key": "images/default/tiles/pending/private-main.jpg",
            }
        ],
    )

    result = maintenance.run_bug_0116_media_drift(argparse.Namespace(apply=False, limit=None))

    assert result["status"] == "blocked"
    assert result["summary"]["failure_category"] == "object_storage_unreachable"
    assert result["summary"]["affected_tasks"] == [
        "sku_pending_formalization",
        "certificate_image_key_migration",
        "brand_logo_and_certificate_thumbnail_backfill",
        "object_key_audit",
    ]
    assert result["summary"]["can_apply"] is False
    assert result["tasks"]["object_key_audit"]["summary"]["failure_reason"] == (
        "skipped_after_object_storage_unreachable"
    )
    assert result["acceptance_summary"]["object"]["status"] == "blocked"
