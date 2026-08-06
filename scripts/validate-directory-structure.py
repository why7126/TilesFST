#!/usr/bin/env python3
"""
文档用途：校验项目目录结构
文档内容：检查禁止的根目录文件、必需目录、Docker部署文件是否存在
内容来源：AI自动生成，项目团队确认
更新方式：目录规范变化时同步更新
备注：该脚本可纳入CI，防止AI或开发人员随意破坏目录结构
"""

from collections import defaultdict
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    "rules/directory-structure.md",
    "openspec/project.md",
    "src/backend/app/main.py",
    "src/web/package.json",
    "src/miniapp/app.json",
    "docker-compose.yml",
    "docker-compose.prod.yml",
    "docker-compose.prod.external.yml",
    "src/backend/Dockerfile",
    "src/web/Dockerfile",
    "src/web/nginx.conf",
]

ALLOWED_ROOT_FILES = {
    "AGENTS.md",
    "README.md",
    ".gitignore",
    ".dockerignore",
    ".coveragerc",
    ".env.example",
    "docker-compose.yml",
    "docker-compose.prod.yml",
    "docker-compose.prod.external.yml",
    "pytest.ini",
    "project.yaml",
    "DOCUMENT_METADATA_INDEX.md",
}

ALLOWED_ROOT_DIRS = {
    "rules",
    "docs",
    "openspec",
    "issues",
    "iterations",
    "releases",
    "mintlify",
    "compatibility",
    ".agents",
    "src",
    "tests",
    "scripts",
    "data",
    "deploy",
}

IGNORED_ROOT_NAMES = {
    ".DS_Store",
    ".env",
    ".env.local",
    ".env.mysql",
    ".env.prod-backfill",
    ".pytest_cache",
    ".venv",
}

FORBIDDEN_PATHS = {
    "openspec/changes/archive": "OpenSpec 已归档 Change 必须位于 openspec/archive/，不得回退到 legacy openspec/changes/archive/。",
}

FORBIDDEN_MINTLIFY_NAMES = {
    ".env",
    ".env.local",
    "node_modules",
    ".mintlify",
    "dist",
    "build",
    ".next",
    "coverage",
}

FORBIDDEN_MINTLIFY_SUFFIXES = {
    ".sqlite",
    ".db",
    ".log",
}

MINTLIFY_SENSITIVE_PATTERNS = (
    re.compile(r"\bAPP_SECRET_KEY\s*=", re.I),
    re.compile(r"\bDATABASE_URL\s*=", re.I),
    re.compile(r"mysql(\+\w+)?://", re.I),
    re.compile(r"\bMINIO_(?:ACCESS|SECRET)_KEY\s*=", re.I),
    re.compile(r"\bOBJECT_STORAGE_(?:ACCESS|SECRET)_KEY\s*=", re.I),
    re.compile(r"\bAuthorization\s*:", re.I),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]+", re.I),
    re.compile(r"\bCookie\s*:", re.I),
)

ISSUE_ROOTS = ("issues/requirements", "issues/bugs")
ISSUE_STAGE_DIRS = ("plan", "review", "archive")
ISSUE_PREFIX_RE = re.compile(r"^(REQ|BUG)-(\d{4,})(?:-|$)")
DEPLOY_ALLOWED_TOP_LEVEL = {"README.md", "docs-site", "local", "prod", "scripts"}
DEPLOY_FORBIDDEN_EXTENSIONS = {".db", ".sqlite", ".sqlite3", ".tar"}
DEPLOY_FORBIDDEN_SUFFIXES = (".tar.gz", ".env", ".env.local", ".env.prod")
DEPLOY_FORBIDDEN_DIR_NAMES = {"__pycache__", "data", "minio", "runtime", "uploads", "images"}


def _git_status_for_path(root: Path, rel: Path) -> str | None:
    if not (root / ".git").exists():
        return None
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain", "--", str(rel)],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout[:2] if result.stdout else ""


def _is_git_ignored_or_untracked(root: Path, rel: Path) -> bool:
    status = _git_status_for_path(root, rel)
    return status in {"", "!!", "??"}


def validate_issue_stage_dirs(root: Path) -> list[str]:
    errors: list[str] = []

    for root_rel in ISSUE_ROOTS:
        issue_root = root / root_rel
        if not issue_root.exists():
            continue

        issue_dirs_by_short_id: dict[str, list[Path]] = defaultdict(list)
        for stage in ISSUE_STAGE_DIRS:
            stage_dir = issue_root / stage
            if not stage_dir.exists():
                continue
            if not stage_dir.is_dir():
                errors.append(f"Issue 阶段路径不是目录: {stage_dir.relative_to(root)}")
                continue

            for issue_dir in sorted(stage_dir.iterdir()):
                if not issue_dir.is_dir():
                    continue
                match = ISSUE_PREFIX_RE.match(issue_dir.name)
                if not match:
                    continue

                short_id = f"{match.group(1)}-{match.group(2)}"
                issue_dirs_by_short_id[short_id].append(issue_dir)

                if not any(issue_dir.iterdir()):
                    errors.append(f"Issue 目录为空: {issue_dir.relative_to(root)}")

                if not (issue_dir / "trace.md").exists():
                    errors.append(f"Issue 目录缺少 trace.md: {issue_dir.relative_to(root)}")

        for short_id, paths in sorted(issue_dirs_by_short_id.items()):
            if len(paths) <= 1:
                continue
            if all(path.parent.name == "archive" for path in paths):
                continue
            locations = "、".join(str(path.relative_to(root)) for path in paths)
            errors.append(f"Issue 短编号重复: {short_id} 同时存在于 {locations}")

    return errors


def validate_deploy_dir(root: Path) -> list[str]:
    errors: list[str] = []
    deploy_root = root / "deploy"
    if not deploy_root.exists():
        return errors
    if not deploy_root.is_dir():
        return [f"deploy 不是目录: {deploy_root.relative_to(root)}"]

    for child in sorted(deploy_root.iterdir()):
        if child.name not in DEPLOY_ALLOWED_TOP_LEVEL:
            errors.append(f"deploy 存在未登记一级路径: {child.relative_to(root)}")

    for path in sorted(deploy_root.rglob("*")):
        rel = path.relative_to(root)
        if path.is_dir():
            if path.name in DEPLOY_FORBIDDEN_DIR_NAMES:
                errors.append(f"deploy 存在禁止运行时目录: {rel}")
            continue
        if path.name == ".env" or any(path.name.endswith(suffix) for suffix in DEPLOY_FORBIDDEN_SUFFIXES):
            if not path.name.endswith(".env.example"):
                if not _is_git_ignored_or_untracked(root, rel):
                    errors.append(f"deploy 存在禁止提交的真实 env 文件: {rel}")
        if path.suffix in DEPLOY_FORBIDDEN_EXTENSIONS or path.name.endswith(".tar.gz"):
            errors.append(f"deploy 存在禁止提交的运行时或镜像文件: {rel}")

    return errors


def validate(root: Path = ROOT) -> list[str]:
    errors = []

    for item in REQUIRED_PATHS:
        if not (root / item).exists():
            errors.append(f"缺少必需路径: {item}")

    for child in root.iterdir():
        if child.name in IGNORED_ROOT_NAMES:
            continue
        if child.name.startswith(".git"):
            continue
        if child.is_file() and child.name not in ALLOWED_ROOT_FILES:
            errors.append(f"根目录存在未登记文件: {child.name}")
        if child.is_dir() and child.name not in ALLOWED_ROOT_DIRS:
            errors.append(f"根目录存在未登记目录: {child.name}")

    for item, reason in FORBIDDEN_PATHS.items():
        if (root / item).exists():
            errors.append(f"存在禁止路径: {item}。{reason}")

    errors.extend(validate_issue_stage_dirs(root))
    errors.extend(validate_deploy_dir(root))
    errors.extend(validate_mintlify_dir(root))

    return errors


def validate_mintlify_dir(root: Path) -> list[str]:
    errors: list[str] = []
    site_root = root / "mintlify"
    if not site_root.exists():
        return errors
    if not site_root.is_dir():
        return [f"mintlify 不是目录: {site_root.relative_to(root)}"]

    allowed_children = {
        "README.md",
        "index.mdx",
        "docs.json",
        "favicon.svg",
        "assets",
        "docs",
        "governance",
        "guides",
        "releases",
        "roles",
        "site-manifest.json",
        "tasks",
        "versions",
    }
    for child in site_root.iterdir():
        if child.name not in allowed_children:
            errors.append(f"mintlify/ 存在未登记路径: {child.relative_to(root)}")

    for path in site_root.rglob("*"):
        rel = path.relative_to(root)
        if path.name in FORBIDDEN_MINTLIFY_NAMES:
            errors.append(f"mintlify/ 存在禁止提交的构建产物或环境文件: {rel}")
        if path.is_file() and path.suffix.lower() in FORBIDDEN_MINTLIFY_SUFFIXES:
            errors.append(f"mintlify/ 存在禁止提交的运行时文件: {rel}")
        if path.is_file() and path.stat().st_size > 5 * 1024 * 1024:
            errors.append(f"mintlify/ 单文件超过 5MB，请改用共享截图去重或外部公开资产: {rel}")
        if path.is_file() and path.suffix.lower() in {".md", ".mdx", ".json", ".txt", ".yml", ".yaml"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in MINTLIFY_SENSITIVE_PATTERNS:
                if pattern.search(text):
                    errors.append(f"mintlify/ 公开站点文件包含敏感模式 {pattern.pattern}: {rel}")
    return errors


def main() -> int:
    errors = validate(ROOT)
    if errors:
        print("目录结构校验失败：")
        for err in errors:
            print(f"- {err}")
        return 1

    print("目录结构校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
