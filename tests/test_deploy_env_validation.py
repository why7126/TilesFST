from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
DEPLOY_ENV_EXAMPLES = sorted((ROOT / "deploy").glob("**/*.env.example"))
REQUIRED_GROUPS = ("环境标识", "应用安全", "数据库", "对象存储", "端口")


def load_validator() -> ModuleType:
    module_path = ROOT / "deploy" / "scripts" / "validate-env.py"
    spec = importlib.util.spec_from_file_location("deploy_validate_env", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_validator()


def write_env(path: Path, values: dict[str, str]) -> None:
    path.write_text("\n".join(f"{key}={value}" for key, value in values.items()) + "\n", encoding="utf-8")


def test_validate_blocks_production_sqlite_debug_and_examples(tmp_path: Path) -> None:
    env_path = tmp_path / "prod.env"
    write_env(
        env_path,
        {
            "TILESFST_DEPLOY_ENV_ID": "prod-mysql-tencent-cos",
            "APP_ENV": "production",
            "APP_DEBUG": "true",
            "APP_SECRET_KEY": "replace-with-production-secret-key",
            "ADMIN_INITIAL_PASSWORD": "replace-with-production-admin-password",
            "DATABASE_URL": "sqlite:////app/data/sqlite/tilesfst.db",
            "OBJECT_STORAGE_PROVIDER": "tencent-cos",
            "OBJECT_STORAGE_ENDPOINT": "cos.ap-guangzhou.myqcloud.com",
            "OBJECT_STORAGE_ACCESS_KEY": "replace-with-tencent-cos-secret-id",
            "OBJECT_STORAGE_SECRET_KEY": "replace-with-tencent-cos-secret-key",
            "OBJECT_STORAGE_BUCKET": "replace-with-cos-bucket",
            "OBJECT_STORAGE_REGION": "ap-guangzhou",
            "OBJECT_STORAGE_AUTO_CREATE_BUCKET": "true",
        },
    )

    errors = validator.validate("prod", "mysql-tencent-cos", env_path, None)

    assert any("APP_DEBUG=true" in error for error in errors)
    assert any("DATABASE_URL must not use SQLite" in error for error in errors)
    assert any("APP_SECRET_KEY" in error for error in errors)
    assert any("OBJECT_STORAGE_AUTO_CREATE_BUCKET=true" in error for error in errors)


def test_validate_blocks_managed_minio_without_profile(tmp_path: Path) -> None:
    env_path = tmp_path / "local.env"
    write_env(
        env_path,
        {
            "TILESFST_DEPLOY_ENV_ID": "local-sqlite-minio-managed",
            "APP_ENV": "development",
            "DATABASE_URL": "sqlite:////app/data/sqlite/tilesfst.db",
            "OBJECT_STORAGE_PROVIDER": "minio",
        },
    )

    errors = validator.validate("local", "sqlite-minio-managed", env_path, None)

    assert any("managed MinIO environment" in error for error in errors)


def test_validate_allows_local_tencent_cos_without_minio_profile(tmp_path: Path) -> None:
    env_path = tmp_path / "local.env"
    write_env(
        env_path,
        {
            "TILESFST_DEPLOY_ENV_ID": "local-sqlite-tencent-cos",
            "APP_ENV": "development",
            "DATABASE_URL": "sqlite:////app/data/sqlite/tilesfst.db",
            "OBJECT_STORAGE_PROVIDER": "tencent-cos",
            "OBJECT_STORAGE_ENDPOINT": "cos.ap-guangzhou.myqcloud.com",
            "OBJECT_STORAGE_ACCESS_KEY": "replace-with-local-secret-id",
            "OBJECT_STORAGE_SECRET_KEY": "replace-with-local-secret-key",
            "OBJECT_STORAGE_BUCKET": "replace-with-local-bucket",
            "OBJECT_STORAGE_REGION": "ap-guangzhou",
            "OBJECT_STORAGE_AUTO_CREATE_BUCKET": "false",
        },
    )

    assert validator.validate("local", "sqlite-tencent-cos", env_path, None) == []


def test_deploy_env_examples_are_grouped_and_include_candidates() -> None:
    assert DEPLOY_ENV_EXAMPLES
    for path in DEPLOY_ENV_EXAMPLES:
        text = path.read_text(encoding="utf-8")
        for group in REQUIRED_GROUPS:
            assert group in text, f"{path} missing group {group}"
        assignments = [line for line in text.splitlines() if line and not line.startswith("#")]
        assert assignments, f"{path} has no variables"
        for line in assignments:
            key = line.split("=", 1)[0]
            index = text.splitlines().index(line)
            previous = text.splitlines()[index - 1] if index > 0 else ""
            assert previous.startswith("#"), f"{path} {key} missing comment"
            assert "候选" in previous or key == "TILESFST_DEPLOY_ENV_ID", f"{path} {key} missing candidate guidance"
