#!/usr/bin/env python3
"""Generate and validate release deployment upgrade plans."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RELEASES_DIR = ROOT / "releases"
PRODUCT_VERSION_FILE = ROOT / "src" / "shared" / "product-version.ts"

SUPPORT_LEVELS = {
    "fresh-install-supported",
    "adjacent-upgrade-supported",
    "cross-version-upgrade-supported",
    "cross-version-upgrade-requires-manual-review",
    "unsupported",
}
SOURCE_CONFIDENCE = {"verified", "reconstructed", "partial", "fresh"}
NO_IMPACT_VALUES = {"", "none", "na", "n/a", "not_applicable", "not applicable", "无", "不涉及"}
ENV_EXAMPLE_PATTERNS = (
    ".env.example",
    "src/backend/.env.example",
    "src/backend/.env.docker",
    "deploy/**/*.env.example",
    "scripts/build-images.env.example",
)
PRODUCTION_REQUIRED_KEYS = {
    "APP_ENV",
    "APP_SECRET_KEY",
    "DATABASE_URL",
    "ADMIN_INITIAL_PASSWORD",
    "OBJECT_STORAGE_PROVIDER",
    "OBJECT_STORAGE_BUCKET",
    "OBJECT_STORAGE_ACCESS_KEY",
    "OBJECT_STORAGE_SECRET_KEY",
    "TILESFST_IMAGE_TAG",
}
UNSAFE_VALUE_TOKENS = (
    "change-me",
    "replace-with",
    "example.com",
    "minioadmin",
    "sqlite:",
)
SENSITIVE_PATTERNS = (
    re.compile(r"\bAPP_SECRET_KEY\s*=", re.I),
    re.compile(r"\bDATABASE_URL\s*=\s*(?!<)", re.I),
    re.compile(r"mysql(\+\w+)?://", re.I),
    re.compile(r"\b(?:MINIO|OBJECT_STORAGE)_(?:SECRET|ACCESS)_KEY\s*=", re.I),
    re.compile(r"\bAuthorization\s*:", re.I),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]+", re.I),
    re.compile(r"\bCookie\s*:", re.I),
    re.compile(r"/Users/[^\\s\"']+", re.I),
)


class UpgradePlanError(ValueError):
    """User-facing validation error."""


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def rel_path(path: Path, *, root: Path = ROOT) -> str:
    return os.path.relpath(path.resolve(), root)


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise UpgradePlanError(f"missing file: {path}") from None
    except json.JSONDecodeError as exc:
        raise UpgradePlanError(f"invalid JSON {path}: {exc}") from None
    if not isinstance(data, dict):
        raise UpgradePlanError(f"{path} must contain a JSON object")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def semver_key(version: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise UpgradePlanError(f"unsupported version format: {version}")
    return tuple(int(part) for part in match.groups())


def release_versions(root: Path = ROOT) -> list[str]:
    releases_dir = root / "releases"
    versions = [path.name for path in releases_dir.iterdir() if path.is_dir() and re.fullmatch(r"v\d+\.\d+\.\d+", path.name)]
    return sorted(versions, key=semver_key)


def versions_between(from_version: str, to_version: str, root: Path = ROOT) -> list[str]:
    start = semver_key(from_version)
    end = semver_key(to_version)
    return [version for version in release_versions(root) if start < semver_key(version) <= end]


def previous_version(to_version: str, root: Path = ROOT) -> str | None:
    versions = [version for version in release_versions(root) if semver_key(version) < semver_key(to_version)]
    return versions[-1] if versions else None


def default_release_from_versions(to_version: str, root: Path = ROOT) -> list[str]:
    """Return the upgrade paths expected for every normal release."""
    sources = ["fresh"]
    previous = previous_version(to_version, root)
    if previous:
        sources.append(previous)
    return sources


def release_dir(version: str, root: Path = ROOT) -> Path:
    return root / "releases" / version


def release_fact(version: str, root: Path = ROOT) -> dict[str, Any] | None:
    path = release_dir(version, root) / "release.json"
    if not path.exists():
        return None
    return read_json(path)


def extract_product_version(path: Path = PRODUCT_VERSION_FILE) -> str | None:
    if not path.exists():
        return None
    match = re.search(r"PRODUCT_VERSION\s*=\s*['\"]([^'\"]+)['\"]", path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_env_text(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


def env_example_files(root: Path = ROOT) -> list[Path]:
    files: list[Path] = []
    for pattern in ENV_EXAMPLE_PATTERNS:
        files.extend(path for path in root.glob(pattern) if path.is_file())
    return sorted(set(files), key=lambda path: rel_path(path, root=root))


def env_snapshot(root: Path = ROOT) -> dict[str, dict[str, str]]:
    return {rel_path(path, root=root): parse_env_text(path.read_text(encoding="utf-8")) for path in env_example_files(root)}


def diff_env_snapshots(source: dict[str, dict[str, str]], target: dict[str, dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    diff: dict[str, list[dict[str, str]]] = {
        "added": [],
        "removed": [],
        "changed_default": [],
        "required_in_production": [],
        "unsafe_example_value": [],
        "manual_review": [],
    }
    paths = sorted(set(source) | set(target))
    for path in paths:
        before = source.get(path, {})
        after = target.get(path, {})
        for key in sorted(set(after) - set(before)):
            diff["added"].append({"path": path, "key": key, "recommendation": "确认生产环境是否需要显式配置"})
        for key in sorted(set(before) - set(after)):
            diff["removed"].append({"path": path, "key": key, "recommendation": "确认生产环境是否仍残留废弃变量"})
        for key in sorted(set(before) & set(after)):
            if before[key] != after[key]:
                diff["changed_default"].append({"path": path, "key": key, "recommendation": "复核默认值变化是否影响部署"})
        for key, value in sorted(after.items()):
            if key in PRODUCTION_REQUIRED_KEYS:
                diff["required_in_production"].append({"path": path, "key": key, "recommendation": "生产环境必须显式配置，不得依赖示例值"})
            if any(token in value.lower() for token in UNSAFE_VALUE_TOKENS):
                diff["unsafe_example_value"].append({"path": path, "key": key, "recommendation": "生产环境不得使用该示例值"})
    return diff


def current_env_diff(root: Path = ROOT) -> dict[str, Any]:
    snapshot = env_snapshot(root)
    return {
        "status": "manual_review",
        "source": "current-env-examples",
        "summary": diff_env_snapshots({}, snapshot),
        "notes": [
            "当前仓库尚未保存历史版本 env 示例快照；跨版本 env diff 需结合 Git tag、release 归档或人工快照复核。",
            "输出仅包含变量名、分类和建议，不包含真实 env 值。",
        ],
    }


def impact_requires_database(release_data: dict[str, Any] | None) -> bool:
    if not isinstance(release_data, dict):
        return False
    impact = release_data.get("impact_scope")
    if not isinstance(impact, dict):
        return False
    return str(impact.get("database", "")).strip().lower() not in NO_IMPACT_VALUES


def path_exists_summary(path: Path, root: Path = ROOT) -> dict[str, Any]:
    return {"path": rel_path(path, root=root), "exists": path.exists()}


def source_confidence_for(version: str, root: Path = ROOT) -> str:
    if version == "fresh":
        return "fresh"
    data = release_fact(version, root)
    if not data:
        return "partial"
    has_release_version = data.get("version") == version
    has_announcement = (release_dir(version, root) / str(data.get("announcement", "announcement.mdx"))).exists()
    return "verified" if has_release_version and has_announcement else "reconstructed"


def manifest_exists(version: str, root: Path = ROOT) -> bool:
    data = release_fact(version, root)
    name = str(data.get("image_manifest", "image-manifest.json")) if data else "image-manifest.json"
    return (release_dir(version, root) / name).exists()


def classify_support(from_version: str, to_version: str, root: Path, blockers: list[str], warnings: list[str]) -> str:
    if blockers:
        return "unsupported"
    if from_version == "fresh":
        return "fresh-install-supported"
    previous = previous_version(to_version, root)
    if from_version == previous:
        return "adjacent-upgrade-supported"
    between = versions_between(from_version, to_version, root)
    if not between:
        return "unsupported"
    missing_release = [version for version in between if release_fact(version, root) is None]
    missing_manifest = [version for version in between if not manifest_exists(version, root)]
    if missing_release or missing_manifest:
        warnings.append(
            "跨版本路径缺少完整 release 或 image manifest 证据，需人工复核："
            f"missing_release={missing_release}, missing_manifest={missing_manifest}"
        )
        return "cross-version-upgrade-requires-manual-review"
    warnings.append("跨版本路径虽具备 release/image 基础事实，仍需补充演练、DB/env/object storage 和回滚证据后才能标记 supported。")
    return "cross-version-upgrade-requires-manual-review"


def build_plan(from_version: str, to_version: str, root: Path = ROOT) -> dict[str, Any]:
    target_release = release_fact(to_version, root)
    source_release = None if from_version == "fresh" else release_fact(from_version, root)
    blockers: list[str] = []
    warnings: list[str] = []
    if target_release is None:
        blockers.append(f"target release missing: releases/{to_version}/release.json")
    elif target_release.get("version") != to_version:
        blockers.append(f"target release version mismatch: expected {to_version}")
    if from_version != "fresh" and source_release is None:
        warnings.append(f"source release fact missing or partial: releases/{from_version}/release.json")
    if target_release and target_release.get("image_required") is True and not manifest_exists(to_version, root):
        blockers.append(f"target image manifest missing: releases/{to_version}/image-manifest.json")

    support_level = classify_support(from_version, to_version, root, blockers, warnings)
    target_dir = release_dir(to_version, root)
    previous = previous_version(to_version, root)
    db_impact = impact_requires_database(target_release)
    if db_impact:
        warnings.append("目标版本声明数据库影响，必须补充 MySQL drift/smoke、备份和回滚证据。")

    plan = {
        "schema_version": 1,
        "generated_at": now_text(),
        "from_version": from_version,
        "to_version": to_version,
        "support_level": support_level,
        "source_confidence": source_confidence_for(from_version, root),
        "version_facts": {
            "target_release": path_exists_summary(target_dir / "release.json", root),
            "target_image_manifest": path_exists_summary(target_dir / "image-manifest.json", root),
            "product_version": extract_product_version(root / "src" / "shared" / "product-version.ts"),
            "git_ref": {"status": "manual_review", "recommendation": "使用发布 tag 或 commit 补充源码快照锚点"},
            "deployment_image_tag": {"key": "TILESFST_IMAGE_TAG", "expected": to_version, "value": "<redacted-or-operator-confirmed>"},
        },
        "impact_summary": {
            "database": "requires_mysql_evidence" if db_impact else "none",
            "environment": "manual_review",
            "docker": "target image manifest required",
            "api": "manual_review_for_cross_version" if from_version != "fresh" else "none",
            "object_storage": "manual_review_for_cross_version" if from_version != "fresh" else "none",
            "maintenance_jobs": "dry_run_required_if_write_tasks_exist",
        },
        "env_diff": current_env_diff(root),
        "required_checks": [
            f"python scripts/validate-release-upgrade.py validate-plan --plan releases/{to_version}/upgrade-plans/{safe_plan_name(from_version, to_version)}",
            f"python scripts/validate-image-build.py validate-manifest --release {to_version}",
            "docker compose config --quiet 或目标 deploy Compose config 校验",
            "若 database impact 非 none：python scripts/check-mysql-schema-drift.py --database-url \"$DATABASE_URL\"",
            "部署后 health/login/core API/Web/media smoke",
        ],
        "steps": upgrade_steps(from_version, to_version, previous),
        "rollback": rollback_steps(from_version, to_version, db_impact),
        "blockers": blockers,
        "warnings": warnings,
        "evidence": {
            "release": path_exists_summary(target_dir / "release.json", root),
            "image_manifest": path_exists_summary(target_dir / "image-manifest.json", root),
            "database": "na" if not db_impact else "pending_mysql_drift_or_smoke",
            "object_storage": "manual_review",
            "post_upgrade_smoke": "pending",
            "post_rollback_smoke": "pending",
        },
    }
    assert_public_safe(plan, artifact="upgrade plan")
    return plan


def safe_plan_name(from_version: str, to_version: str) -> str:
    source = "fresh" if from_version == "fresh" else from_version
    return f"{source}-to-{to_version}.json"


def upgrade_steps(from_version: str, to_version: str, previous: str | None) -> list[str]:
    if from_version == "fresh":
        return [
            f"确认 releases/{to_version}/release.json 与 image-manifest.json 存在且版本一致。",
            f"准备生产 env，显式设置 APP_ENV=production、MySQL DATABASE_URL、对象存储变量和 TILESFST_IMAGE_TAG={to_version}。",
            "执行目标 Compose config 校验。",
            "在空 MySQL 库执行应用启动初始化并确认默认管理员可登录。",
            "完成 health、login、核心 API、Web 静态资源和媒体读写或只读 smoke。",
        ]
    if previous == from_version:
        return [
            f"确认来源版本 {from_version} 和目标版本 {to_version} release 事实源存在。",
            "备份数据库、对象存储影响范围和当前 env 摘要。",
            f"加载或拉取目标镜像，将 TILESFST_IMAGE_TAG 更新为 {to_version}。",
            "执行目标 Compose config 校验并重启服务。",
            "完成升级后 health、login、核心 API、Web、小程序或媒体 smoke。",
        ]
    return [
        f"聚合 {from_version} 到 {to_version} 所有中间版本的 release、DB、env、Docker、API、对象存储和维护任务影响。",
        "先完成 dry-run、备份确认和人工复核；必要时拆为多个相邻版本升级。",
        f"加载或拉取目标镜像，将 TILESFST_IMAGE_TAG 更新为 {to_version}。",
        "执行升级后 smoke；缺少演练证据时不得标记为 cross-version-upgrade-supported。",
    ]


def rollback_steps(from_version: str, to_version: str, db_impact: bool) -> dict[str, Any]:
    previous_label = "人工确认的上一稳定版本" if from_version == "fresh" else from_version
    return {
        "previous_image": previous_label,
        "target_image": to_version,
        "env_snapshot": "旧 env 变量名摘要、hash 或负责人确认；不得记录真实值",
        "database_backup": "required" if db_impact or from_version != "fresh" else "recommended",
        "object_storage_backup": "只读确认；若执行写入型维护任务则必须备份或记录不可逆风险",
        "rollback_steps": [
            f"回退 TILESFST_IMAGE_TAG 或镜像包到 {previous_label}。",
            "恢复旧 env 摘要对应的真实 env，由运维在生产环境执行。",
            "如数据库已写入变更，根据备份恢复或已验证反向迁移执行。",
            "完成回滚后 health、login、核心 API、Web 和媒体 smoke。",
        ],
        "post_rollback_smoke": "pending",
    }


def assert_public_safe(data: Any, *, artifact: str) -> None:
    text = json.dumps(data, ensure_ascii=False)
    matches = [pattern.pattern for pattern in SENSITIVE_PATTERNS if pattern.search(text)]
    if matches:
        raise UpgradePlanError(f"{artifact} contains sensitive pattern(s): {', '.join(matches)}")


def validate_plan_data(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("from_version", "to_version", "support_level", "source_confidence", "impact_summary", "required_checks", "steps", "rollback", "blockers", "warnings", "evidence"):
        if key not in data:
            errors.append(f"missing required field: {key}")
    if data.get("support_level") not in SUPPORT_LEVELS:
        errors.append(f"invalid support_level: {data.get('support_level')}")
    if data.get("source_confidence") not in SOURCE_CONFIDENCE:
        errors.append(f"invalid source_confidence: {data.get('source_confidence')}")
    rollback = data.get("rollback")
    if not isinstance(rollback, dict):
        errors.append("rollback must be an object")
    else:
        for key in ("previous_image", "target_image", "env_snapshot", "database_backup", "object_storage_backup", "rollback_steps", "post_rollback_smoke"):
            if key not in rollback:
                errors.append(f"rollback missing field: {key}")
    try:
        assert_public_safe(data, artifact="upgrade plan")
    except UpgradePlanError as exc:
        errors.append(str(exc))
    return errors


def write_plan(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    plan = build_plan(args.from_version, args.to_version, root)
    output = args.output
    if output is None:
        output = root / "releases" / args.to_version / "upgrade-plans" / safe_plan_name(args.from_version, args.to_version)
    write_json(output, plan)
    print("升级计划已生成：")
    print(f"- path: {rel_path(output, root=root)}")
    print(f"- support_level: {plan['support_level']}")
    print(f"- blockers: {len(plan['blockers'])}")
    print(f"- warnings: {len(plan['warnings'])}")
    return 0


def validate_plan(args: argparse.Namespace) -> int:
    data = read_json(args.plan)
    errors = validate_plan_data(data)
    if errors:
        print("升级计划校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1
    print("升级计划校验通过：")
    print(f"- plan: {args.plan}")
    print(f"- support_level: {data.get('support_level')}")
    print(f"- blockers: {len(data.get('blockers') or [])}")
    print(f"- warnings: {len(data.get('warnings') or [])}")
    return 0


def print_env_diff(args: argparse.Namespace) -> int:
    source = env_snapshot(args.from_dir.resolve()) if args.from_dir else {}
    target = env_snapshot(args.to_dir.resolve()) if args.to_dir else env_snapshot(args.root.resolve())
    diff = diff_env_snapshots(source, target)
    print(json.dumps(diff, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)

    plan_parser = sub.add_parser("plan", help="Generate an upgrade plan")
    plan_parser.add_argument("--from", dest="from_version", required=True)
    plan_parser.add_argument("--to", dest="to_version", required=True)
    plan_parser.add_argument("--output", type=Path)
    plan_parser.set_defaults(func=write_plan)

    validate_parser = sub.add_parser("validate-plan", help="Validate an upgrade plan")
    validate_parser.add_argument("--plan", required=True, type=Path)
    validate_parser.set_defaults(func=validate_plan)

    env_parser = sub.add_parser("env-diff", help="Diff env example files")
    env_parser.add_argument("--from-dir", type=Path)
    env_parser.add_argument("--to-dir", type=Path)
    env_parser.set_defaults(func=print_env_diff)

    args = parser.parse_args()
    try:
        return int(args.func(args))
    except UpgradePlanError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
