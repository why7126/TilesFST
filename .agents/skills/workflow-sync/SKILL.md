---
name: workflow-sync
description: Sync REQ/BUG/Sprint/OpenSpec workflow status after req/bug/sprint/opsx commands
---

# workflow-sync

After any workflow command that changes REQ, BUG, Change, or Sprint scope/status, **MUST** run workflow sync.

## Command

```bash
python scripts/sync-workflow-status.py \
  --event <event> \
  [--sprint auto|sprint-xxx] \
  [--change <change-id>] \
  [--req <REQ-id>] \
  [--bug <BUG-id>]
```

| Flag | Purpose |
|------|---------|
| `--sprint auto` | Resolve sprint by context (see below) |
| `--sprint none` | Skip sprint-level artifacts; sync issue/trace/registry only |
| `--check` | Fail if derived docs drift (CI) |
| `--dry-run` | Report only, no writes |

### Sprint resolution (`--sprint auto`)

| Event kind | Resolution |
|------------|------------|
| `req.*` / `bug.*` with `--req` / `--bug` | Sync sprint **only if** that issue is listed in `iterations/<sprint>/sprint.yaml` `requirements` or `bugs`; otherwise skip sprint artifacts and report `_skipped — BUG-xxxx not in sprint scope_` |
| `opsx.*` with `--change` | Sync sprint **only if** that change is in sprint `changes` |
| `sprint.*` | Use explicit sprint or the single `in_progress` sprint |
| No issue/change focus | Fall back to single `in_progress` sprint (legacy default) |

When sprint sync is skipped, the script still updates the target issue `trace.md`, `_registry.yaml`, and parent requirement related-bug index when applicable.

## Event mapping

| Command family | `--event` |
|----------------|-----------|
| capture | `req.capture` 与/或 `bug.capture`（按本次创建的条目分别执行） |
| req-capture | `req.capture` |
| req-generate | `req.generate` |
| req-complete | `req.complete` |
| req-review | `req.review` |
| req-opsx | `req.opsx` |
| bug-capture | `bug.capture` |
| bug-generate | `bug.generate` |
| bug-complete | `bug.complete` |
| bug-review | `bug.review` |
| bug-opsx | `bug.opsx` |
| opsx-propose | `opsx.propose` |
| opsx-apply | `opsx.apply` |
| opsx-archive | `opsx.archive` |
| sprint-propose | `sprint.propose` |
| sprint-apply | `sprint.apply` |
| sprint-archive | `sprint.archive` |

## Guardrails

1. Print the **Workflow Sync Report** from script stdout.
2. If exit code != 0, fix drift and re-run before ending the parent command.
3. Do **not** hand-edit `sprint.md` Scope marker blocks; use the script.
4. Marker blocks: `<!-- workflow-sync:scope-*:start/end -->`.
5. Scope 表 archived 时间与 §里程碑「目标日期」MUST 为 `YYYY-MM-DD HH:mm:ss` 且时分秒 MUST 非 `00:00:00`（见 `rules/document-governance.md` §6.1）。
6. §Sprint 目标 不在 sync 范围；纳入 REQ/BUG 时 MUST 同步更新 **编号列表** 与 **`### xxx 要点`** 两处。
7. Issue `trace.md` 的 `## 变更记录` MUST 保持表头紧跟章节标题；若历史记录行出现在表头前，脚本 SHOULD 自动归一化并在报告中体现 delta。

## Refreshed artifacts

- `iterations/<sprint>/sprint.md` Scope tables + note；§里程碑「目标日期」列 legacy 仅日期 → `YYYY-MM-DD HH:mm:ss`
- `iterations/<sprint>/acceptance-report.md` issue status lines + note
- `iterations/<sprint>/release-note.md` publish status
- `issues/requirements|bugs/*/trace.md` status + iteration + `openspec_changes[].status`（Frontmatter 与 fenced `yaml` 块均需同步）+ `## 变更记录` workflow event 行 / 表格格式归一化
- parent requirement `trace.md` related bug index
- `issues/requirements/_registry.yaml` / `issues/bugs/_registry.yaml`
- 写入时自动维护 Frontmatter `created_at` / `updated_at`（`rules/document-governance.md` §2.4）
