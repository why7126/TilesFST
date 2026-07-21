---
name: "bug-opsx"
description: "已评审缺陷 → OpenSpec fix-* Change（CLI）；原 /bug-to-change"
---

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- BUG 转 Change 时只读取目标 BUG 文档包、父需求 trace 摘要与候选 spec 片段；不得默认读取全部 `openspec/specs/**`。
- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
- 关联能力追溯先读取 BUG 包与 `trace.md` 中的 `related_requirement` / `related_change`，再定向读取对应 spec；不要默认在 `openspec/specs` + `openspec/changes/archive` 上做宽泛全文搜索。
- 需要历史证据时先用 `rg -l "<keyword>" openspec/specs issues/requirements` 获取候选文件；只有候选不足时才加入 `openspec/changes/archive/**`。
- 生成 Change artifacts 前只读取目标 capability 的 Requirement 标题和相关场景片段，避免整读大 spec。
- 命令输出优先控制在 `max_output_tokens <= 8000`；大范围命中先给命中数和文件列表。

# bug-opsx

Use this skill when the user asks to run the workflow command `bug-opsx`.

## Command Template

将 **`approved`** 的 `issues/bugs/BUG-*` 转为 `openspec/changes/fix-*/`。默认 **fix-***；不写 `src/`。

**Input**：`BUG-xxxx`

| Flag | 含义 |
|------|------|
| `--hotfix` | 命名/任务强调紧急发布 |
| `--change-name <id>` | 指定 fix-* id |

---

## Step 0 — 读取

```text
AGENTS.md
rules/bug-management.md
rules/testing.md
rules/api.md
openspec/project.md
```

BUG 目录：bug.md、root-cause.md、workaround.md、acceptance.md、trace.md、logs/、screenshots/

```bash
openspec list --json
```

---

## Step 0.5 — 评审门禁（MUST）

`trace.md` `status === approved`（或 `in_sprint`/`done`）否则 **停止** → `/bug-review`

---

## Step 1 — Bug Readiness

Ready / Partially Ready / Not Ready。Not Ready → `/bug-complete`，停止。

---

## Step 2 — 分析

- 现象、复现、影响（Bug Analysis Report）
- 根因分类、严重等级
- 关联 REQ/Change（若有）

---

## Step 3 — 创建 fix-* Change

```bash
openspec new change "fix-<area>-<topic>"
```

命名示例：`fix-minio-upload-timeout`、`fix-admin-login-redirect`

---

## Step 4 — Artifacts

按 CLI 生成 proposal（含 Rollback Plan）、design（根因+修复方案+测试）、specs（MODIFIED/ADDED）、tasks（**含回归测试**）。

proposal **Why** 链接 `BUG-xxxx`。

---

## Step 5 — 追溯

更新 BUG `trace.md`：

```yaml
openspec_changes:
  - change_id: fix-…
    type: fix
    status: proposed
```

tasks 末项提醒：`docs/knowledge-base/incidents/`（若适用）

---

## Step 6 — 输出

```text
## Bug → OpenSpec 完成
**BUG:** …
**Change:** fix-…
**Next:** /opsx-apply fix-…
```

---

## Guardrails

- 仅 approved
- 默认 fix-*，非 add
- 不跳过 CLI
- 不写 src

## 参考

- `.agents/skills/req-opsx/SKILL.md`（结构对照）
- `.agents/skills/opsx-apply/SKILL.md`

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md` and run:

```bash
python scripts/sync-workflow-status.py --event bug.opsx --bug <BUG-id> --change <change-id> --sprint auto
```

- Exit code **MUST** be `0` before ending this command.
- 当目标 BUG 已在 Sprint 正式范围内时，Workflow Sync **MUST** 把 `<change-id>` 写入同一 Sprint 的 `changes[]`，同步 `scope_estimates[].change`，并移除对应 open-change 延后项；结束前用 `python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto --dry-run` 确认后续 `/opsx-apply` 不再报告 `change <id> not in sprint scope`。
- Print the summary **Workflow Sync Report** to the user; use `--output detail` only for debugging.
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`).

## Final Step — AI Usage Post-command Hook (MUST)

After Workflow Sync exits with code `0`, run:

```bash
python scripts/extract-ai-usage.py --post-command-hook --workflow-event bug.opsx --bug <BUG-id> --change <change-id> --json
```

- Print only the compact hook summary: `status`, `usage_mode`, `command_run_count`, `sprint_snapshot`, `warning_count`, and `recommended_action`.
- If local session input is unavailable, report `usage_mode: unavailable` and the recommended action; do not treat that as parent command failure.
