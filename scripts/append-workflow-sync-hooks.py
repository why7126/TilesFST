#!/usr/bin/env python3
"""Append Workflow Sync final step to Cursor workflow commands (idempotent).

Cursor commands remain the source of slash-command truth; source-command skills
carry the same guardrail for Codex skill execution.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CMD_DIR = ROOT / ".cursor/commands"
SKILL_DIR = ROOT / ".agents/skills"

HOOKS: dict[str, str] = {
    "req-capture.md": "req.capture",
    "req-generate.md": "req.generate",
    "req-complete.md": "req.complete",
    "req-review.md": "req.review",
    "req-opsx.md": "req.opsx",
    "bug-capture.md": "bug.capture",
    "bug-generate.md": "bug.generate",
    "bug-complete.md": "bug.complete",
    "bug-review.md": "bug.review",
    "bug-opsx.md": "bug.opsx",
    "opsx-propose.md": "opsx.propose",
    "opsx-apply.md": "opsx.apply",
    "opsx-archive.md": "opsx.archive",
    "sprint-propose.md": "sprint.propose",
    "sprint-apply.md": "sprint.apply",
    "sprint-archive.md": "sprint.archive",
}

EXTRA_ARGS: dict[str, str] = {
    "req-capture.md": "--req <REQ-id>",
    "req-generate.md": "--req <REQ-id>",
    "req-complete.md": "--req <REQ-id>",
    "req-review.md": "--req <REQ-id>",
    "req-opsx.md": "--req <REQ-id> --change <change-id>",
    "bug-capture.md": "--bug <BUG-id>",
    "bug-generate.md": "--bug <BUG-id>",
    "bug-complete.md": "--bug <BUG-id>",
    "bug-review.md": "--bug <BUG-id>",
    "bug-opsx.md": "--bug <BUG-id> --change <change-id>",
    "opsx-propose.md": "--change <change-id>",
    "opsx-apply.md": "--change <change-id>",
    "opsx-archive.md": "--change <change-id>",
    "sprint-propose.md": "--sprint <sprint-id>",
    "sprint-apply.md": "--sprint <sprint-id>",
    "sprint-archive.md": "--sprint <sprint-id>",
}

MARKER = "## Final Step — Workflow Sync (MUST)"


def build_footer(filename: str, event: str) -> str:
    extra = EXTRA_ARGS.get(filename, "")
    sprint_flag = "--sprint auto" if filename.startswith("opsx-") else ""
    args = f"--event {event} {extra} {sprint_flag}".strip()
    return f"""

---

{MARKER}

Read `.agents/skills/workflow-sync/SKILL.md` and run:

```bash
python scripts/sync-workflow-status.py {args}
```

- Exit code **MUST** be `0` before ending this command.
- Print the **Workflow Sync Report** to the user.
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`).
"""


def source_skill_name(command_filename: str) -> str:
    return f"source-command-{command_filename.removesuffix('.md')}/SKILL.md"


def append_if_missing(path: Path, filename: str, event: str) -> None:
    if not path.exists():
        print(f"skip missing {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"skip exists {path.relative_to(ROOT)}")
        return
    path.write_text(text.rstrip() + build_footer(filename, event), encoding="utf-8")
    print(f"updated {path.relative_to(ROOT)}")


def main() -> None:
    for filename, event in HOOKS.items():
        append_if_missing(CMD_DIR / filename, filename, event)
        append_if_missing(SKILL_DIR / source_skill_name(filename), filename, event)


if __name__ == "__main__":
    main()
