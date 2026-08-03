from __future__ import annotations

import sys
import importlib.util
from pathlib import Path
from types import ModuleType

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def load_validator() -> ModuleType:
    module_path = ROOT / "scripts" / "validate-directory-structure.py"
    spec = importlib.util.spec_from_file_location("validate_directory_structure", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_validator()


def write_required_paths(root: Path) -> None:
    for item in validator.REQUIRED_PATHS:
        path = root / item
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")


def write_allowed_root_dirs(root: Path) -> None:
    for item in validator.ALLOWED_ROOT_DIRS:
        (root / item).mkdir(parents=True, exist_ok=True)


def test_validate_rejects_legacy_openspec_change_archive_root(tmp_path: Path) -> None:
    write_required_paths(tmp_path)
    write_allowed_root_dirs(tmp_path)
    (tmp_path / "openspec" / "changes" / "archive").mkdir(parents=True)

    errors = validator.validate(tmp_path)

    assert any("openspec/changes/archive" in error for error in errors)


def test_validate_rejects_empty_staged_issue_dir(tmp_path: Path) -> None:
    write_required_paths(tmp_path)
    write_allowed_root_dirs(tmp_path)
    (tmp_path / "issues" / "bugs" / "plan" / "BUG-0001-empty").mkdir(parents=True)

    errors = validator.validate(tmp_path)

    assert any("Issue 目录为空" in error and "BUG-0001-empty" in error for error in errors)
    assert any("缺少 trace.md" in error and "BUG-0001-empty" in error for error in errors)


def test_validate_rejects_duplicate_issue_short_id_across_stages(tmp_path: Path) -> None:
    write_required_paths(tmp_path)
    write_allowed_root_dirs(tmp_path)
    first = tmp_path / "issues" / "bugs" / "plan" / "BUG-0001-first"
    second = tmp_path / "issues" / "bugs" / "archive" / "BUG-0001-second"
    first.mkdir(parents=True)
    second.mkdir(parents=True)
    (first / "trace.md").write_text("bug_id: BUG-0001-first\n", encoding="utf-8")
    (second / "trace.md").write_text("bug_id: BUG-0001-second\n", encoding="utf-8")

    errors = validator.validate(tmp_path)

    assert any("Issue 短编号重复: BUG-0001" in error for error in errors)


def test_validate_allows_deploy_matrix_structure(tmp_path: Path) -> None:
    write_required_paths(tmp_path)
    write_allowed_root_dirs(tmp_path)
    (tmp_path / "deploy" / "README.md").write_text("deploy\n", encoding="utf-8")
    (tmp_path / "deploy" / "local").mkdir(parents=True)
    (tmp_path / "deploy" / "prod").mkdir(parents=True)
    (tmp_path / "deploy" / "scripts").mkdir(parents=True)
    (tmp_path / "deploy" / "local" / "compose.yml").write_text("services: {}\n", encoding="utf-8")
    (tmp_path / "deploy" / "local" / "sqlite-minio-managed.env.example").write_text(
        "# example\nAPP_ENV=development\n",
        encoding="utf-8",
    )

    errors = validator.validate(tmp_path)

    assert not any("deploy" in error for error in errors)


def test_validate_rejects_deploy_runtime_and_secret_files(tmp_path: Path) -> None:
    write_required_paths(tmp_path)
    write_allowed_root_dirs(tmp_path)
    (tmp_path / "deploy" / "local").mkdir(parents=True)
    (tmp_path / "deploy" / "local" / "mysql-tencent-cos.env").write_text("APP_SECRET_KEY=secret\n", encoding="utf-8")
    (tmp_path / "deploy" / "local" / "data").mkdir()
    (tmp_path / "deploy" / "local" / "tilesfst.sqlite3").write_text("", encoding="utf-8")
    (tmp_path / "deploy" / "prod" / "images").mkdir(parents=True)
    (tmp_path / "deploy" / "prod" / "images" / "bundle.tar.gz").write_text("", encoding="utf-8")

    errors = validator.validate(tmp_path)

    assert any("真实 env" in error and "mysql-tencent-cos.env" in error for error in errors)
    assert any("禁止运行时目录" in error and "deploy/local/data" in error for error in errors)
    assert any("运行时或镜像文件" in error and "tilesfst.sqlite3" in error for error in errors)
    assert any("运行时或镜像文件" in error and "bundle.tar.gz" in error for error in errors)


def test_validate_allows_governed_mintlify_root(tmp_path: Path) -> None:
    write_required_paths(tmp_path)
    write_allowed_root_dirs(tmp_path)
    (tmp_path / "mintlify" / "assets" / "screenshots").mkdir(parents=True)
    (tmp_path / "mintlify" / "docs").mkdir()
    (tmp_path / "mintlify" / "releases").mkdir()
    (tmp_path / "mintlify" / "README.md").write_text("---\ncreated_at: 2026-08-03 19:10:00\nupdated_at: 2026-08-03 19:10:00\n---\n", encoding="utf-8")
    (tmp_path / "mintlify" / "mint.json").write_text('{"navigation":[]}', encoding="utf-8")
    (tmp_path / "mintlify" / "site-manifest.json").write_text('{"versions":[]}', encoding="utf-8")

    assert validator.validate(tmp_path) == []


def test_validate_rejects_mintlify_build_output_and_secrets(tmp_path: Path) -> None:
    write_required_paths(tmp_path)
    write_allowed_root_dirs(tmp_path)
    (tmp_path / "mintlify" / "node_modules").mkdir(parents=True)
    (tmp_path / "mintlify" / "docs").mkdir()
    (tmp_path / "mintlify" / "docs" / "secret.mdx").write_text("Authorization: Bearer abc.def", encoding="utf-8")

    errors = validator.validate(tmp_path)

    assert any("node_modules" in error for error in errors)
    assert any("敏感模式" in error and "secret.mdx" in error for error in errors)


def test_docker_compose_docs_site_profile_is_optional() -> None:
    compose = yaml.safe_load((ROOT / "docker-compose.yml").read_text(encoding="utf-8"))
    docs_site = compose["services"]["docs-site"]

    assert docs_site["profiles"] == ["docs-site"]
    assert docs_site["working_dir"] == "/workspace/mintlify"
    assert "./mintlify:/workspace/mintlify:ro" in docs_site["volumes"]
    assert "${HOST_PORT_MINTLIFY_DOCS:-3001}:3000" in docs_site["ports"]
    assert "depends_on" not in docs_site
