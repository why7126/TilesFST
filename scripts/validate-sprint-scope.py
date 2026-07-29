#!/usr/bin/env python3
"""Validate that sprint.md Scope mirrors sprint.yaml formal scope."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from workflow_sync.collect import load_sprint, read_text


def short_issue_code(issue_id: str) -> str:
    parts = issue_id.split("-", 2)
    if len(parts) >= 2 and parts[0] in {"REQ", "BUG"}:
        return f"{parts[0]}-{parts[1]}"
    return issue_id


def extract_scope_section(text: str) -> str | None:
    match = re.search(r"^## 2\. Scope\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else None


def extract_marker_block(text: str, name: str) -> str:
    pattern = re.compile(
        rf"<!-- workflow-sync:{re.escape(name)}:start -->(.*?)"
        rf"<!-- workflow-sync:{re.escape(name)}:end -->",
        re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1) if match else ""


def validate_sprint_scope(sprint_id: str, focus: set[str]) -> list[str]:
    sprint = load_sprint(sprint_id)
    if sprint is None:
        return [f"sprint `{sprint_id}` not found"]

    md_path = sprint.path / "sprint.md"
    if not md_path.exists():
        return [f"{md_path} not found"]

    text = read_text(md_path)
    scope = extract_scope_section(text)
    if scope is None:
        return [f"{md_path} missing `## 2. Scope` section"]

    main_scope = scope.split("<!-- workflow-sync:", 1)[0]
    req_block = extract_marker_block(text, "scope-requirements")
    bug_block = extract_marker_block(text, "scope-bugs")
    change_block = extract_marker_block(text, "scope-changes")

    failures: list[str] = []

    def in_focus(item_id: str) -> bool:
        return not focus or item_id in focus or short_issue_code(item_id) in focus

    for req_id in sprint.requirements:
        if not in_focus(req_id):
            continue
        if req_id not in main_scope:
            failures.append(f"{req_id} missing from sprint.md `## 2. Scope` main table")
        if short_issue_code(req_id) not in req_block:
            failures.append(f"{req_id} missing from workflow-sync requirements table")

    for bug_id in sprint.bugs:
        if not in_focus(bug_id):
            continue
        if bug_id not in main_scope:
            failures.append(f"{bug_id} missing from sprint.md `## 2. Scope` main table")
        if short_issue_code(bug_id) not in bug_block:
            failures.append(f"{bug_id} missing from workflow-sync bugs table")

    for change_id in sprint.changes:
        if focus and change_id not in focus:
            continue
        if change_id not in main_scope:
            failures.append(f"{change_id} missing from sprint.md `## 2. Scope` main table")
        if change_id not in change_block:
            failures.append(f"{change_id} missing from workflow-sync changes table")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sprint_id")
    parser.add_argument(
        "--item",
        action="append",
        default=[],
        help="Limit validation to an issue/change id; may be repeated.",
    )
    args = parser.parse_args()

    failures = validate_sprint_scope(args.sprint_id, set(args.item))
    if failures:
        print("## Sprint Scope Validation Failed")
        print()
        print(f"**Sprint:** {args.sprint_id}")
        print()
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("## Sprint Scope Validation")
    print()
    print(f"**Sprint:** {args.sprint_id}")
    if args.item:
        print(f"**Items:** {', '.join(args.item)}")
    print()
    print("Result: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
