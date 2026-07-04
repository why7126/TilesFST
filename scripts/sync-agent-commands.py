#!/usr/bin/env python3
"""Sync slash commands from .cursor/commands/ to other AI agent directories.

Source of truth: .cursor/commands/*.md

Targets:
  - .claude/commands/   (grouped subdirs, extended frontmatter)
  - .opencode/commands/ (flat *.md, description frontmatter)
  - .kiro/prompts/      (flat *.prompt.md)
  - .codex/prompts/     (flat *.md, legacy slash-command format)

Run from repo root:
  python scripts/sync-agent-commands.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / ".cursor" / "commands"

GROUP_PREFIXES = ("opsx", "req", "bug", "sprint", "release", "build")
GROUP_DISPLAY = {
    "opsx": "OPSX",
    "req": "REQ",
    "bug": "BUG",
    "sprint": "Sprint",
    "release": "Release",
    "build": "Build",
}
WORD_UPPER = {"opsx": "OPSX", "req": "REQ", "bug": "BUG", "api": "API", "ds": "DS"}


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    block = text[4:end]
    body = text[end + 5 :]
    meta: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, body


def title_words(slug: str) -> str:
    parts = slug.split("-")
    return " ".join(WORD_UPPER.get(p.lower(), p.capitalize()) for p in parts)


def split_command(stem: str) -> tuple[str | None, str]:
    for group in GROUP_PREFIXES:
        prefix = f"{group}-"
        if stem.startswith(prefix):
            return group, stem[len(prefix) :]
    return None, stem


def claude_display_name(stem: str) -> str:
    group, action = split_command(stem)
    if group:
        return f"{GROUP_DISPLAY[group]}: {title_words(action)}"
    return title_words(stem)


def claude_relpath(stem: str) -> Path:
    group, action = split_command(stem)
    if group:
        return Path(group) / f"{action}.md"
    return Path(f"{stem}.md")


def claude_tags(category: str) -> str:
    cat = category.lower()
    if cat == "bootstrap":
        return "[bootstrap, workflow]"
    return "[workflow]"


def write_claude(stem: str, meta: dict[str, str], body: str) -> Path:
    out = ROOT / ".claude" / "commands" / claude_relpath(stem)
    out.parent.mkdir(parents=True, exist_ok=True)
    category = meta.get("category", "Workflow")
    content = (
        "---\n"
        f'name: "{claude_display_name(stem)}"\n'
        f"description: {meta.get('description', stem)}\n"
        f"category: {category}\n"
        f"tags: {claude_tags(category)}\n"
        "---\n"
        f"{body}"
    )
    out.write_text(content, encoding="utf-8")
    return out


def write_opencode(stem: str, meta: dict[str, str], body: str) -> Path:
    out = ROOT / ".opencode" / "commands" / f"{stem}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    content = (
        "---\n"
        f"description: {meta.get('description', stem)}\n"
        "---\n"
        f"{body}"
    )
    out.write_text(content, encoding="utf-8")
    return out


def write_kiro(stem: str, meta: dict[str, str], body: str) -> Path:
    out = ROOT / ".kiro" / "prompts" / f"{stem}.prompt.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    content = (
        "---\n"
        f"description: {meta.get('description', stem)}\n"
        "---\n"
        f"{body}"
    )
    out.write_text(content, encoding="utf-8")
    return out


def write_codex(stem: str, meta: dict[str, str], body: str) -> Path:
    out = ROOT / ".codex" / "prompts" / f"{stem}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    content = (
        "---\n"
        f"description: {meta.get('description', stem)}\n"
        "---\n"
        f"{body}"
    )
    out.write_text(content, encoding="utf-8")
    return out


def expected_outputs(stem: str) -> list[Path]:
    paths = [
        ROOT / ".claude" / "commands" / claude_relpath(stem),
        ROOT / ".opencode" / "commands" / f"{stem}.md",
        ROOT / ".kiro" / "prompts" / f"{stem}.prompt.md",
        ROOT / ".codex" / "prompts" / f"{stem}.md",
    ]
    return paths


def prune_stale(generated: set[Path]) -> list[Path]:
    removed: list[Path] = []
    target_roots = [
        (ROOT / ".claude" / "commands", ".md"),
        (ROOT / ".opencode" / "commands", ".md"),
        (ROOT / ".kiro" / "prompts", ".prompt.md"),
        (ROOT / ".codex" / "prompts", ".md"),
    ]
    for root, suffix in target_roots:
        if not root.exists():
            continue
        for path in root.rglob(f"*{suffix}"):
            if path not in generated:
                path.unlink()
                removed.append(path)
                # remove empty parent dirs under claude/commands
                parent = path.parent
                while parent != root and parent.exists() and not any(parent.iterdir()):
                    parent.rmdir()
                    parent = parent.parent
    return removed


def main() -> int:
    if not SOURCE_DIR.is_dir():
        print(f"Missing source directory: {SOURCE_DIR}", file=sys.stderr)
        return 1

    sources = sorted(SOURCE_DIR.glob("*.md"))
    if not sources:
        print("No command files found in .cursor/commands/", file=sys.stderr)
        return 1

    generated: set[Path] = set()
    for src in sources:
        stem = src.stem
        meta, body = parse_frontmatter(src.read_text(encoding="utf-8"))
        generated.add(write_claude(stem, meta, body))
        generated.add(write_opencode(stem, meta, body))
        generated.add(write_kiro(stem, meta, body))
        generated.add(write_codex(stem, meta, body))

    removed = prune_stale(generated)
    print(f"Synced {len(sources)} commands from .cursor/commands/")
    print(f"  → .claude/commands/ ({len(list((ROOT / '.claude' / 'commands').rglob('*.md')))} files)")
    print(f"  → .opencode/commands/ ({len(list((ROOT / '.opencode' / 'commands').glob('*.md')))} files)")
    print(f"  → .kiro/prompts/ ({len(list((ROOT / '.kiro' / 'prompts').glob('*.prompt.md')))} files)")
    print(f"  → .codex/prompts/ ({len(list((ROOT / '.codex' / 'prompts').glob('*.md')))} files)")
    if removed:
        print(f"Removed {len(removed)} stale file(s):")
        for path in removed:
            print(f"  - {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
