---
description: 缺陷生成 - 仅生成 bug.md
---

**Input**：`BUG-xxxx`（须 `capture.md`）

**Output**：**仅** `bug.md`；trace → `status: draft`

## bug.md frontmatter

```yaml
---
bug_id: BUG-xxxx
title:
severity: high
status: draft
owner:
discovered_at:
environment:
related_requirement:
related_change:
---
```

正文：现象、复现、期望/实际、影响范围、严重等级说明。

## Next

`/bug-complete BUG-xxxx`

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md` and run:

```bash
python scripts/sync-workflow-status.py --event bug.generate --bug <BUG-id> --sprint auto
```

- Exit code **MUST** be `0` before ending this command.
- Print the **Workflow Sync Report** to the user.
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`).
