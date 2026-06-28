---
description: 缺陷评审 - 确认是否修复；仅 approved 可 bug-opsx 与进 Sprint
---

**Input**：`BUG-xxxx`

Flags：`--approve` | `--reject` | `--defer` | `--wont-fix`

**Output**：`review.md`；status → `approved` | `rejected` | `deferred` | `wont_fix`

## Step — 目录迁移（MUST，`--approve` 时）

Read `rules/issues-lifecycle.md`。

| Flag | 迁移 |
|------|------|
| `--approve` | `plan/` → `review/` |
| `--reject` / `--defer` / `--wont-fix` | **跳过**（保留 `plan/`） |

`--approve` 时 **MUST** 在 Workflow Sync **之前**运行：

```bash
python scripts/promote-issue-stage.py --bug <BUG-id> --to review --reason "/bug-review --approve"
```

- Exit code **MUST** be `0`（已在 `review/` 时可 no-op）。
- 打印脚本 stdout（迁移路径、引用更新计数）。

## 评审清单

- [ ] 可复现或根因充分
- [ ] 严重等级合理
- [ ] 回归验收明确
- [ ] 是否需 hotfix 路径

## 门禁

**仅 `approved`** → `/bug-opsx`、`/sprint-propose`（P0 BUG 优先）

## Next

`/bug-opsx BUG-xxxx`

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md` and run:

```bash
python scripts/sync-workflow-status.py --event bug.review --bug <BUG-id> --sprint auto
```

- Exit code **MUST** be `0` before ending this command.
- Print the **Workflow Sync Report** to the user.
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`).
