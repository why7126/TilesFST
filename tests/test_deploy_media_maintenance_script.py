from __future__ import annotations

import argparse
from io import StringIO
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
    assert "banner" in task.description
    assert "banner" in TASKS["backfill-brand-certificate-thumbnails"].description
    assert "banner" in TASKS["media-drift-reconcile"].description
    assert TASKS["media-drift-reconcile"].supports_apply is True
    assert TASKS["bug-0116-media-drift"].description == "Historical alias for media-drift-reconcile."


def test_media_maintenance_parser_documents_progress_stderr_contract() -> None:
    from app.modules.media.maintenance import build_parser

    help_text = build_parser().format_help()

    assert "--progress" in help_text
    assert "stderr" in help_text
    assert "final" in help_text
    assert "JSON stdout" in help_text


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
        "business_id_media_key_migration",
        "certificate_image_key_migration",
        "brand_logo_and_certificate_thumbnail_backfill",
        "object_key_audit",
    ]
    assert result["summary"]["can_apply"] is False
    assert result["tasks"]["object_key_audit"]["summary"]["failure_reason"] == (
        "skipped_after_object_storage_unreachable"
    )
    assert result["acceptance_summary"]["object"]["status"] == "blocked"


def test_progress_reporter_outputs_counts_and_percent_without_sensitive_values() -> None:
    from app.modules.media.maintenance import ProgressReporter

    stream = StringIO()
    reporter = ProgressReporter(
        enabled=True,
        task="backfill-image-variants",
        stage="image_variant_backfill",
        total=2,
        stream=stream,
    )

    reporter.emit(status="started")
    reporter.advance(success=1, failed=0, skipped=0)

    output = stream.getvalue()
    assert "task=backfill-image-variants" in output
    assert "stage=image_variant_backfill" in output
    assert "completed=1" in output
    assert "total=2" in output
    assert "progress_percent=50.00" in output
    assert "success=1" in output
    assert "failed=0" in output
    assert "skipped=0" in output
    assert "images/default/tiles/private.webp" not in output
    assert ".env" not in output
    assert "Authorization" not in output
    assert "Cookie" not in output


def _mock_image_variant_sources(monkeypatch) -> None:
    from app.modules.media import maintenance

    monkeypatch.setattr(maintenance, "_effective_thumbnail_max_size_kb", lambda: 0)
    monkeypatch.setattr(maintenance, "_effective_display_max_size_kb", lambda: 768)
    monkeypatch.setattr(
        maintenance,
        "_thumbnail_source_rows",
        lambda limit: [
            {
                "source_type": "sku_image",
                "source_id": 820,
                "object_key": "images/default/tiles/160/private-product.webp",
            }
        ],
    )
    monkeypatch.setattr(
        maintenance,
        "_needs_regeneration",
        lambda original_key, variant_key, **kwargs: (
            variant_key.endswith(".thumb.webp"),
            "thumbnail_missing" if variant_key.endswith(".thumb.webp") else None,
        ),
    )
    monkeypatch.setattr(
        maintenance,
        "_object_exists",
        lambda object_key: not object_key.endswith(".thumb.webp"),
    )


def test_media_maintenance_cli_keeps_stdout_json_when_progress_disabled(
    monkeypatch,
    capsys,
) -> None:
    from app.modules.media import maintenance

    _mock_image_variant_sources(monkeypatch)

    exit_code = maintenance.main(["backfill-image-variants"])
    captured = capsys.readouterr()

    assert exit_code == 0
    payload = json.loads(captured.out)
    assert payload["task"] == "backfill-image-variants"
    assert payload["summary"]["total"] == 1
    assert payload["summary"]["estimated_writes"] == 1
    assert captured.err == ""


def test_media_maintenance_cli_progress_uses_stderr_and_preserves_stdout_json(
    monkeypatch,
    capsys,
) -> None:
    from app.modules.media import maintenance

    _mock_image_variant_sources(monkeypatch)

    exit_code = maintenance.main(["backfill-image-variants", "--progress"])
    captured = capsys.readouterr()

    assert exit_code == 0
    payload = json.loads(captured.out)
    assert payload["task"] == "backfill-image-variants"
    assert "progress task=backfill-image-variants" in captured.err
    assert "stage=image_variant_backfill" in captured.err
    assert "completed=1" in captured.err
    assert "total=1" in captured.err
    assert "progress_percent=100.00" in captured.err
    assert "private-product.webp" not in captured.err
    assert "images/default/tiles/160" not in captured.err
    assert ".env" not in captured.err
    assert "Authorization" not in captured.err
    assert "Cookie" not in captured.err


def test_business_id_media_migration_progress_reports_item_io_statuses(
    monkeypatch,
    capsys,
) -> None:
    from app.modules.media import maintenance

    monkeypatch.setattr(
        maintenance,
        "_business_media_rows",
        lambda limit: [
            {
                "source_type": "brand_logo",
                "source_id": 3,
                "business_id": 3,
                "object_key": "images/default/brands/logos/private-logo.webp",
                "mime_type": None,
                "table_name": "brands",
                "column_name": "logo_object_key",
            }
        ],
    )
    monkeypatch.setattr(
        maintenance,
        "_object_exists",
        lambda object_key: object_key == "images/default/brands/logos/private-logo.webp",
    )
    monkeypatch.setattr(maintenance, "_copy_media_object_with_variants", lambda *args: None)
    monkeypatch.setattr(maintenance, "_update_business_media_reference", lambda *args: None)

    result = maintenance.run_business_id_media_key_migration(
        argparse.Namespace(apply=True, limit=None, progress=True)
    )
    captured = capsys.readouterr()

    assert result["summary"]["total"] == 1
    assert result["summary"]["success"] == 1
    assert "progress task=migrate-business-id-media-keys" in captured.err
    assert "stage=business_id_media_key_migration" in captured.err
    assert "status=checking_source" in captured.err
    assert "status=checking_target" in captured.err
    assert "status=copying_object" in captured.err
    assert "status=updating_db" in captured.err
    assert "completed=1" in captured.err
    assert "progress_percent=100.00" in captured.err
    assert "private-logo.webp" not in captured.err
    assert "images/default/brands/logos" not in captured.err


def test_media_drift_reconcile_progress_outputs_stage_progress(monkeypatch, capsys) -> None:
    from app.modules.media import maintenance

    def fake_task(task: str) -> dict[str, object]:
        return {
            "task": task,
            "summary": {"total": 1, "failed": 0, "retry_candidates": 0, "non_standard": 0},
            "items": [],
        }

    monkeypatch.setattr(
        maintenance,
        "run_pending_tile_formalization",
        lambda args: fake_task("formalize-pending-tile-images"),
    )
    monkeypatch.setattr(
        maintenance,
        "run_business_id_media_key_migration",
        lambda args: fake_task("migrate-business-id-media-keys"),
    )
    monkeypatch.setattr(
        maintenance,
        "run_certificate_image_key_migration",
        lambda args: {
            **fake_task("migrate-certificate-image-keys"),
            "summary": {"total": 1, "image_candidates": 0, "failed": 0, "retry_candidates": 0},
        },
    )
    monkeypatch.setattr(
        maintenance,
        "run_thumbnail_backfill",
        lambda args: fake_task("backfill-brand-certificate-thumbnails"),
    )
    monkeypatch.setattr(
        maintenance,
        "run_object_key_audit",
        lambda args: fake_task("object-key-audit"),
    )

    result = maintenance.run_bug_0116_media_drift(
        argparse.Namespace(apply=False, limit=None, progress=True, task="media-drift-reconcile")
    )
    captured = capsys.readouterr()

    assert result["task"] == "media-drift-reconcile"
    assert result["summary"]["task_count"] == 5
    assert "stage=sku_pending_formalization" in captured.err
    assert "stage=business_id_media_key_migration" in captured.err
    assert "stage=certificate_image_key_migration" in captured.err
    assert "stage=brand_logo_and_certificate_thumbnail_backfill" in captured.err
    assert "stage=object_key_audit" in captured.err
    assert "completed=5" in captured.err
    assert "progress_percent=100.00" in captured.err
