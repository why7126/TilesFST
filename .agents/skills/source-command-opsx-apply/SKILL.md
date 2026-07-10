---
name: "source-command-opsx-apply"
description: "Implement tasks from an OpenSpec change"
---

# source-command-opsx-apply

Use this skill when the user asks to run `/opsx-apply <change-id>` or implement an OpenSpec change.

## Context Budget Guardrails（MUST）

- 大 diff 先用 `git diff --stat` / `git diff --name-only`；不得默认展开 `src/web/openapi.json`、Orval generated、coverage 或构建产物全文。
- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- `openspec instructions apply --json` returned `contextFiles` is the default read boundary.
- UI/test定位先 `rg -l` 找文件，再分段读取目标片段。
- 默认排除 generated、node_modules、coverage、dist、archive 大目录。
- best-practices 只读 Cross-cutting Gate 命中的标签文件。
- 完成一组 task 后用 `git diff -- <changed-files>` 或 `tasks.md` 片段复核，避免重复读全部上下文。
- 命令输出优先 `max_output_tokens <= 8000`。

## Input

- `<change-id>`：指定 Change。
- Omitted：若上下文唯一可推断则使用；否则列 active changes 并询问。
- `--skip-cross-cutting-gate`：仅 P0 热修可跳过，输出必须说明理由。

## Must Read

```text
AGENTS.md
openspec/project.md
rules/global.md
rules/coding.md
rules/testing.md
rules/security.md
rules/directory-structure.md
.agents/skills/workflow-sync/SKILL.md
```

Then run:

```bash
openspec status --change "<change-id>" --json
openspec instructions apply --change "<change-id>" --json
```

Read every concrete path in `contextFiles`.

When relevant, read focused snippets from:

```text
issues/requirements/<REQ>/acceptance.md + trace.md
issues/bugs/<BUG>/root-cause.md + acceptance.md + trace.md
iterations/change|archive/<sprint>/sprint.md §横切预防清单
docs/knowledge-base/best-practices/<matched>.md
```

## Cross-cutting Apply Gate（MUST before `src/`）

Skip only with `--skip-cross-cutting-gate` and explicit P0/hotfix reason.

Infer tags from trace, proposal/design, change id, and tasks:

| Tag | Trigger | Best-practice |
|---|---|---|
| `admin-list` | 管理端列表、分页、table-card | `admin-list-page-consistency.md` |
| `admin-form` | 表单页、设置页、保存 CTA | `admin-form-page-consistency.md` |
| `admin-modal` | 弹窗 CRUD / modal fix | `admin-modal-width-css-cascade.md` |
| `media-upload` | 图片、视频、Logo、头像上传 | `admin-media-upload-chain.md` |

Report:

```text
Change / Tags / Refs
AC-XCUT: pass|warn|n/a
knowledge_base_refs: pass|warn|n/a
best-practices read: pass|n/a
Verdict: PROCEED | WARN-PROCEED | BLOCKED
```

BLOCKED if add-* UI lacks required cross-cutting AC. Do not edit `src/` until resolved.

## Implementation Loop

For each pending task:

1. Announce current task.
2. Make minimal scoped changes.
3. Add/update tests when behavior changes.
4. Mark task `- [ ]` → `- [x]` immediately after completion.
5. Re-run focused checks/tests.
6. Stop and ask if task is ambiguous, gate is blocked, or implementation reveals design conflict.

## Completion Output

Report change id, schema, completed tasks this session, total progress, tests/checks run, remaining tasks, and whether archive is ready.

## Final Step — Workflow Sync（MUST）

Run:

```bash
python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto
```

- Exit code MUST be `0`。
- Print Workflow Sync Report。
- Verify linked REQ/BUG trace has `openspec_changes[].status: applied` and `/opsx-apply` in `## 变更记录`; if missing, fix workflow sync and rerun instead of hand-editing marker blocks.
- Do not hand-edit workflow-sync marker blocks。
