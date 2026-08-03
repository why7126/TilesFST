#!/usr/bin/env python3
"""Validate deploy environment files without printing secret values."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXAMPLE_TOKENS = (
    "change-me",
    "replace-with",
    "example.com",
    "minioadmin",
)
EXTERNAL_PROVIDERS = {"tencent-cos", "volcengine-tos", "s3-compatible"}
MANAGED_MINIO_PROVIDERS = {"minio"}
SELF_HOSTED_MINIO_PROVIDERS = {"self-hosted-minio"}


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


def is_true(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def has_example_value(value: str | None) -> bool:
    lowered = str(value or "").lower()
    return any(token in lowered for token in EXAMPLE_TOKENS)


def validate(domain: str, environment: str, env_path: Path, profile: str | None) -> list[str]:
    values = parse_env(env_path)
    errors: list[str] = []
    env_id = f"{domain}-{environment}"
    provider = values.get("OBJECT_STORAGE_PROVIDER", "")
    database_url = values.get("DATABASE_URL", "")
    profile = profile or ""

    if values.get("TILESFST_DEPLOY_ENV_ID") not in {"", env_id}:
        errors.append(f"{env_id}: TILESFST_DEPLOY_ENV_ID must match selected environment")

    if domain == "prod":
        if values.get("APP_ENV") != "production":
            errors.append(f"{env_id}: APP_ENV must be production")
        if is_true(values.get("APP_DEBUG")):
            errors.append(f"{env_id}: APP_DEBUG=true is not allowed in production")
        if database_url.startswith("sqlite:"):
            errors.append(f"{env_id}: production DATABASE_URL must not use SQLite")
        for key in ("APP_SECRET_KEY", "ADMIN_INITIAL_PASSWORD", "DATABASE_URL", "OBJECT_STORAGE_ACCESS_KEY", "OBJECT_STORAGE_SECRET_KEY", "OBJECT_STORAGE_BUCKET"):
            if has_example_value(values.get(key)):
                errors.append(f"{env_id}: {key} must not use an example value in production")

    if provider in EXTERNAL_PROVIDERS:
        if profile == "self-hosted-storage":
            errors.append(f"{env_id}: external object storage must not enable self-hosted-storage profile")
        for key in ("OBJECT_STORAGE_ENDPOINT", "OBJECT_STORAGE_ACCESS_KEY", "OBJECT_STORAGE_SECRET_KEY", "OBJECT_STORAGE_BUCKET", "OBJECT_STORAGE_REGION"):
            if not values.get(key):
                errors.append(f"{env_id}: {key} is required for {provider}")
        if domain == "prod" and is_true(values.get("OBJECT_STORAGE_AUTO_CREATE_BUCKET")):
            errors.append(f"{env_id}: OBJECT_STORAGE_AUTO_CREATE_BUCKET=true is not allowed for production external storage")

    if provider in MANAGED_MINIO_PROVIDERS and profile != "self-hosted-storage":
        errors.append(f"{env_id}: managed MinIO environment must enable self-hosted-storage profile")

    if provider in SELF_HOSTED_MINIO_PROVIDERS and profile == "self-hosted-storage":
        errors.append(f"{env_id}: external MinIO environment must not enable self-hosted-storage profile")

    if re.search(r"\s", provider):
        errors.append(f"{env_id}: OBJECT_STORAGE_PROVIDER must not contain whitespace")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate deploy env file")
    parser.add_argument("--domain", required=True, choices=("local", "prod"))
    parser.add_argument("--environment", required=True)
    parser.add_argument("--env-file", required=True, type=Path)
    parser.add_argument("--profile", default="")
    args = parser.parse_args()

    if not args.env_file.exists():
        print(f"BLOCKED: env file not found: {args.env_file}", file=sys.stderr)
        return 1

    errors = validate(args.domain, args.environment, args.env_file, args.profile or None)
    if errors:
        print("部署环境校验失败：")
        for error in errors:
            print(f"- {error}")
        print("修复建议：复制对应 *.env.example 为真实 env 后替换占位值，或选择匹配的环境 ID/profile。")
        return 1

    print(f"部署环境校验通过：{args.domain}-{args.environment}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
