#!/usr/bin/env python3
"""Validate source-command skills follow Agent context budget guardrails."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agents" / "skills"
REQUIRED_RULE = "rules/agent-context-budget.md"

# Patterns that are risky when written as a positive/default instruction.
BROAD_READ_PATTERNS = [
    re.compile(r"cat\s+rules/\*\.md"),
    re.compile(r"cat\s+docs/\*\*"),
    re.compile(r"cat\s+issues/\*\*"),
    re.compile(r"cat\s+iterations/\*\*"),
    re.compile(r"ls\s+-R"),
    re.compile(r"rg\s+[^\n]*\s\.\s*(?:$|[;&|])"),
]

NEGATION_HINTS = (
    "不要",
    "禁止",
    "不得",
    "MUST NOT",
    "must not",
    "Do not",
    "don't",
    "Don’t",
    "避免",
)


def is_negated(line: str) -> bool:
    return any(hint in line for hint in NEGATION_HINTS)


def validate_skill(path: Path) -> list[str]:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if REQUIRED_RULE not in text:
        errors.append(f"{rel}: 缺少 `{REQUIRED_RULE}` 引用")

    if "Context Budget Guardrails" not in text:
        errors.append(f"{rel}: 缺少 Context Budget Guardrails 章节")

    for lineno, line in enumerate(text.splitlines(), start=1):
        if is_negated(line):
            continue
        for pattern in BROAD_READ_PATTERNS:
            if pattern.search(line):
                errors.append(f"{rel}:{lineno}: 存在默认宽泛读取指令 `{line.strip()}`")
                break

    return errors


def main() -> int:
    skill_paths = sorted(SKILLS_DIR.glob("source-command-*/SKILL.md"))
    if not skill_paths:
        print("未找到 source-command 技能文件。", file=sys.stderr)
        return 1

    errors: list[str] = []
    for path in skill_paths:
        errors.extend(validate_skill(path))

    if errors:
        print("Agent 上下文预算校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Agent 上下文预算校验通过：{len(skill_paths)} 个 source-command 技能均已接入预算规则。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
