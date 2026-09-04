from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-release.py"
IMAGE_SCRIPT = ROOT / "scripts" / "validate-image-build.py"
USAGE_SCRIPT = ROOT / "scripts" / "validate-usage-docs.py"
GENERATE_USAGE_SCRIPT = ROOT / "scripts" / "generate-usage-docs.py"
SPEC = importlib.util.spec_from_file_location("validate_release_script", SCRIPT)
assert SPEC and SPEC.loader
validate_release_script = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_release_script)
IMAGE_SPEC = importlib.util.spec_from_file_location("validate_image_build_script", IMAGE_SCRIPT)
assert IMAGE_SPEC and IMAGE_SPEC.loader
validate_image_build_script = importlib.util.module_from_spec(IMAGE_SPEC)
IMAGE_SPEC.loader.exec_module(validate_image_build_script)
USAGE_SPEC = importlib.util.spec_from_file_location("validate_usage_docs_script", USAGE_SCRIPT)
assert USAGE_SPEC and USAGE_SPEC.loader
validate_usage_docs_script = importlib.util.module_from_spec(USAGE_SPEC)
USAGE_SPEC.loader.exec_module(validate_usage_docs_script)
GENERATE_USAGE_SPEC = importlib.util.spec_from_file_location("generate_usage_docs_script", GENERATE_USAGE_SCRIPT)
assert GENERATE_USAGE_SPEC and GENERATE_USAGE_SPEC.loader
generate_usage_docs_script = importlib.util.module_from_spec(GENERATE_USAGE_SPEC)
GENERATE_USAGE_SPEC.loader.exec_module(generate_usage_docs_script)


def write_release(tmp_path: Path, *, version: str = "v0.1.0", gate_status: str = "pass", announcement: str = "# Release\n\nPublic notes.") -> tuple[Path, Path]:
    root = tmp_path
    release_dir = root / "releases" / version
    release_dir.mkdir(parents=True)
    (root / "releases" / "mint.json").write_text('{"name":"test"}', encoding="utf-8")
    product_version = root / "product-version.ts"
    product_version.write_text(f"export const PRODUCT_VERSION = '{version}';\n", encoding="utf-8")
    gates = {
        name: {"status": gate_status, "evidence": "checked"} for name in validate_release_script.REQUIRED_GATES
    }
    data = {
        "version": version,
        "release_time": "2026-07-02 14:56:58",
        "owner": "product",
        "formal_scope_only": True,
        "version_change_rationale": "",
        "image_required": False,
        "image_required_rationale": "no backend, database, docker, or image delivery impact",
        "image_tag": version,
        "image_plan": "image-build-plan.json",
        "image_manifest": "image-manifest.json",
        "external_image_build_evidence": {"status": "na", "rationale": "not required"},
        "sprints": ["sprint-004"],
        "requirements": [],
        "bugs": [],
        "changes": [],
        "gates": gates,
        "known_issues": [],
        "upgrade_steps": ["deploy"],
        "rollback": {"conditions": ["smoke failed"], "steps": ["rollback"]},
        "impact_scope": {
            "web_admin": "none",
            "owner_web": "none",
            "miniapp": "none",
            "backend": "none",
            "database": "none",
            "object_storage": "none",
            "docker": "none",
        },
        "announcement": "announcement.mdx",
    }
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")
    (release_dir / "announcement.mdx").write_text(announcement, encoding="utf-8")
    return release_dir, product_version


def test_validate_release_passes(tmp_path: Path) -> None:
    release_dir, product_version = write_release(tmp_path)
    assert validate_release_script.validate_release(release_dir, product_version) == []


def test_release_validation_does_not_apply_evidence_source_diagnostics_by_default(tmp_path: Path) -> None:
    release_dir, product_version = write_release(tmp_path)
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    data["known_issues"] = [
        {
            "status": "passed",
            "source": "network_trial",
            "summary": "diagnostic-only record without locator evidence",
        }
    ]
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")
    write_upgrade_plan(release_dir, from_version="fresh", to_version="v0.1.0")
    write_upgrade_plan(release_dir, from_version="v0.0.5", to_version="v0.1.0")

    assert validate_release_script.validate_release(release_dir, product_version, stage="publish") == []


def test_version_mismatch_blocks_release_even_with_rationale(tmp_path: Path) -> None:
    release_dir, product_version = write_release(tmp_path, version="v0.1.0")
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    data["version_change_rationale"] = "temporary draft note"
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")
    product_version.write_text("export const PRODUCT_VERSION = 'v0.0.1';\n", encoding="utf-8")
    errors = validate_release_script.validate_release(release_dir, product_version, stage="publish")
    assert any("product version mismatch blocks publish" in error for error in errors)
    assert any("/image-prepare v0.1.0" in error and "/image-build v0.1.0" in error for error in errors)


def test_release_prepare_syncs_product_version_sources_and_metadata(tmp_path: Path, monkeypatch) -> None:
    release_dir, product_version = write_release(
        tmp_path,
        version="v2.0.0",
        announcement=(
            "---\n"
            "title: 产品版本 v1.9.9\n"
            "---\n\n"
            "# 产品版本 v1.9.9\n\n"
            "## 发布注意事项\n\n"
            "- 当前产品版本号仍需在发布准备阶段更新为 `v2.0.0`。\n"
        ),
    )
    miniapp_dir = tmp_path / "src" / "miniapp" / "utils"
    miniapp_dir.mkdir(parents=True)
    miniapp_ts = miniapp_dir / "product-version.ts"
    miniapp_js = miniapp_dir / "product-version.js"
    product_version.write_text("export const PRODUCT_VERSION = 'v1.9.9';\n", encoding="utf-8")
    miniapp_ts.write_text("export const PRODUCT_VERSION = 'v1.9.8';\n", encoding="utf-8")
    miniapp_js.write_text("const PRODUCT_VERSION = 'v1.9.7';\nmodule.exports = { PRODUCT_VERSION };\n", encoding="utf-8")
    monkeypatch.setattr(validate_release_script, "PRODUCT_VERSION_FILE", product_version.resolve())
    monkeypatch.setattr(validate_release_script, "MINIAPP_PRODUCT_VERSION_FILES", (miniapp_ts.resolve(), miniapp_js.resolve()))

    result = validate_release_script.sync_release_product_versions(release_dir, product_version.resolve())

    assert result["version"] == "v2.0.0"
    assert "export const PRODUCT_VERSION = 'v2.0.0'" in product_version.read_text(encoding="utf-8")
    assert "export const PRODUCT_VERSION = 'v2.0.0'" in miniapp_ts.read_text(encoding="utf-8")
    assert "const PRODUCT_VERSION = 'v2.0.0'" in miniapp_js.read_text(encoding="utf-8")
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    assert data["gates"]["product_version"]["status"] == "pass"
    assert data["product_version_sync"]["status"] == "synced"
    announcement = (release_dir / "announcement.mdx").read_text(encoding="utf-8")
    assert "title: 产品版本 v2.0.0" in announcement
    assert "# 产品版本 v2.0.0" in announcement
    assert "产品版本号已由 release-prepare 自动同步为 `v2.0.0`" in announcement
    assert "当前产品版本号仍需" not in announcement
    assert validate_release_script.validate_release(release_dir, product_version.resolve()) == []


def test_miniapp_product_version_mismatch_blocks_publish(tmp_path: Path, monkeypatch) -> None:
    release_dir, product_version = write_release(tmp_path, version="v0.1.0")
    miniapp_dir = tmp_path / "src" / "miniapp" / "utils"
    miniapp_dir.mkdir(parents=True)
    miniapp_ts = miniapp_dir / "product-version.ts"
    miniapp_js = miniapp_dir / "product-version.js"
    miniapp_ts.write_text("export const PRODUCT_VERSION = 'v0.0.1';\n", encoding="utf-8")
    miniapp_js.write_text("const PRODUCT_VERSION = 'v0.1.0';\nmodule.exports = { PRODUCT_VERSION };\n", encoding="utf-8")
    monkeypatch.setattr(validate_release_script, "PRODUCT_VERSION_FILE", product_version.resolve())
    monkeypatch.setattr(validate_release_script, "MINIAPP_PRODUCT_VERSION_FILES", (miniapp_ts.resolve(), miniapp_js.resolve()))

    errors = validate_release_script.validate_release(release_dir, product_version, stage="publish")

    assert any(str(miniapp_ts) in error for error in errors)
    assert any("product version mismatch blocks publish" in error for error in errors)


def test_release_status_classifies_product_version_mismatch_as_prepare_gap(tmp_path: Path) -> None:
    release_dir, product_version = write_release(tmp_path, version="v0.1.0")
    product_version.write_text("export const PRODUCT_VERSION = 'v0.0.1';\n", encoding="utf-8")

    status = validate_release_script.release_status(release_dir, product_version)

    assert status["phase"] == "prepare_blocked"
    assert any(item["classification"] == "prepare_evidence_missing" for item in status["blocking_evidence"])
    assert any("/image-prepare v0.1.0" in item["message"] for item in status["blocking_evidence"])


def test_sensitive_announcement_fails(tmp_path: Path) -> None:
    release_dir, product_version = write_release(tmp_path, announcement="DATABASE_URL=mysql+pymysql://user:pass@example/db")
    errors = validate_release_script.validate_release(release_dir, product_version)
    assert any("sensitive pattern" in error for error in errors)


def test_release_status_reports_missing_default_upgrade_plan_command(tmp_path: Path, monkeypatch) -> None:
    release_dir, product_version = write_release(tmp_path, version="v1.0.0")
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    data["release_time"] = "2026-08-30 10:25:00"
    data["release_target"] = {
        "environment": "development",
        "deployment_scope": "development",
        "production_release_required": True,
        "rationale": "development release",
    }
    data["usage_docs"] = {
        "status": "skipped",
        "generation_decision": {"required": False, "confirmed_at": "2026-08-30 10:25:00", "confirmed_by": "operator", "rationale": "no docs"},
    }
    data["gates"]["usage_docs_preview"] = {"status": "na", "rationale": "no docs"}
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(validate_release_script, "ROOT", tmp_path)

    status = validate_release_script.release_status(release_dir, product_version)

    assert status["phase"] == "upgrade_pending"
    assert status["next_command"] == "/release-prepare v1.0.0"
    assert any(item["classification"] == "publish_evidence_missing" for item in status["blocking_evidence"])
    assert any(item["safe_remediation"] == "/release-prepare v1.0.0" for item in status["blocking_evidence"])
    assert status["default_upgrade_paths"][0]["command"] == "python scripts/validate-release-upgrade.py plan --from fresh --to v1.0.0"


def test_release_status_reports_declared_extra_upgrade_paths_as_prepare_owned(tmp_path: Path, monkeypatch) -> None:
    release_dir, product_version = write_release(tmp_path, version="v1.2.0")
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    data["release_time"] = "2026-08-31 09:10:00"
    data["usage_docs"] = {
        "status": "skipped",
        "generation_decision": {
            "required": False,
            "confirmed_at": "2026-08-31 09:10:00",
            "confirmed_by": "release-propose-default",
            "rationale": "default skip",
        },
    }
    data["gates"]["usage_docs_preview"] = {"status": "na", "rationale": "default skip"}
    data["upgrade_plans"] = {
        "sources": ["fresh", "previous-release"],
        "explicit_sources": ["v1.0.0"],
    }
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")
    (tmp_path / "releases" / "v1.1.0").mkdir()
    (tmp_path / "releases" / "v1.1.0" / "release.json").write_text(
        json.dumps({"version": "v1.1.0", "announcement": "announcement.mdx"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(validate_release_script, "ROOT", tmp_path)

    status = validate_release_script.release_status(release_dir, product_version)

    assert status["next_command"] == "/release-prepare v1.2.0"
    assert [item["from_version"] for item in status["default_upgrade_paths"]] == ["fresh", "v1.1.0", "v1.0.0"]
    assert any("v1.0.0-to-v1.2.0.json" in item["message"] for item in status["blocking_evidence"])


def test_release_status_has_no_followups_for_project_release(tmp_path: Path, monkeypatch) -> None:
    release_dir, product_version = write_release(tmp_path, version="v1.0.0")
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    data["release_time"] = "2026-08-30 10:25:00"
    data["release_target"] = {
        "environment": "development",
        "deployment_scope": "development",
        "production_release_required": True,
        "rationale": "development release",
    }
    data["usage_docs"] = {
        "status": "skipped",
        "generation_decision": {"required": False, "confirmed_at": "2026-08-30 10:25:00", "confirmed_by": "operator", "rationale": "no docs"},
    }
    data["gates"]["usage_docs_preview"] = {"status": "na", "rationale": "no docs"}
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")
    write_upgrade_plan(release_dir, from_version="fresh", to_version="v1.0.0", target="development")
    monkeypatch.setattr(validate_release_script, "ROOT", tmp_path)

    status = validate_release_script.release_status(release_dir, product_version)

    assert status["phase"] == "publish_ready"
    assert status["blocking_decisions"] == []
    assert status["blocking_evidence"] == []
    assert status["followups"] == []


def test_release_status_ignores_legacy_production_target_override(tmp_path: Path, monkeypatch) -> None:
    release_dir, product_version = write_release(tmp_path, version="v1.0.0")
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    data["release_time"] = "2026-08-30 10:25:00"
    data["release_target"] = {
        "environment": "development",
        "deployment_scope": "development",
        "production_release_required": True,
        "rationale": "development release",
    }
    data["usage_docs"] = {
        "status": "skipped",
        "generation_decision": {"required": False, "confirmed_at": "2026-08-30 10:25:00", "confirmed_by": "operator", "rationale": "no docs"},
    }
    data["gates"]["usage_docs_preview"] = {"status": "na", "rationale": "no docs"}
    data["known_issues"] = [
        {
            "classification": "production_only_pending",
            "target_environment": "production",
            "phase": "production_publish",
            "blocking_scope": "release-publish:production",
            "evidence_ref": "development archive follow-up",
        }
    ]
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")
    write_upgrade_plan(release_dir, from_version="fresh", to_version="v1.0.0", target="production")
    monkeypatch.setattr(validate_release_script, "ROOT", tmp_path)

    status = validate_release_script.release_status(release_dir, product_version, target_override="production")

    assert status["target"] == "project"
    assert status["phase"] == "publish_ready"
    assert status["blocking_evidence"] == []


def test_missing_gate_fails(tmp_path: Path) -> None:
    release_dir, product_version = write_release(tmp_path)
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    del data["gates"]["orval"]
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")
    errors = validate_release_script.validate_release(release_dir, product_version)
    assert "gate orval is required" in errors


def test_database_impact_requires_mysql_compatibility_evidence(tmp_path: Path) -> None:
    release_dir, product_version = write_release(tmp_path)
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    data["release_time"] = "2026-07-21 10:35:42"
    data["impact_scope"]["database"] = "schema change"
    data["gates"]["database_migration"] = {
        "status": "pass",
        "evidence": "schema.sql and docs updated",
    }
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")

    errors = validate_release_script.validate_release(release_dir, product_version)

    assert any("MySQL" in error or "schema.mysql.sql" in error for error in errors)
    assert any("schema drift" in error or "smoke" in error for error in errors)
    assert any("rollback" in error or "backup" in error for error in errors)


def test_database_impact_accepts_mysql_drift_and_rollback_evidence(tmp_path: Path) -> None:
    release_dir, product_version = write_release(tmp_path)
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    data["release_time"] = "2026-07-21 10:35:42"
    data["impact_scope"]["database"] = "schema change"
    data["gates"]["database_migration"] = {
        "status": "pass",
        "evidence": "schema.mysql.sql checked by scripts/check-mysql-schema-drift.py against target MySQL; rollback backup verified.",
    }
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")

    assert validate_release_script.validate_release(release_dir, product_version) == []


def test_image_required_false_requires_rationale(tmp_path: Path) -> None:
    release_dir, product_version = write_release(tmp_path)
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    data["image_required"] = False
    data["image_required_rationale"] = ""
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")

    errors = validate_release_script.validate_release(release_dir, product_version)

    assert any("image_required false requires image_required_rationale" in error for error in errors)


def test_image_input_candidates_exclude_release_evidence_narrative_docs() -> None:
    assert "docs/08-production-image-release.md" not in validate_image_build_script.INPUT_FILE_CANDIDATES
    assert "docs/04-database-design.md" not in validate_image_build_script.INPUT_FILE_CANDIDATES
    assert "docs/08-production-image-release.md" in validate_image_build_script.LEGACY_NARRATIVE_INPUT_FILES


def test_image_input_candidates_include_user_visible_product_versions() -> None:
    assert "src/shared/product-version.ts" in validate_image_build_script.INPUT_FILE_CANDIDATES
    assert "src/miniapp/utils/product-version.ts" in validate_image_build_script.INPUT_FILE_CANDIDATES
    assert "src/miniapp/utils/product-version.js" in validate_image_build_script.INPUT_FILE_CANDIDATES


def write_minimal_image_plan(release_dir: Path, release_data: dict) -> None:
    (release_dir / "image-build-plan.json").write_text(
        json.dumps(
            {
                "version": release_data["version"],
                "image_required": True,
                "image_tag": release_data["version"],
                "source_scope": {
                    "sprints": release_data.get("sprints", []),
                    "requirements": release_data.get("requirements", []),
                    "bugs": release_data.get("bugs", []),
                    "changes": release_data.get("changes", []),
                },
                "release_input": {
                    "source": "release.json stable fields",
                    "hash": validate_image_build_script.stable_release_input_hash(release_data),
                    "fields": validate_image_build_script.stable_release_input(release_data),
                },
                "build_env": {"default": {}, "example": {}},
                "input_files": [],
                "input_hashes": {},
                "database_impact": {"required": False},
                "required_commands": [],
                "auto_actions": [],
                "warnings": [],
                "blockers": [],
            }
        ),
        encoding="utf-8",
    )


def test_image_required_true_prepare_requires_plan_not_manifest(tmp_path: Path) -> None:
    release_dir, product_version = write_release(tmp_path)
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    data["release_time"] = "2026-07-29 16:00:00"
    data["image_required"] = True
    data["image_required_rationale"] = "docker impact"
    data["impact_scope"]["docker"] = "image delivery"
    data["gates"]["image_prepare"] = {"status": "pass", "evidence": "image-build-plan.json validated"}
    data["gates"]["image_build"] = {"status": "pass", "evidence": "image-manifest.json validated"}
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")

    errors = validate_release_script.validate_release(release_dir, product_version, stage="prepare")

    assert any("image build plan" in error for error in errors)
    assert not any("image manifest" in error for error in errors)

    write_minimal_image_plan(release_dir, data)

    assert validate_release_script.validate_release(release_dir, product_version, stage="prepare") == []
    publish_errors = validate_release_script.validate_release(release_dir, product_version, stage="publish")
    assert any("image manifest" in error for error in publish_errors)


def write_upgrade_plan(release_dir: Path, *, from_version: str, to_version: str, target: str = "project") -> None:
    payload = {
        "from_version": from_version,
        "to_version": to_version,
        "deployment_scope": "project",
        "support_level": "fresh-install-supported" if from_version == "fresh" else "adjacent-upgrade-supported",
        "source_confidence": "fresh" if from_version == "fresh" else "verified",
        "impact_summary": {},
        "required_checks": [],
        "steps": [],
        "rollback": {
            "previous_image": "previous",
            "target_image": to_version,
            "env_snapshot": "redacted",
            "database_backup": "recommended",
            "object_storage_backup": "recommended",
            "rollback_steps": [],
            "post_rollback_smoke": "pending",
        },
        "blockers": [],
        "warnings": [],
        "evidence": {},
    }
    path = release_dir / "upgrade-plans" / f"{from_version}-to-{to_version}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_project_publish_does_not_require_production_deployment(tmp_path: Path, monkeypatch) -> None:
    release_dir, product_version = write_release(tmp_path, version="v1.0.0")
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    data["release_time"] = "2026-08-30 10:00:00"
    data["release_target"] = {
        "environment": "development",
        "deployment_scope": "development",
        "production_release_required": True,
        "rationale": "dev release",
    }
    data["usage_docs"] = {
        "status": "skipped",
        "generation_decision": {"required": False, "confirmed_at": "2026-08-30 10:00:00", "confirmed_by": "operator", "rationale": "not needed"},
    }
    data["gates"]["usage_docs_preview"] = {"status": "na", "rationale": "not needed"}
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")
    write_upgrade_plan(release_dir, from_version="fresh", to_version="v1.0.0", target="development")
    monkeypatch.setattr(validate_release_script, "ROOT", tmp_path)

    assert validate_release_script.validate_release(release_dir, product_version, stage="publish") == []


def test_project_publish_ignores_legacy_production_target_override(tmp_path: Path, monkeypatch) -> None:
    release_dir, product_version = write_release(tmp_path, version="v1.0.0")
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    data["release_time"] = "2026-08-30 10:00:00"
    data["release_target"] = {
        "environment": "development",
        "deployment_scope": "development",
        "production_release_required": True,
        "rationale": "dev release",
    }
    data["usage_docs"] = {
        "status": "skipped",
        "generation_decision": {"required": False, "confirmed_at": "2026-08-30 10:00:00", "confirmed_by": "operator", "rationale": "not needed"},
    }
    data["gates"]["usage_docs_preview"] = {"status": "na", "rationale": "not needed"}
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")
    write_upgrade_plan(release_dir, from_version="fresh", to_version="v1.0.0", target="development")
    monkeypatch.setattr(validate_release_script, "ROOT", tmp_path)

    errors = validate_release_script.validate_release(release_dir, product_version, stage="publish", target_override="production")

    assert errors == []


def test_image_plan_detects_input_hash_drift(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    release_dir = root / "releases" / "v9.9.9"
    release_dir.mkdir(parents=True)
    monkeypatch.setattr(validate_image_build_script, "ROOT", root)
    monkeypatch.setattr(validate_image_build_script, "RELEASES_DIR", root / "releases")
    monkeypatch.setattr(validate_image_build_script, "DEFAULT_ENV_FILE", root / "scripts" / "build-images.env")
    monkeypatch.setattr(validate_image_build_script, "ENV_EXAMPLE_FILE", root / "scripts" / "build-images.env.example")
    (root / "scripts").mkdir()
    (root / "scripts" / "build-images.env.example").write_text("IMAGE_BUILD_TAG=v0.0.1\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (root / "scripts" / "build-images.env").write_text("IMAGE_BUILD_TAG=v9.9.9\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    tracked = root / "src" / "backend" / "Dockerfile"
    tracked.parent.mkdir(parents=True)
    tracked.write_text("FROM python:3.12-slim\n", encoding="utf-8")
    (release_dir / "announcement.mdx").write_text("# public", encoding="utf-8")
    (release_dir / "release.json").write_text(
        json.dumps(
            {
                "version": "v9.9.9",
                "announcement": "announcement.mdx",
                "image_required": True,
                "image_required_rationale": "docker impact",
                "sprints": [],
                "requirements": [],
                "bugs": [],
                "changes": [],
                "impact_scope": {"database": "none"},
            }
        ),
        encoding="utf-8",
    )

    validate_image_build_script.prepare_plan("v9.9.9", release_dir, root / "scripts" / "build-images.env")
    tracked.write_text("FROM python:3.12-alpine\n", encoding="utf-8")

    errors = validate_image_build_script.validate_plan("v9.9.9", release_dir)

    assert any("input hash drift" in error for error in errors)


def test_image_plan_tracks_deploy_inputs(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    release_dir = root / "releases" / "v9.9.9"
    release_dir.mkdir(parents=True)
    monkeypatch.setattr(validate_image_build_script, "ROOT", root)
    monkeypatch.setattr(validate_image_build_script, "RELEASES_DIR", root / "releases")
    monkeypatch.setattr(validate_image_build_script, "DEFAULT_ENV_FILE", root / "scripts" / "build-images.env")
    monkeypatch.setattr(validate_image_build_script, "ENV_EXAMPLE_FILE", root / "scripts" / "build-images.env.example")
    (root / "scripts").mkdir()
    (root / "scripts" / "build-images.env.example").write_text("IMAGE_BUILD_TAG=v0.0.1\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (root / "scripts" / "build-images.env").write_text("IMAGE_BUILD_TAG=v9.9.9\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (root / "deploy" / "local").mkdir(parents=True)
    (root / "deploy" / "scripts").mkdir(parents=True)
    (root / "deploy" / "local" / "compose.yml").write_text("services: {}\n", encoding="utf-8")
    (root / "deploy" / "local" / "sqlite-minio-managed.env.example").write_text("# env\nAPP_ENV=development\n", encoding="utf-8")
    (root / "deploy" / "scripts" / "up.sh").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    (release_dir / "announcement.mdx").write_text("# public", encoding="utf-8")
    (release_dir / "release.json").write_text(
        json.dumps(
            {
                "version": "v9.9.9",
                "announcement": "announcement.mdx",
                "image_required": True,
                "image_required_rationale": "docker impact",
                "sprints": [],
                "requirements": [],
                "bugs": [],
                "changes": [],
                "impact_scope": {"docker": "deploy input"},
            }
        ),
        encoding="utf-8",
    )

    plan = validate_image_build_script.prepare_plan("v9.9.9", release_dir, root / "scripts" / "build-images.env")

    assert "deploy/local/compose.yml" in plan["input_files"]
    assert "deploy/local/sqlite-minio-managed.env.example" in plan["input_files"]
    assert "deploy/scripts/up.sh" in plan["input_files"]


def test_image_plan_ignores_mutable_release_gate_evidence(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    release_dir = root / "releases" / "v9.9.9"
    release_dir.mkdir(parents=True)
    monkeypatch.setattr(validate_image_build_script, "ROOT", root)
    monkeypatch.setattr(validate_image_build_script, "RELEASES_DIR", root / "releases")
    monkeypatch.setattr(validate_image_build_script, "DEFAULT_ENV_FILE", root / "scripts" / "build-images.env")
    monkeypatch.setattr(validate_image_build_script, "ENV_EXAMPLE_FILE", root / "scripts" / "build-images.env.example")
    (root / "scripts").mkdir()
    (root / "scripts" / "build-images.env.example").write_text("IMAGE_BUILD_TAG=v0.0.1\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (root / "scripts" / "build-images.env").write_text("IMAGE_BUILD_TAG=v9.9.9\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (release_dir / "announcement.mdx").write_text("# public", encoding="utf-8")
    release_data = {
        "version": "v9.9.9",
        "announcement": "announcement.mdx",
        "image_required": True,
        "image_required_rationale": "docker impact",
        "sprints": ["sprint-999"],
        "requirements": [],
        "bugs": [],
        "changes": [],
        "impact_scope": {"database": "none", "docker": "image delivery"},
        "gates": {"image_prepare": {"status": "na", "rationale": "pending"}},
    }
    (release_dir / "release.json").write_text(json.dumps(release_data), encoding="utf-8")

    validate_image_build_script.prepare_plan("v9.9.9", release_dir, root / "scripts" / "build-images.env")
    release_data["gates"]["image_prepare"] = {"status": "pass", "evidence": "plan validated"}
    release_data["prepare_status"] = "blocked"
    (release_dir / "release.json").write_text(json.dumps(release_data), encoding="utf-8")

    assert validate_image_build_script.validate_plan("v9.9.9", release_dir) == []


def test_image_plan_ignores_announcement_copy_updates(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    release_dir = root / "releases" / "v9.9.9"
    release_dir.mkdir(parents=True)
    monkeypatch.setattr(validate_image_build_script, "ROOT", root)
    monkeypatch.setattr(validate_image_build_script, "RELEASES_DIR", root / "releases")
    monkeypatch.setattr(validate_image_build_script, "DEFAULT_ENV_FILE", root / "scripts" / "build-images.env")
    monkeypatch.setattr(validate_image_build_script, "ENV_EXAMPLE_FILE", root / "scripts" / "build-images.env.example")
    (root / "scripts").mkdir()
    (root / "scripts" / "build-images.env.example").write_text("IMAGE_BUILD_TAG=v0.0.1\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (root / "scripts" / "build-images.env").write_text("IMAGE_BUILD_TAG=v9.9.9\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    announcement = release_dir / "announcement.mdx"
    announcement.write_text("# public\n\nUsage docs pending.\n", encoding="utf-8")
    release_data = {
        "version": "v9.9.9",
        "announcement": "announcement.mdx",
        "image_required": True,
        "image_required_rationale": "docker impact",
        "sprints": ["sprint-999"],
        "requirements": [],
        "bugs": [],
        "changes": [],
        "impact_scope": {"database": "none", "docker": "image delivery"},
    }
    (release_dir / "release.json").write_text(json.dumps(release_data), encoding="utf-8")

    plan = validate_image_build_script.prepare_plan("v9.9.9", release_dir, root / "scripts" / "build-images.env")
    announcement.write_text("# public\n\nUsage docs skipped; image build completed.\n", encoding="utf-8")

    assert "releases/v9.9.9/announcement.mdx" not in plan["input_files"]
    assert validate_image_build_script.validate_plan("v9.9.9", release_dir) == []


def test_image_prepare_blocks_when_product_version_sources_are_not_aligned(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    release_dir = root / "releases" / "v9.9.9"
    release_dir.mkdir(parents=True)
    monkeypatch.setattr(validate_image_build_script, "ROOT", root)
    monkeypatch.setattr(validate_image_build_script, "RELEASES_DIR", root / "releases")
    monkeypatch.setattr(validate_image_build_script, "DEFAULT_ENV_FILE", root / "scripts" / "build-images.env")
    monkeypatch.setattr(validate_image_build_script, "ENV_EXAMPLE_FILE", root / "scripts" / "build-images.env.example")
    (root / "scripts").mkdir()
    (root / "scripts" / "build-images.env.example").write_text("IMAGE_BUILD_TAG=v0.0.1\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (root / "scripts" / "build-images.env").write_text("IMAGE_BUILD_TAG=v9.9.9\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (root / "src" / "shared").mkdir(parents=True)
    (root / "src" / "miniapp" / "utils").mkdir(parents=True)
    (root / "src" / "shared" / "product-version.ts").write_text("export const PRODUCT_VERSION = 'v9.9.8';\n", encoding="utf-8")
    (root / "src" / "miniapp" / "utils" / "product-version.ts").write_text("export const PRODUCT_VERSION = 'v9.9.8';\n", encoding="utf-8")
    (root / "src" / "miniapp" / "utils" / "product-version.js").write_text(
        "const PRODUCT_VERSION = 'v9.9.8';\nmodule.exports = { PRODUCT_VERSION };\n",
        encoding="utf-8",
    )
    (release_dir / "announcement.mdx").write_text("# public", encoding="utf-8")
    release_data = {
        "version": "v9.9.9",
        "announcement": "announcement.mdx",
        "image_required": True,
        "image_required_rationale": "docker impact",
        "sprints": ["sprint-999"],
        "requirements": [],
        "bugs": [],
        "changes": [],
        "impact_scope": {"database": "none", "docker": "image delivery"},
    }
    (release_dir / "release.json").write_text(json.dumps(release_data), encoding="utf-8")

    plan = validate_image_build_script.prepare_plan("v9.9.9", release_dir, root / "scripts" / "build-images.env")

    assert any(blocker["code"] == "product_version_mismatch" for blocker in plan["blockers"])
    assert any("/release-prepare v9.9.9" in blocker["message"] for blocker in plan["blockers"])


def test_image_plan_detects_stable_release_scope_drift(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    release_dir = root / "releases" / "v9.9.9"
    release_dir.mkdir(parents=True)
    monkeypatch.setattr(validate_image_build_script, "ROOT", root)
    monkeypatch.setattr(validate_image_build_script, "RELEASES_DIR", root / "releases")
    monkeypatch.setattr(validate_image_build_script, "DEFAULT_ENV_FILE", root / "scripts" / "build-images.env")
    monkeypatch.setattr(validate_image_build_script, "ENV_EXAMPLE_FILE", root / "scripts" / "build-images.env.example")
    (root / "scripts").mkdir()
    (root / "scripts" / "build-images.env.example").write_text("IMAGE_BUILD_TAG=v0.0.1\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (root / "scripts" / "build-images.env").write_text("IMAGE_BUILD_TAG=v9.9.9\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (release_dir / "announcement.mdx").write_text("# public", encoding="utf-8")
    release_data = {
        "version": "v9.9.9",
        "announcement": "announcement.mdx",
        "image_required": True,
        "image_required_rationale": "docker impact",
        "sprints": ["sprint-999"],
        "requirements": [],
        "bugs": [],
        "changes": [],
        "impact_scope": {"database": "none", "docker": "image delivery"},
    }
    (release_dir / "release.json").write_text(json.dumps(release_data), encoding="utf-8")

    validate_image_build_script.prepare_plan("v9.9.9", release_dir, root / "scripts" / "build-images.env")
    release_data["sprints"].append("sprint-1000")
    (release_dir / "release.json").write_text(json.dumps(release_data), encoding="utf-8")

    errors = validate_image_build_script.validate_plan("v9.9.9", release_dir)
    assert "release stable input drift: release.json" in errors


def add_skipped_usage_docs(release_dir: Path) -> None:
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    data["release_time"] = "2026-08-01 10:40:00"
    data["usage_docs"] = {
        "status": "skipped",
        "root": "usage-docs",
        "manifest": "usage-docs/manifest.json",
        "source_version": None,
        "manual_overrides_allowed": True,
        "overwrite_policy": "current-version-only-by-default",
        "generation_decision": {
            "required": False,
            "confirmed_at": "2026-08-01 10:40:00",
            "confirmed_by": "operator",
            "rationale": "No user-visible usage flow changed.",
        },
    }
    data["gates"]["usage_docs_preview"] = {
        "status": "na",
        "rationale": "2026-08-01 10:40:00: usage docs skipped by operator; no user-visible usage flow changed.",
    }
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")


def add_generated_usage_docs(release_dir: Path, *, sensitive: bool = False, authorized_override: bool = True) -> None:
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    version = data["version"]
    data["release_time"] = "2026-08-01 10:40:00"
    data["usage_docs"] = {
        "status": "generated",
        "root": "usage-docs",
        "manifest": "usage-docs/manifest.json",
        "source_version": None,
        "manual_overrides_allowed": True,
        "overwrite_policy": "current-version-only-by-default",
        "generation_decision": {
            "required": True,
            "confirmed_at": "2026-08-01 10:40:00",
            "confirmed_by": "operator",
            "rationale": "Release changes user-visible usage flow.",
        },
    }
    data["gates"]["usage_docs_preview"] = {
        "status": "pass",
        "evidence": "2026-08-01 10:41:00: scripts/validate-usage-docs.py passed.",
    }
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")

    usage_dir = release_dir / "usage-docs"
    site_asset_dir = release_dir.parents[1] / "mintlify" / "assets" / "screenshots"
    (usage_dir / "admin").mkdir(parents=True, exist_ok=True)
    site_asset_dir.mkdir(parents=True, exist_ok=True)
    (site_asset_dir / "overview.png").write_bytes(b"fake-png")
    (site_asset_dir / "admin.png").write_bytes(b"fake-png")
    (usage_dir / "overview.mdx").write_text(
        "# Overview\n\n![Overview](/assets/screenshots/overview.png)\n",
        encoding="utf-8",
    )
    (usage_dir / "admin" / "index.mdx").write_text(
        "# Admin\nDATABASE_URL=mysql://secret/db\n" if sensitive else "# Admin\n\n![Admin](/assets/screenshots/admin.png)\n",
        encoding="utf-8",
    )
    manual_overrides = []
    if not authorized_override:
        manual_overrides.append(
            {
                "change_type": "content_correction",
                "reason": "Fix old docs",
                "confirmed_by": "operator",
                "confirmed_at": "2026-08-01 10:40:00",
                "files": ["overview.mdx"],
                "summary": "Updated behavior",
                "authorized": False,
            }
        )
    (usage_dir / "manifest.json").write_text(
        json.dumps(
            {
                "version": version,
                "generated_at": "2026-08-01 10:41:00",
                "source_version": None,
                "source_release": {"path": "release.json", "sha256": "test"},
                "input_files": ["release.json"],
                "pages": ["overview.mdx", "admin/index.mdx"],
                "screenshots": [
                    {
                        "path": "/assets/screenshots/overview.png",
                        "site_asset": "mintlify/assets/screenshots/overview.png",
                        "content_hash": validate_usage_docs_script.path_sha256(site_asset_dir / "overview.png"),
                        "pages": ["overview.mdx"],
                        "covered_pages": ["overview.mdx"],
                        "caption": "Overview screenshot",
                        "source_type": "runtime_system",
                        "source": "test runtime system screenshot fixture",
                        "first_used_in": version,
                        "used_by_versions": [version],
                        "reuse_reason": "test fixture",
                    },
                    {
                        "path": "/assets/screenshots/admin.png",
                        "site_asset": "mintlify/assets/screenshots/admin.png",
                        "content_hash": validate_usage_docs_script.path_sha256(site_asset_dir / "admin.png"),
                        "pages": ["admin/index.mdx"],
                        "covered_pages": ["admin/index.mdx"],
                        "caption": "Admin screenshot",
                        "source_type": "runtime_system",
                        "source": "test runtime system screenshot fixture",
                        "first_used_in": version,
                        "used_by_versions": [version],
                        "reuse_reason": "test fixture",
                    },
                ],
                "coverage": {
                    "admin": {"status": "covered"},
                    "miniapp": {"status": "exempt", "rationale": "No miniapp changes"},
                    "release_impact_scope": {"status": "covered"},
                },
                "manual_overrides": manual_overrides,
                "automation_policy": {
                    "current_version": "current version can be regenerated after confirmation",
                    "old_versions": "content locked by default",
                    "content_corrections_require_authorization": True,
                },
            }
        ),
        encoding="utf-8",
    )
    (release_dir.parent / "mint.json").write_text(
        json.dumps(
            {
                "navigation": [
                    {
                        "group": "docs",
                        "pages": [
                            f"{version}/usage-docs/overview",
                            f"{version}/usage-docs/admin/index",
                        ],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def test_usage_docs_generated_flow_passes(tmp_path: Path) -> None:
    release_dir, product_version = write_release(tmp_path)
    add_generated_usage_docs(release_dir)

    assert validate_usage_docs_script.validate_release_usage_docs(release_dir / "release.json") == []
    assert validate_release_script.validate_release(release_dir, product_version) == []


def test_usage_docs_skipped_flow_passes_without_empty_directory(tmp_path: Path) -> None:
    release_dir, product_version = write_release(tmp_path)
    add_skipped_usage_docs(release_dir)

    assert validate_release_script.validate_release(release_dir, product_version) == []
    (release_dir / "usage-docs").mkdir()
    errors = validate_usage_docs_script.validate_release_usage_docs(release_dir / "release.json")
    assert any("must not create" in error for error in errors)


def test_usage_docs_pending_confirmation_blocks_release(tmp_path: Path) -> None:
    release_dir, product_version = write_release(tmp_path)
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    data["release_time"] = "2026-08-01 10:40:00"
    data["usage_docs"] = {"status": "pending_confirmation", "root": "usage-docs"}
    data["gates"]["usage_docs_preview"] = {"status": "na", "rationale": "pending user confirmation"}
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")

    errors = validate_release_script.validate_release(release_dir, product_version)

    assert any("pending_confirmation" in error for error in errors)
    assert any("/release-propose v0.1.0 --usage-docs" in error for error in errors)
    assert any("/release-propose v0.1.0 --no-usage-docs" in error for error in errors)


def test_usage_docs_requested_is_prepare_action_not_schema_error(tmp_path: Path) -> None:
    release_dir, _product_version = write_release(tmp_path)
    data = json.loads((release_dir / "release.json").read_text(encoding="utf-8"))
    data["release_time"] = "2026-08-31 09:10:00"
    data["usage_docs"] = {
        "status": "requested",
        "root": "usage-docs",
        "generation_decision": {
            "required": True,
            "confirmed_at": "2026-08-31 09:10:00",
            "confirmed_by": "operator",
            "rationale": "user requested usage docs",
        },
    }
    data["gates"]["usage_docs_preview"] = {"status": "na", "rationale": "pending prepare generation"}
    (release_dir / "release.json").write_text(json.dumps(data), encoding="utf-8")

    errors = validate_usage_docs_script.validate_release_usage_docs(release_dir / "release.json")

    assert any("status requested requires release preparation" in error for error in errors)
    assert not any("must be generated, skipped" in error for error in errors)


def test_generate_usage_docs_blocks_gate_until_real_screenshots(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    releases_dir = root / "releases"
    release_dir = releases_dir / "v9.9.9"
    template_dir = releases_dir / "templates" / "usage-docs"
    release_dir.mkdir(parents=True)
    template_dir.mkdir(parents=True)
    template_dir.joinpath("overview.mdx").write_text("# {{VERSION}}\n", encoding="utf-8")
    monkeypatch.setattr(generate_usage_docs_script, "RELEASES_DIR", releases_dir)
    monkeypatch.setattr(generate_usage_docs_script, "MINTLIFY_DIR", root / "mintlify")
    monkeypatch.setattr(generate_usage_docs_script, "TEMPLATE_DIR", template_dir)
    release_dir.joinpath("release.json").write_text(
        json.dumps(
            {
                "version": "v9.9.9",
                "gates": {"usage_docs_preview": {"status": "na", "rationale": "pending"}},
                "usage_docs": {
                    "status": "pending_confirmation",
                    "root": "usage-docs",
                    "manifest": "usage-docs/manifest.json",
                    "generation_decision": {
                        "required": True,
                        "confirmed_at": "2026-08-02 20:53:23",
                        "confirmed_by": "operator",
                        "rationale": "User-visible docs required.",
                    },
                },
            }
        ),
        encoding="utf-8",
    )

    generate_usage_docs_script.generate_usage_docs("v9.9.9")

    release_data = json.loads(release_dir.joinpath("release.json").read_text(encoding="utf-8"))
    manifest = json.loads(release_dir.joinpath("usage-docs/manifest.json").read_text(encoding="utf-8"))
    assert release_data["usage_docs"]["status"] == "generated"
    assert release_data["gates"]["usage_docs_preview"]["status"] == "blocked"
    assert "real system screenshots" in release_data["gates"]["usage_docs_preview"]["evidence"]
    assert manifest["screenshots"] == []
    assert (root / "mintlify" / "docs" / "v9.9.9" / "overview.mdx").exists()
    docs = json.loads((root / "mintlify" / "docs.json").read_text(encoding="utf-8"))
    assert "docs/v9.9.9/overview" in json.dumps(docs)


def test_previous_usage_docs_version_uses_semver_and_requires_manifest(tmp_path: Path, monkeypatch) -> None:
    releases_dir = tmp_path / "releases"
    for version in ("v0.9.0", "v0.10.0", "v0.11.0", "v0.12.0"):
        (releases_dir / version / "usage-docs").mkdir(parents=True)
    (releases_dir / "v0.9.0" / "usage-docs" / "manifest.json").write_text("{}", encoding="utf-8")
    (releases_dir / "v0.10.0" / "usage-docs" / "manifest.json").write_text("{}", encoding="utf-8")
    (releases_dir / "v0.11.0" / "usage-docs" / "manifest.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(generate_usage_docs_script, "RELEASES_DIR", releases_dir)

    assert generate_usage_docs_script.previous_usage_docs_version("v0.11.0") == "v0.10.0"
    assert generate_usage_docs_script.previous_usage_docs_version("v0.12.0") == "v0.11.0"
    assert generate_usage_docs_script.previous_usage_docs_version("v0.10.1") == "v0.10.0"
    assert generate_usage_docs_script.previous_usage_docs_version("v0.0.1") is None

    (releases_dir / "v0.11.0" / "usage-docs" / "manifest.json").unlink()
    assert generate_usage_docs_script.previous_usage_docs_version("v0.12.0") == "v0.10.0"


def test_generate_usage_docs_inherits_semver_previous_manifest(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    releases_dir = root / "releases"
    template_dir = releases_dir / "templates" / "usage-docs"
    template_dir.mkdir(parents=True)
    template_dir.joinpath("overview.mdx").write_text("# Template {{VERSION}}\n", encoding="utf-8")

    previous = releases_dir / "v0.10.0" / "usage-docs"
    previous.mkdir(parents=True)
    previous.joinpath("overview.mdx").write_text("# v0.10.0 docs\n", encoding="utf-8")
    previous.joinpath("manifest.json").write_text(
        json.dumps(
            {
                "version": "v0.10.0",
                "generated_at": "2026-08-03 10:00:00",
                "source_release": {"path": "release.json", "sha256": "previous"},
                "input_files": ["release.json"],
                "pages": ["overview.mdx"],
                "screenshots": [],
                "coverage": {"admin": {"status": "covered"}},
                "manual_overrides": [],
                "automation_policy": {"content_corrections_require_authorization": True},
            }
        ),
        encoding="utf-8",
    )
    (releases_dir / "v0.11.0" / "usage-docs").mkdir(parents=True)

    target = releases_dir / "v0.12.0"
    target.mkdir(parents=True)
    target.joinpath("release.json").write_text(
        json.dumps(
            {
                "version": "v0.12.0",
                "gates": {"usage_docs_preview": {"status": "na", "rationale": "pending"}},
                "usage_docs": {
                    "status": "pending_confirmation",
                    "root": "usage-docs",
                    "manifest": "usage-docs/manifest.json",
                    "generation_decision": {
                        "required": True,
                        "confirmed_at": "2026-08-04 08:00:00",
                        "confirmed_by": "operator",
                        "rationale": "User-visible docs required.",
                    },
                },
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(generate_usage_docs_script, "RELEASES_DIR", releases_dir)
    monkeypatch.setattr(generate_usage_docs_script, "MINTLIFY_DIR", root / "mintlify")
    monkeypatch.setattr(generate_usage_docs_script, "TEMPLATE_DIR", template_dir)

    generate_usage_docs_script.generate_usage_docs("v0.12.0")

    release_data = json.loads(target.joinpath("release.json").read_text(encoding="utf-8"))
    manifest = json.loads(target.joinpath("usage-docs/manifest.json").read_text(encoding="utf-8"))
    assert release_data["usage_docs"]["source_version"] == "v0.10.0"
    assert manifest["source_version"] == "v0.10.0"
    assert manifest["pages"] == ["overview.mdx"]
    assert "v0.12.0 docs" in target.joinpath("usage-docs/overview.mdx").read_text(encoding="utf-8")


def test_project_existing_usage_docs_migrates_historical_docs(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    releases_dir = root / "releases"
    release_dir = releases_dir / "v9.9.9"
    release_dir.mkdir(parents=True)
    (releases_dir / "mint.json").write_text(
        json.dumps({"navigation": [{"group": "docs", "pages": ["v9.9.9/usage-docs/overview"]}]}),
        encoding="utf-8",
    )
    usage_dir = release_dir / "usage-docs"
    (usage_dir / "assets" / "screenshots").mkdir(parents=True)
    (usage_dir / "assets" / "screenshots" / "overview.png").write_bytes(b"historical-png")
    (usage_dir / "overview.mdx").write_text("# Historical\n\n![Overview](/assets/screenshots/overview.png)\n", encoding="utf-8")
    (release_dir / "announcement.mdx").write_text("# Announcement", encoding="utf-8")
    (release_dir / "release.json").write_text(
        json.dumps(
            {
                "version": "v9.9.9",
                "announcement": "announcement.mdx",
                "usage_docs": {"status": "generated", "root": "usage-docs", "manifest": "usage-docs/manifest.json"},
                "gates": {"usage_docs_preview": {"status": "pass", "evidence": "existing docs validated"}},
            }
        ),
        encoding="utf-8",
    )
    (usage_dir / "manifest.json").write_text(
        json.dumps(
            {
                "version": "v9.9.9",
                "generated_at": "2026-08-03 19:10:00",
                "source_release": {"path": "release.json", "sha256": "test"},
                "input_files": ["release.json"],
                "pages": ["overview.mdx"],
                "screenshots": [
                    {
                        "path": "assets/screenshots/overview.png",
                        "pages": ["overview.mdx"],
                        "caption": "Overview",
                        "source_type": "runtime_system",
                        "source": "historical runtime screenshot",
                    }
                ],
                "coverage": {
                    "admin": {"status": "covered"},
                    "miniapp": {"status": "exempt", "rationale": "No miniapp changes"},
                    "release_impact_scope": {"status": "covered"},
                },
                "manual_overrides": [],
                "automation_policy": {"content_corrections_require_authorization": True},
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(generate_usage_docs_script, "RELEASES_DIR", releases_dir)
    monkeypatch.setattr(generate_usage_docs_script, "MINTLIFY_DIR", root / "mintlify")
    monkeypatch.setattr(validate_usage_docs_script, "ROOT", root)
    monkeypatch.setattr(validate_usage_docs_script, "MINTLIFY_DIR", root / "mintlify")

    target = generate_usage_docs_script.project_existing_usage_docs("v9.9.9")

    manifest = json.loads((usage_dir / "manifest.json").read_text(encoding="utf-8"))
    assert target == root / "mintlify" / "docs" / "v9.9.9"
    assert manifest["site_projection"]["status"] == "synced"
    assert (root / "mintlify" / "docs" / "latest" / "overview.mdx").exists()
    assert (root / "mintlify" / "releases" / "v9.9.9" / "announcement.mdx").exists()
    assert manifest["screenshots"][0]["site_asset"].startswith("mintlify/assets/screenshots/")
    assert validate_usage_docs_script.validate_release_usage_docs(release_dir / "release.json") == []


def test_usage_docs_generated_requires_manifest_navigation_and_public_safety(tmp_path: Path) -> None:
    release_dir, _product_version = write_release(tmp_path)
    add_generated_usage_docs(release_dir)
    (release_dir / "usage-docs" / "manifest.json").unlink()

    errors = validate_usage_docs_script.validate_release_usage_docs(release_dir / "release.json")
    assert any("missing file" in error for error in errors)

    add_generated_usage_docs(release_dir)
    (release_dir.parent / "mint.json").write_text('{"navigation":[]}', encoding="utf-8")
    errors = validate_usage_docs_script.validate_release_usage_docs(release_dir / "release.json")
    assert any("navigation missing" in error for error in errors)

    add_generated_usage_docs(release_dir, sensitive=True)
    errors = validate_usage_docs_script.validate_release_usage_docs(release_dir / "release.json")
    assert any("sensitive pattern" in error for error in errors)

    add_generated_usage_docs(release_dir, authorized_override=False)
    errors = validate_usage_docs_script.validate_release_usage_docs(release_dir / "release.json")
    assert any("content_correction requires authorized=true" in error for error in errors)

    add_generated_usage_docs(release_dir)
    manifest_path = release_dir / "usage-docs" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["screenshots"] = []
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    errors = validate_usage_docs_script.validate_release_usage_docs(release_dir / "release.json")
    assert any("manifest.screenshots" in error for error in errors)

    add_generated_usage_docs(release_dir)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["screenshots"][0]["source"] = "REQ-0001 prototype screenshot"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    errors = validate_usage_docs_script.validate_release_usage_docs(release_dir / "release.json")
    assert any("real system screenshot" in error for error in errors)


def test_usage_docs_site_projection_checks_mintlify_targets(tmp_path: Path, monkeypatch) -> None:
    release_dir, _product_version = write_release(tmp_path)
    add_generated_usage_docs(release_dir)
    root = tmp_path
    version = release_dir.name
    usage_dir = release_dir / "usage-docs"
    site_root = root / "mintlify"
    monkeypatch.setattr(validate_usage_docs_script, "ROOT", root)
    monkeypatch.setattr(validate_usage_docs_script, "MINTLIFY_DIR", site_root)
    monkeypatch.setattr(validate_release_script, "MINTLIFY_DIR", site_root)

    for rel in ("docs/v0.1.0/admin", "docs/latest/admin", "releases/v0.1.0", "assets/screenshots"):
        (site_root / rel).mkdir(parents=True, exist_ok=True)
    for page in ("overview.mdx", "admin/index.mdx"):
        source = usage_dir / page
        for target_root in (site_root / "docs" / version, site_root / "docs" / "latest"):
            target = target_root / page
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    (site_root / "releases" / version / "announcement.mdx").write_text("# Public", encoding="utf-8")
    (site_root / "assets" / "screenshots" / "sha256-admin.png").write_bytes(b"fake-png")
    (site_root / "docs.json").write_text(
        json.dumps(
            {
                "theme": "mint",
                "navigation": [
                    {
                        "group": "docs",
                        "pages": [
                            "docs/latest/overview",
                            f"docs/{version}/overview",
                            f"docs/{version}/admin/index",
                            f"releases/{version}/announcement",
                        ],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (site_root / "site-manifest.json").write_text('{"versions":["v0.1.0"]}', encoding="utf-8")

    manifest_path = usage_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    hashes = {
        page: validate_usage_docs_script.path_sha256(site_root / "docs" / version / page)
        for page in manifest["pages"]
    }
    manifest["site_projection"] = {
        "status": "synced",
        "source_release": f"releases/{version}",
        "source_manifest": f"releases/{version}/usage-docs/manifest.json",
        "target_site_root": f"mintlify/docs/{version}",
        "latest_target": "mintlify/docs/latest",
        "synced_at": "2026-08-03 19:10:00",
        "mode": "copy",
        "content_hashes": hashes,
        "manual_overrides": [],
    }
    for screenshot in manifest["screenshots"]:
        source_asset = root / str(screenshot["site_asset"])
        screenshot["content_hash"] = validate_usage_docs_script.path_sha256(source_asset)
        screenshot["first_used_in"] = version
        screenshot["used_by_versions"] = [version]
        screenshot["covered_pages"] = screenshot["pages"]
        screenshot["reuse_reason"] = "test fixture"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    assert validate_usage_docs_script.validate_release_usage_docs(release_dir / "release.json") == []

    (site_root / "docs" / version / "overview.mdx").write_text("# drift", encoding="utf-8")
    errors = validate_usage_docs_script.validate_release_usage_docs(release_dir / "release.json")
    assert any("content_hashes drift" in error for error in errors)


def test_image_prepare_auto_normalizes_tag_mismatch(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    release_dir = root / "releases" / "v9.9.9"
    release_dir.mkdir(parents=True)
    monkeypatch.setattr(validate_image_build_script, "ROOT", root)
    monkeypatch.setattr(validate_image_build_script, "RELEASES_DIR", root / "releases")
    monkeypatch.setattr(validate_image_build_script, "DEFAULT_ENV_FILE", root / "scripts" / "build-images.env")
    monkeypatch.setattr(validate_image_build_script, "ENV_EXAMPLE_FILE", root / "scripts" / "build-images.env.example")
    (root / "scripts").mkdir()
    (root / "scripts" / "build-images.env.example").write_text("IMAGE_BUILD_TAG=v0.0.1\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (root / "scripts" / "build-images.env").write_text("IMAGE_BUILD_TAG=v1.0.0\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (release_dir / "announcement.mdx").write_text("# public", encoding="utf-8")
    (release_dir / "release.json").write_text(
        json.dumps(
            {
                "version": "v9.9.9",
                "announcement": "announcement.mdx",
                "image_required": True,
                "image_required_rationale": "docker impact",
                "sprints": [],
                "requirements": [],
                "bugs": [],
                "changes": [],
                "impact_scope": {"database": "none"},
            }
        ),
        encoding="utf-8",
    )

    plan = validate_image_build_script.prepare_plan("v9.9.9", release_dir, root / "scripts" / "build-images.env")

    env_text = (root / "scripts" / "build-images.env").read_text(encoding="utf-8")
    assert "IMAGE_BUILD_TAG=v9.9.9" in env_text
    assert plan["image_tag"] == "v9.9.9"
    assert not any(blocker["code"] == "image_tag_mismatch" for blocker in plan["blockers"])
    assert any(action["code"] == "image_tag_normalized" for action in plan["auto_actions"])


def test_image_prepare_records_compose_default_tag_as_warning(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    release_dir = root / "releases" / "v9.9.9"
    release_dir.mkdir(parents=True)
    monkeypatch.setattr(validate_image_build_script, "ROOT", root)
    monkeypatch.setattr(validate_image_build_script, "RELEASES_DIR", root / "releases")
    monkeypatch.setattr(validate_image_build_script, "DEFAULT_ENV_FILE", root / "scripts" / "build-images.env")
    monkeypatch.setattr(validate_image_build_script, "ENV_EXAMPLE_FILE", root / "scripts" / "build-images.env.example")
    (root / "scripts").mkdir()
    (root / "scripts" / "build-images.env.example").write_text("IMAGE_BUILD_TAG=v0.0.1\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (root / "scripts" / "build-images.env").write_text("IMAGE_BUILD_TAG=v9.9.9\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (root / "docker-compose.prod.yml").write_text("image: tilesfst-web:${TILESFST_IMAGE_TAG:-v0.0.4}\n", encoding="utf-8")
    (release_dir / "announcement.mdx").write_text("# public", encoding="utf-8")
    (release_dir / "release.json").write_text(
        json.dumps(
            {
                "version": "v9.9.9",
                "announcement": "announcement.mdx",
                "image_required": True,
                "image_required_rationale": "docker impact",
                "sprints": [],
                "requirements": [],
                "bugs": [],
                "changes": [],
                "impact_scope": {"database": "none", "docker": "image delivery"},
            }
        ),
        encoding="utf-8",
    )

    plan = validate_image_build_script.prepare_plan("v9.9.9", release_dir, root / "scripts" / "build-images.env")

    assert not any(blocker["code"] == "compose_default_tag_mismatch" for blocker in plan["blockers"])
    assert any(warning["code"] == "compose_default_tag_fallback_mismatch" for warning in plan["warnings"])


def test_image_paths_use_repo_relative_external_release_dir(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    monkeypatch.setattr(validate_image_build_script, "ROOT", root)

    external_tar = root.parent / "releases" / "v9.9.9" / "images" / "tilesfst-v9.9.9-linux-amd64.tar.gz"

    assert validate_image_build_script.rel_path(external_tar) == "../releases/v9.9.9/images/tilesfst-v9.9.9-linux-amd64.tar.gz"


def test_image_manifest_validation_passes_with_matching_hashes(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    release_dir = root / "releases" / "v9.9.9"
    release_dir.mkdir(parents=True)
    monkeypatch.setattr(validate_image_build_script, "ROOT", root)
    monkeypatch.setattr(validate_image_build_script, "RELEASES_DIR", root / "releases")
    monkeypatch.setattr(validate_image_build_script, "DEFAULT_ENV_FILE", root / "scripts" / "build-images.env")
    monkeypatch.setattr(validate_image_build_script, "ENV_EXAMPLE_FILE", root / "scripts" / "build-images.env.example")
    (root / "scripts").mkdir()
    (root / "scripts" / "build-images.env.example").write_text("IMAGE_BUILD_TAG=v0.0.1\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (root / "scripts" / "build-images.env").write_text("IMAGE_BUILD_TAG=v9.9.9\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (release_dir / "announcement.mdx").write_text("# public", encoding="utf-8")
    (release_dir / "release.json").write_text(
        json.dumps(
            {
                "version": "v9.9.9",
                "announcement": "announcement.mdx",
                "image_required": True,
                "image_required_rationale": "docker impact",
                "sprints": [],
                "requirements": [],
                "bugs": [],
                "changes": [],
                "impact_scope": {"database": "none"},
            }
        ),
        encoding="utf-8",
    )
    plan = validate_image_build_script.prepare_plan("v9.9.9", release_dir, root / "scripts" / "build-images.env")
    plan_path = release_dir / "image-build-plan.json"
    tar_path = root / "releases" / "v9.9.9" / "images" / "tilesfst-v9.9.9-linux-amd64.tar.gz"
    tar_path.parent.mkdir(parents=True)
    tar_path.write_bytes(b"release image")
    tar_sha = validate_image_build_script.file_sha256(tar_path)
    Path(f"{tar_path}.sha256").write_text(f"{tar_sha}  {tar_path.name}\n", encoding="utf-8")
    (release_dir / "image-manifest.json").write_text(
        json.dumps(
            {
                "version": "v9.9.9",
                "image_tag": "v9.9.9",
                "built_at": "2026-07-29 16:00:00",
                "platform": "linux/amd64",
                "backend_image": {"ref": "tilesfst-backend:v9.9.9"},
                "web_image": {"ref": "tilesfst-web:v9.9.9"},
                "tarball": {
                    "path": "releases/v9.9.9/images/tilesfst-v9.9.9-linux-amd64.tar.gz",
                    "sha256": tar_sha,
                    "exists": True,
                },
                "input_hashes": plan["input_hashes"],
                "validation": {"platform": "pass", "backend_dependencies": "pass", "web_nginx": "pass"},
                "source_plan": {"path": "releases/v9.9.9/image-build-plan.json", "sha256": validate_image_build_script.file_sha256(plan_path)},
            }
        ),
        encoding="utf-8",
    )

    assert validate_image_build_script.validate_manifest("v9.9.9", release_dir) == []


def test_image_manifest_validation_detects_sidecar_checksum_mismatch(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    release_dir = root / "releases" / "v9.9.9"
    release_dir.mkdir(parents=True)
    monkeypatch.setattr(validate_image_build_script, "ROOT", root)
    monkeypatch.setattr(validate_image_build_script, "RELEASES_DIR", root / "releases")
    monkeypatch.setattr(validate_image_build_script, "DEFAULT_ENV_FILE", root / "scripts" / "build-images.env")
    monkeypatch.setattr(validate_image_build_script, "ENV_EXAMPLE_FILE", root / "scripts" / "build-images.env.example")
    (root / "scripts").mkdir()
    (root / "scripts" / "build-images.env.example").write_text("IMAGE_BUILD_TAG=v0.0.1\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (root / "scripts" / "build-images.env").write_text("IMAGE_BUILD_TAG=v9.9.9\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (release_dir / "announcement.mdx").write_text("# public", encoding="utf-8")
    release_data = {
        "version": "v9.9.9",
        "announcement": "announcement.mdx",
        "image_required": True,
        "image_required_rationale": "docker impact",
        "sprints": [],
        "requirements": [],
        "bugs": [],
        "changes": [],
        "impact_scope": {"database": "none"},
    }
    (release_dir / "release.json").write_text(json.dumps(release_data), encoding="utf-8")
    plan = validate_image_build_script.prepare_plan("v9.9.9", release_dir, root / "scripts" / "build-images.env")
    plan_path = release_dir / "image-build-plan.json"
    tar_path = root / "releases" / "v9.9.9" / "images" / "tilesfst-v9.9.9-linux-amd64.tar.gz"
    tar_path.parent.mkdir(parents=True)
    tar_path.write_bytes(b"release image")
    tar_sha = validate_image_build_script.file_sha256(tar_path)
    Path(f"{tar_path}.sha256").write_text(f"{'0' * 64}  {tar_path.name}\n", encoding="utf-8")
    (release_dir / "image-manifest.json").write_text(
        json.dumps(
            {
                "version": "v9.9.9",
                "image_tag": "v9.9.9",
                "built_at": "2026-07-29 16:00:00",
                "platform": "linux/amd64",
                "backend_image": {"ref": "tilesfst-backend:v9.9.9"},
                "web_image": {"ref": "tilesfst-web:v9.9.9"},
                "tarball": {
                    "path": "releases/v9.9.9/images/tilesfst-v9.9.9-linux-amd64.tar.gz",
                    "sha256": tar_sha,
                    "exists": True,
                },
                "input_hashes": plan["input_hashes"],
                "validation": {"platform": "pass", "backend_dependencies": "pass", "web_nginx": "pass"},
                "source_plan": {"path": "releases/v9.9.9/image-build-plan.json", "sha256": validate_image_build_script.file_sha256(plan_path)},
            }
        ),
        encoding="utf-8",
    )

    errors = validate_image_build_script.validate_manifest("v9.9.9", release_dir)

    assert any("tarball sidecar sha256 mismatch" in error for error in errors)


def test_image_manifest_validation_detects_tarball_checksum_mismatch(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    release_dir = root / "releases" / "v9.9.9"
    release_dir.mkdir(parents=True)
    monkeypatch.setattr(validate_image_build_script, "ROOT", root)
    monkeypatch.setattr(validate_image_build_script, "RELEASES_DIR", root / "releases")
    monkeypatch.setattr(validate_image_build_script, "DEFAULT_ENV_FILE", root / "scripts" / "build-images.env")
    monkeypatch.setattr(validate_image_build_script, "ENV_EXAMPLE_FILE", root / "scripts" / "build-images.env.example")
    (root / "scripts").mkdir()
    (root / "scripts" / "build-images.env.example").write_text("IMAGE_BUILD_TAG=v0.0.1\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (root / "scripts" / "build-images.env").write_text("IMAGE_BUILD_TAG=v9.9.9\nIMAGE_BUILD_PLATFORM=linux/amd64\n", encoding="utf-8")
    (release_dir / "announcement.mdx").write_text("# public", encoding="utf-8")
    release_data = {
        "version": "v9.9.9",
        "announcement": "announcement.mdx",
        "image_required": True,
        "image_required_rationale": "docker impact",
        "sprints": [],
        "requirements": [],
        "bugs": [],
        "changes": [],
        "impact_scope": {"database": "none"},
    }
    (release_dir / "release.json").write_text(json.dumps(release_data), encoding="utf-8")
    plan = validate_image_build_script.prepare_plan("v9.9.9", release_dir, root / "scripts" / "build-images.env")
    plan_path = release_dir / "image-build-plan.json"
    tar_path = root / "releases" / "v9.9.9" / "images" / "tilesfst-v9.9.9-linux-amd64.tar.gz"
    tar_path.parent.mkdir(parents=True)
    tar_path.write_bytes(b"release image")
    original_sha = validate_image_build_script.file_sha256(tar_path)
    Path(f"{tar_path}.sha256").write_text(f"{original_sha}  {tar_path.name}\n", encoding="utf-8")
    tar_path.write_bytes(b"changed release image")
    (release_dir / "image-manifest.json").write_text(
        json.dumps(
            {
                "version": "v9.9.9",
                "image_tag": "v9.9.9",
                "built_at": "2026-07-29 16:00:00",
                "platform": "linux/amd64",
                "backend_image": {"ref": "tilesfst-backend:v9.9.9"},
                "web_image": {"ref": "tilesfst-web:v9.9.9"},
                "tarball": {
                    "path": "releases/v9.9.9/images/tilesfst-v9.9.9-linux-amd64.tar.gz",
                    "sha256": original_sha,
                    "exists": True,
                },
                "input_hashes": plan["input_hashes"],
                "validation": {"platform": "pass", "backend_dependencies": "pass", "web_nginx": "pass"},
                "source_plan": {"path": "releases/v9.9.9/image-build-plan.json", "sha256": validate_image_build_script.file_sha256(plan_path)},
            }
        ),
        encoding="utf-8",
    )

    errors = validate_image_build_script.validate_manifest("v9.9.9", release_dir)

    assert any("tarball sha256 mismatch" in error for error in errors)
