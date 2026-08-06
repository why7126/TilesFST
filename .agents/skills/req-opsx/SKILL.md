---
name: "req-opsx"
description: "已评审需求 → OpenSpec Change（CLI 驱动）；原 /requirement-to-opsx"
---

# req-opsx

Use this skill when the user asks to run the workflow command `req-opsx`.

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- REQ 转 Change 时只读取目标 REQ 六件套摘要与候选 spec 片段；不得默认读取全部 `openspec/specs/**`。
- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
- 检索先定位再分段读取；大范围 `rg/find` 默认排除 Harness、模板 assets、历史 agent 目录、archive、generated、node_modules、dist、coverage。
- 命令输出优先 `max_output_tokens <= 8000`；大 diff、OpenAPI/Orval 生成物、测试日志、Workflow Sync 输出先给摘要或命中数。


## Command Template

将 **`approved`** 的 `issues/requirements/REQ-*` 转为 `openspec/changes/<change-id>/`（proposal / design / specs / tasks）。**不写 `src/`**；实现用 `/opsx-apply`。

**Input**：`REQ-xxxx` 或 `REQ-xxxx-name`

| Flag | 含义 |
|------|------|
| `--type add\|fix\|update` | 强制 change 类型 |
| `--strategy <name>` | css-port、tailwind-ds 等 |
| `--skip-explore` | 跳过 UI 策略探讨 |
| `--change-name <kebab-case>` | 指定 change id |

---

## 前置关系

```text
/req-capture → /req-explore → /req-generate → /req-complete → /req-review (approved)
        │
        └─ /sprint-propose sprint-* --req REQ-*  →  /req-opsx REQ-*  →  /opsx-apply  →  /opsx-archive
```

兼容追溯场景可在 `approved` 状态直接 `/req-opsx`，但最终输出 MUST 提醒：若该 REQ 尚未纳入 Sprint，下一步先执行 `/sprint-propose`，不得直接 `/opsx-apply`。

```text
        │
        └─ legacy/追溯：/req-opsx REQ-*  →  必须补 /sprint-propose  →  /opsx-apply
```

---

## Step 0 — 必须读取

```text
AGENTS.md
openspec/project.md
rules/global.md
rules/requirement-management.md
rules/ui-design.md
rules/testing.md
rules/directory-structure.md
```

```bash
openspec list --json
openspec list --specs
```

REQ 目录：requirement.md、user-stories.md、business-flow.md、acceptance.md、trace.md、prototype/**

---

## Step 0.5 — 评审门禁（MUST — 无例外）

读 `trace.md`（或 requirement.md frontmatter）`status`：

| status | 动作 |
|--------|------|
| `approved` | 继续 |
| `in_sprint` | 可继续（须已完成 `/req-review`） |
| `done` | 可继续（追溯/补建 change） |
| `pending_review` / `draft` / `captured` / `enriching` / … | **立即停止** → `/req-review REQ-xxxx --approve` |

未评审 **不得** opsx；**不得**因 Sprint 规划已写入而 bypass（见 `rules/requirement-management.md` §4.1）。

---

## Step 1 — Readiness

输出 **Requirement Readiness Report**（ready / partially ready / not ready）。

**Not Ready** → `/req-complete REQ-xxxx`，**停止**，不创建 change。

---

## Step 2 — 影响分析与 Change 分类

```yaml
impact: { backend, web, miniapp, admin, database, storage, api }
capabilities: { new: [], modified: [] }
```

| 条件 | change_type | 示例 |
|------|-------------|------|
| 无相关 spec | add | add-user-login |
| 已有实现，验收/视觉未过 | fix | fix-login-css-port |
| 仅规范文案 | update | update-login-acceptance-sync |

---

## Step 3 — 原型与验收冲突（MUST）

`prototype/web/` 存在时输出 Conflict Report；优先级：

```text
HTML > PNG > *-context.md > acceptance.md > ui-design.md > openspec/specs
```

design.md **MUST** 含 Conflict Resolution；delta spec 用 MODIFIED/REMOVED 消化。

---

## Step 4 — UI Explore Gate

`impact.web` 且有 prototype 时，无 `--strategy` 且非 `--skip-explore`：选 CSS Port / DS / Asset，写入 design.md D1。

---

## Step 5 — 创建 Change（CLI）

```bash
openspec new change "<change-id>"
openspec status --change "<change-id>" --json
```

---

## Step 6 — 生成 Artifacts

```bash
openspec instructions <artifact-id> --change "<change-id>" --json
```

按 schema 顺序写 proposal、design、specs、tasks。MODIFIED 标题 **MUST** 与 `openspec/specs/` 一致。

文档语言 MUST 遵守 `rules/language.md`：

- `proposal.md`、`design.md`、`tasks.md`、`trace.md` 标题、章节名和任务项 MUST 中文优先；不得保留 `Why`、`What Changes`、`Implementation`、`Validation`、`Root Cause` 等英文脚手架标题。
- OpenSpec 关键字、命令、路径、代码标识符和 API 字段 MAY 保留英文。
- 生成后运行 `python scripts/validate-openspec-language.py`；失败时先修正文档再进入 Workflow Sync。

---

## Step 7 — 追溯

更新 REQ `trace.md`：

```yaml
openspec_changes:
  - change_id: …
    type: fix
    status: proposed
```

创建 `openspec/changes/<id>/trace.md`（UI 类含 PNG checklist）。

---

## Step 8 — 输出

```text
## Req → OpenSpec 完成
**REQ:** …
**Change:** …
**Next:** 若 Workflow Sync 已解析到 Sprint：`/opsx-apply <REQ-id>` 或 `/sprint-apply sprint-xxx`；若未解析到 Sprint：先 `/sprint-propose sprint-xxx --req <REQ-id>`
**待用户决策/处理:** 若目标 Sprint 未确定，必须由用户选择 sprint-xxx；若 Change 范围需要拆分，必须确认拆分策略。
```

---

## Guardrails

| 规则 | 说明 |
|------|------|
| 仅 approved | 未评审不得 opsx |
| 不替代 req-complete | 文档不全先 complete |
| 不跳过 CLI | 禁止手写 change 目录 |
| 不写 src | 实现用 opsx-apply |

---

## 参考

- `.agents/skills/req-complete/SKILL.md`
- `.agents/skills/opsx-apply/SKILL.md`、`opsx-archive.md`、`opsx-explore.md`
- 归档样例：`openspec/archive/`

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md` and run:

```bash
python scripts/sync-workflow-status.py --event req.opsx --req <REQ-id> --change <change-id> --sprint auto
```

- Exit code **MUST** be `0` before ending this command.
- 当目标 REQ 已在 Sprint 正式范围内时，Workflow Sync **MUST** 把 `<change-id>` 写入同一 Sprint 的 `changes[]`，同步 `scope_estimates[].change`，并移除对应 open-change 延后项；结束前用 `python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto --dry-run` 确认后续 `/opsx-apply` 不再报告 `change <id> not in sprint scope`。
- 最终下一步若指向 `/opsx-apply`，MUST 使用原始 `<REQ-id>`，不得改用真实 `<change-id>`；`/opsx-apply` 内部再从 REQ trace 解析 linked Change。
- Print the summary **Workflow Sync Report** to the user; use `--output detail` only for debugging.
- Confirm the summary includes Issue subdocument checked/updated counts when applicable; `requirement.md` must reference the linked Change without conflicting with `trace.md`.
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`).

## Final Step — AI Usage Post-command Hook (MUST)

After Workflow Sync exits with code `0`, run:

```bash
python scripts/extract-ai-usage.py --post-command-hook --workflow-event req.opsx --req <REQ-id> --change <change-id> --json
```

- Print only the compact hook summary: `status`, `usage_mode`, `command_run_count`, `sprint_snapshot`, `warning_count`, and `recommended_action`.
- If local session input is unavailable, report `usage_mode: unavailable` and the recommended action; do not treat that as parent command failure.

## Final Output Contract（MUST）

命令结束前，最终回复 MUST 明确包含：

```text
下一步：<可直接执行的命令；若没有则写“暂无可推进下一步”>
待用户决策/处理：
- <需要用户选择、确认、补充或处理的事项；若没有则写“无”>
```

- 如果存在明确可推进的下一步，MUST 给出可复制执行的命令，例如 `/bug-review BUG-0122 --approve`。
- 如果下一步取决于用户选择，MUST 用条件化条目列出选项；已在「下一步」中给出的命令或动作，不得在「待用户决策/处理」中重复。
- 「待用户决策/处理」只列缺失输入、需用户选择的范围/策略/证据/验收/发布确认、阻塞项或需人工处理事项；没有则写“无”。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
