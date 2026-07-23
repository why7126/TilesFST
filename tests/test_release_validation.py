from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-release.py"
SPEC = importlib.util.spec_from_file_location("validate_release_script", SCRIPT)
assert SPEC and SPEC.loader
validate_release_script = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_release_script)


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


def test_version_mismatch_requires_rationale(tmp_path: Path) -> None:
    release_dir, product_version = write_release(tmp_path, version="v0.1.0")
    product_version.write_text("export const PRODUCT_VERSION = 'v0.0.1';\n", encoding="utf-8")
    errors = validate_release_script.validate_release(release_dir, product_version)
    assert any("version_change_rationale" in error for error in errors)


def test_sensitive_announcement_fails(tmp_path: Path) -> None:
    release_dir, product_version = write_release(tmp_path, announcement="DATABASE_URL=mysql+pymysql://user:pass@example/db")
    errors = validate_release_script.validate_release(release_dir, product_version)
    assert any("sensitive pattern" in error for error in errors)


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
