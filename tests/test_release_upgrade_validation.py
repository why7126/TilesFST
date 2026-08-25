from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-release-upgrade.py"
SPEC = importlib.util.spec_from_file_location("validate_release_upgrade_script", SCRIPT)
assert SPEC and SPEC.loader
upgrade = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(upgrade)


def write_release(root: Path, version: str, *, image_manifest: bool = True, database: str = "none") -> None:
    release_dir = root / "releases" / version
    release_dir.mkdir(parents=True)
    (release_dir / "announcement.mdx").write_text("# Release\n", encoding="utf-8")
    (release_dir / "release.json").write_text(
        json.dumps(
            {
                "version": version,
                "image_required": image_manifest,
                "image_manifest": "image-manifest.json",
                "impact_scope": {"database": database},
                "announcement": "announcement.mdx",
            }
        ),
        encoding="utf-8",
    )
    if image_manifest:
        (release_dir / "image-manifest.json").write_text(json.dumps({"version": version, "image_tag": version}), encoding="utf-8")


def write_env_example(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_fresh_install_supported_with_release_and_manifest(tmp_path: Path) -> None:
    write_release(tmp_path, "v1.0.0")
    write_env_example(tmp_path, ".env.example", "APP_ENV=production\nTILESFST_IMAGE_TAG=v1.0.0\n")
    (tmp_path / "src" / "shared").mkdir(parents=True)
    (tmp_path / "src" / "shared" / "product-version.ts").write_text("export const PRODUCT_VERSION = 'v1.0.0';\n", encoding="utf-8")

    plan = upgrade.build_plan("fresh", "v1.0.0", tmp_path)

    assert plan["support_level"] == "fresh-install-supported"
    assert plan["source_confidence"] == "fresh"
    assert plan["blockers"] == []


def test_adjacent_upgrade_supported_when_previous_release_exists(tmp_path: Path) -> None:
    write_release(tmp_path, "v1.0.0")
    write_release(tmp_path, "v1.0.1")

    plan = upgrade.build_plan("v1.0.0", "v1.0.1", tmp_path)

    assert plan["support_level"] == "adjacent-upgrade-supported"
    assert plan["source_confidence"] == "verified"


def test_cross_version_requires_manual_review_when_intermediate_manifest_missing(tmp_path: Path) -> None:
    write_release(tmp_path, "v0.0.5", image_manifest=False)
    write_release(tmp_path, "v1.0.0", image_manifest=False)
    write_release(tmp_path, "v1.1.2")

    plan = upgrade.build_plan("v0.0.5", "v1.1.2", tmp_path)

    assert plan["support_level"] == "cross-version-upgrade-requires-manual-review"
    assert any("missing_manifest" in warning for warning in plan["warnings"])


def test_official_v112_upgrade_plans_only_include_confirmed_paths() -> None:
    plans = {path.name for path in (ROOT / "releases" / "v1.1.2" / "upgrade-plans").glob("*.json")}

    assert plans == {"fresh-to-v1.1.2.json", "v1.1.1-to-v1.1.2.json"}


def test_default_release_from_versions_include_fresh_and_previous_only(tmp_path: Path) -> None:
    write_release(tmp_path, "v1.0.0")
    write_release(tmp_path, "v1.0.1")
    write_release(tmp_path, "v1.1.2")

    assert upgrade.default_release_from_versions("v1.1.2", tmp_path) == ["fresh", "v1.0.1"]


def test_default_release_from_versions_for_first_release_is_fresh_only(tmp_path: Path) -> None:
    write_release(tmp_path, "v1.0.0")

    assert upgrade.default_release_from_versions("v1.0.0", tmp_path) == ["fresh"]


def test_env_diff_reports_added_changed_required_and_unsafe(tmp_path: Path) -> None:
    before = {"a.env.example": {"APP_ENV": "development", "OLD_KEY": "1"}}
    after = {"a.env.example": {"APP_ENV": "production", "APP_SECRET_KEY": "change-me", "NEW_KEY": "2"}}

    diff = upgrade.diff_env_snapshots(before, after)

    assert {"path": "a.env.example", "key": "NEW_KEY", "recommendation": "确认生产环境是否需要显式配置"} in diff["added"]
    assert any(item["key"] == "OLD_KEY" for item in diff["removed"])
    assert any(item["key"] == "APP_ENV" for item in diff["changed_default"])
    assert any(item["key"] == "APP_SECRET_KEY" for item in diff["required_in_production"])
    assert any(item["key"] == "APP_SECRET_KEY" for item in diff["unsafe_example_value"])


def test_validate_plan_rejects_sensitive_content() -> None:
    data = {
        "from_version": "v1.0.0",
        "to_version": "v1.0.1",
        "support_level": "adjacent-upgrade-supported",
        "source_confidence": "verified",
        "impact_summary": {},
        "required_checks": [],
        "steps": [],
        "rollback": {
            "previous_image": "v1.0.0",
            "target_image": "v1.0.1",
            "env_snapshot": "DATABASE_URL=mysql+pymysql://user:pass@example/db",
            "database_backup": "required",
            "object_storage_backup": "required",
            "rollback_steps": [],
            "post_rollback_smoke": "pending",
        },
        "blockers": [],
        "warnings": [],
        "evidence": {},
    }

    errors = upgrade.validate_plan_data(data)

    assert any("sensitive pattern" in error for error in errors)
