#!/usr/bin/env python3
"""Pre-push safety scan for files that should not enter Git."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_TEXT_BYTES = 1024 * 1024
LARGE_FILE_BYTES = 10 * 1024 * 1024

TEXT_SUFFIXES = {
    ".cfg",
    ".conf",
    ".css",
    ".env",
    ".example",
    ".html",
    ".js",
    ".json",
    ".md",
    ".mdx",
    ".py",
    ".sh",
    ".sql",
    ".ts",
    ".tsx",
    ".txt",
    ".wxml",
    ".wxss",
    ".yaml",
    ".yml",
}

HIGH_CONFIDENCE_SECRET_PATTERNS = [
    re.compile(r"(?i)\b(AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"(?i)\b(?:mysql|postgresql|mongodb|redis)://[^\s'\"<>]+"),
]

ENV_SECRET_PATTERNS = [
    re.compile(r"(?i)^\s*(?:secret|token|api[_-]?key|access[_-]?key|authorization|cookie)\s*[:=]\s*['\"]?[^'\"\s<>{}]{12,}", re.MULTILINE),
    re.compile(r"(?i)\b(?:MINIO|S3|COS)_[A-Z0-9_]*(?:SECRET|KEY|TOKEN)[A-Z0-9_]*\s*[:=]\s*[^\s'\"<>]{8,}"),
]

ABS_PATH_PATTERN = re.compile(r"/Users/[^\s'\"<>]+|/home/[^\s'\"<>]+")

SAFE_PLACEHOLDERS = (
    "<access_token>",
    "<token>",
    "<secret>",
    "<local-project>",
    "<user-home>",
    "change-me",
    "change-me-in-local-env",
    "example",
    "localhost",
)


def run_git(args: list[str]) -> list[str]:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or result.stdout.strip() or f"git {' '.join(args)} failed")
    return [line for line in result.stdout.splitlines() if line]


def staged_and_tracked_files() -> set[str]:
    files = set(run_git(["diff", "--cached", "--name-only"]))
    files.update(run_git(["diff", "--name-only"]))
    files.update(run_git(["ls-files", "--others", "--exclude-standard"]))
    return files


def all_files() -> set[str]:
    return set(run_git(["ls-files"])) | {
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }


def is_runtime_or_artifact(rel: str) -> bool:
    parts = rel.split("/")
    if parts[0] in {"dist", "build", "coverage", "node_modules"}:
        return True
    if parts[0] == "data" and len(parts) > 1 and parts[1] in {"runtime", "uploads", "tmp", "minio", "mysql", "s3"}:
        return True
    return rel.endswith((".sqlite", ".sqlite3", ".db", ".tar", ".tgz", ".zip", ".7z", ".gz"))


def is_real_env(rel: str) -> bool:
    name = Path(rel).name
    if name == ".env" or name.startswith(".env."):
        return not name.endswith(".example")
    if rel.startswith("deploy/") and name.endswith(".env"):
        return True
    return rel == "scripts/build-images.env"


def is_reference_context(rel: str) -> bool:
    return rel.startswith(("docs/", "issues/", "iterations/", "openspec/archive/", "tests/"))


def is_env_like(rel: str) -> bool:
    name = Path(rel).name.lower()
    return ".env" in name or name.endswith((".env.example", ".example"))


def is_probably_text(path: Path) -> bool:
    if path.suffix.lower() in TEXT_SUFFIXES:
        return True
    try:
        sample = path.read_bytes()[:4096]
    except OSError:
        return False
    return b"\0" not in sample


def redact(value: str) -> str:
    value = value.strip()
    if len(value) <= 16:
        return "<redacted>"
    return f"{value[:6]}...<redacted>...{value[-4:]}"


def scan_text(rel: str, path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if path.stat().st_size > MAX_TEXT_BYTES:
        warnings.append(f"{rel}: text file larger than scan window")
        return errors, warnings
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        warnings.append(f"{rel}: cannot read file: {exc}")
        return errors, warnings
    patterns = list(HIGH_CONFIDENCE_SECRET_PATTERNS)
    if is_env_like(rel):
        patterns.extend(ENV_SECRET_PATTERNS)
    for pattern in patterns:
        for match in pattern.finditer(text):
            raw = match.group(0)
            if any(token in raw.lower() for token in SAFE_PLACEHOLDERS):
                continue
            errors.append(f"{rel}: possible secret or connection string: {redact(raw)}")
            break
    for match in ABS_PATH_PATTERN.finditer(text):
        raw = match.group(0)
        lowered_raw = raw.lower()
        if "<local-project>" in lowered_raw or "<user-home>" in lowered_raw:
            continue
        if "[^" in raw:
            continue
        message = f"{rel}: local absolute path detected: {redact(raw)}"
        if is_reference_context(rel):
            warnings.append(message)
        else:
            errors.append(message)
        break
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="scan all current files instead of staged + tracked files")
    args = parser.parse_args()

    candidates = sorted(all_files() if args.all else staged_and_tracked_files())
    errors: list[str] = []
    warnings: list[str] = []
    scanned = 0

    for rel in candidates:
        path = ROOT / rel
        if not path.exists() or path.is_dir():
            continue
        scanned += 1
        try:
            size = path.stat().st_size
        except OSError as exc:
            warnings.append(f"{rel}: cannot stat file: {exc}")
            continue
        if is_real_env(rel):
            errors.append(f"{rel}: real environment file must not be tracked or staged")
        if is_runtime_or_artifact(rel):
            errors.append(f"{rel}: runtime data, database, build artifact, or archive must not be tracked or staged")
        if size > LARGE_FILE_BYTES:
            warnings.append(f"{rel}: large file ({size} bytes), confirm it belongs in Git")
        if is_probably_text(path):
            text_errors, text_warnings = scan_text(rel, path)
            errors.extend(text_errors)
            warnings.extend(text_warnings)

    print("## Git Safety Check")
    print()
    print(f"Scope: {'all files' if args.all else 'staged + modified tracked + untracked files'}")
    print(f"Files scanned: {scanned}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    if errors:
        print("\nErrors:")
        for item in errors[:50]:
            print(f"- {item}")
        if len(errors) > 50:
            print(f"- ... {len(errors) - 50} more")
    if warnings:
        print("\nWarnings:")
        for item in warnings[:50]:
            print(f"- {item}")
        if len(warnings) > 50:
            print(f"- ... {len(warnings) - 50} more")
    if errors:
        print("\nResult: BLOCKED. Remove, untrack, or redact the reported files/content before push.")
        return 1
    print("\nResult: PASS. Review warnings if any before push.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
