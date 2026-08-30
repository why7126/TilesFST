#!/usr/bin/env python3
"""Validate environment-tiered evidence gates for changes, sprints, and releases."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import environment_tiered_evidence


ROOT = Path(__file__).resolve().parents[1]


def render_markdown(report: environment_tiered_evidence.EnvironmentEvidenceReport) -> str:
    lines = [
        "## Environment Tiered Evidence Report",
        "",
        f"**Scope:** `{report.scope}`",
        f"**Target:** `{report.target}`",
        f"**Checked Files:** {len(report.checked_files)}",
        f"**Blockers:** {len(report.blockers)}",
        "",
        f"**Verdict:** {'PASS' if report.ok else 'BLOCKED'}",
    ]
    if report.blockers:
        lines.extend(["", "| Rule | File | Line | Message |", "|---|---|---:|---|"])
        for blocker in report.blockers:
            lines.append(f"| `{blocker.rule_id}` | `{blocker.file}` | {blocker.line} | {blocker.message} |")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--change", help="OpenSpec Change id")
    group.add_argument("--sprint", help="Sprint id")
    group.add_argument("--release-dir", type=Path, help="Release directory")
    parser.add_argument("--target", choices=sorted(environment_tiered_evidence.TARGETS), default="development")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    if args.change:
        report = environment_tiered_evidence.validate_change(root, args.change, target=args.target)
    elif args.sprint:
        report = environment_tiered_evidence.validate_sprint(root, args.sprint, target=args.target)
    else:
        release_dir = args.release_dir if args.release_dir.is_absolute() else root / args.release_dir
        report = environment_tiered_evidence.validate_release(root, release_dir, target=args.target)

    if args.json:
        print(json.dumps(asdict(report), ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
