---
name: "opsx-apply"
description: "Implement tasks from an OpenSpec change"
---

# opsx-apply

Use this skill when the user asks to run `/opsx-apply <target>` or implement an OpenSpec change. `<target>` may be a `REQ-*`, `BUG-*`, or raw OpenSpec `<change-id>`.

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- 大 diff 先用 `git diff --stat` / `git diff --name-only`；不得默认展开 `src/web/openapi.json`、Orval generated、coverage 或构建产物全文。
- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
- `openspec instructions apply --json` returned `contextFiles` is the default read boundary.
- UI/test定位先 `rg -l` 找文件，再分段读取目标片段。
- 默认排除 generated、node_modules、coverage、dist、archive 大目录。
- best-practices 只读 Cross-cutting Gate 命中的标签文件。
- 完成一组 task 后用 `git diff -- <changed-files>` 或 `tasks.md` 片段复核，避免重复读全部上下文。
- 命令输出优先 `max_output_tokens <= 8000`。

## Input

- `<target>`：指定目标；可为 `REQ-*`、`BUG-*` 或 OpenSpec `<change-id>`。
- Omitted：若上下文唯一可推断则使用；否则列 active changes 并询问。
- `--skip-cross-cutting-gate`：仅 P0 热修可跳过，输出必须说明理由。

## Target Resolution（MUST）

在执行 OpenSpec CLI 前，MUST 先解析 `<target>`：

| 输入类型 | 解析规则 | 下一步输出参数 |
|---|---|---|
| `REQ-*` | 读取该 REQ `trace.md` 的 `openspec_changes[]`，选择当前 active 且适合 apply 的 linked Change | 继续使用原始 `REQ-*` |
| `BUG-*` | 读取该 BUG `trace.md` 的 `openspec_changes[]`，选择当前 active 且适合 apply 的 linked Change | 继续使用原始 `BUG-*` |
| 其他 | 按 OpenSpec `<change-id>` 处理 | 使用 `<change-id>` |

- 若一个 REQ/BUG 只有一个 active linked Change，MUST 将其作为内部 `<change-id>` 继续执行。
- 若一个 REQ/BUG 有多个候选 linked Change，MUST 列出候选并要求用户选择；不得猜测。
- 若 REQ/BUG 找不到 linked Change，MUST 停止并提示先运行 `/req-opsx <REQ-id>` 或 `/bug-opsx <BUG-id>`。
- 后续 `openspec status`、`openspec instructions apply`、Workflow Sync、AI Usage hook 均使用解析后的真实 `<change-id>`。
- 最终下一步若指向 `/opsx-archive`，REQ 来源 MUST 输出 `/opsx-archive <REQ-id>`，BUG 来源 MUST 输出 `/opsx-archive <BUG-id>`，非 REQ/BUG Change 才输出 `/opsx-archive <change-id>`。

## Must Read

```text
AGENTS.md
openspec/project.md
rules/global.md
rules/coding.md
rules/testing.md
rules/security.md
rules/directory-structure.md
rules/document-governance.md
rules/requirement-management.md
rules/bug-management.md
rules/iterations-lifecycle.md
.agents/skills/workflow-sync/SKILL.md
```

Then run:

```bash
openspec status --change "<resolved-change-id>" --json
openspec instructions apply --change "<resolved-change-id>" --json
```

Read every concrete path in `contextFiles`.

When relevant, read focused snippets from:

```text
issues/requirements/<REQ>/acceptance.md + trace.md
issues/bugs/<BUG>/root-cause.md + acceptance.md + trace.md
iterations/change|archive/<sprint>/sprint.md §横切预防清单
docs/knowledge-base/best-practices/<matched>.md
```

For BUG-sourced Changes or fixes that involve root-cause claims, MUST read `rules/root-cause-evidence.md` and verify that `root-cause.md` uses `unknown` / `hypothesis` / `probable` / `confirmed` semantics. A `confirmed` root cause without evidence is a blocker until the BUG document is completed or the implementation explicitly records the remaining evidence risk.

## Sprint Inclusion Gate（MUST before implementation）

Before editing `src/`, running implementation checks, or marking any task complete, verify the target Change is eligible for `/opsx-apply`.

For every Change:

1. Identify whether the Change is linked to `REQ-*` / `BUG-*` from Change trace, proposal/design, tasks, or Issue `trace.md` `openspec_changes[]`.
2. Confirm `python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto --dry-run` resolves a Sprint and does not report sprint skipped/unresolved. This is mandatory for all Changes, including non-REQ/BUG Changes created by `/opsx-propose` or `/spec-opt`.
3. Read the resolved `iterations/change|archive/<sprint>/sprint.yaml` snippet and confirm:
   - `changes[]` contains `<change-id>`.
   - for linked REQ/BUG Changes, `requirements[]` contains linked `REQ-*` and/or `bugs[]` contains linked `BUG-*`.
   - for non-REQ/BUG Changes, `scope_estimates[]` contains an independent Change scope item or equivalent estimate/rationale for `<change-id>`.
4. For linked REQ/BUG Changes, confirm each linked Issue `trace.md` has `iteration: <sprint-id>` and `status: in_sprint` or a later delivery state.

If any check fails, **BLOCKED**: do not implement. If the linked REQ/BUG is already in a Sprint but `changes[]` lacks `<change-id>`, first run the originating `/req-opsx` or `/bug-opsx` Workflow Sync final step again to repair Sprint scope, then rerun this dry-run gate. Tell the user to run `/sprint-propose` only when the linked REQ/BUG itself is not in any Sprint scope.

If a non-REQ/BUG Change is not in Sprint scope, **BLOCKED**: do not implement. First run `/sprint-propose` for the Change or repair a known Sprint with:

```bash
python scripts/add-sprint-scope-item.py \
  --sprint <sprint-id> \
  --change <change-id> \
  --size <XS|S|M|L|XL|XXL> \
  --story-points <number> \
  --person-days <number> \
  --rationale "<估算与影响说明>"
```

Then rerun Workflow Sync, `validate-sprint-scope.py`, and this apply dry-run gate.

If the user already ran `/sprint-propose` for the linked REQ/BUG but the dry-run still reports `change <id> not in sprint scope`, treat this as Sprint scope machine-source persistence failure, not as missing user intent. Repair `iterations/change|archive/<sprint>/sprint.yaml` with:

```bash
python scripts/add-sprint-scope-item.py \
  --sprint <sprint-id> \
  [--req <REQ-id> | --bug <BUG-id>] \
  --change <change-id> \
  --size <XS|S|M|L|XL|XXL> \
  --story-points <number> \
  --person-days <number> \
  --rationale "<估算与影响说明>"
```

Then rerun Workflow Sync, `validate-sprint-scope.py`, and this apply dry-run gate. Do not ask the user to repeat the same `/sprint-propose` command when the issue/change pair and target Sprint are already known.

No Change may bypass this Sprint Inclusion Gate merely because it has no linked REQ/BUG.

## Cross-cutting Apply Gate（MUST before `src/`）

Skip only with `--skip-cross-cutting-gate` and explicit P0/hotfix reason.

### Prototype UI Gate（MUST）

If the Change or linked REQ has `prototype/`, `prototype_refs`, `AC-PROTOTYPE-*`, UI Skeleton, or explicit visual references, MUST read `docs/standards/prototype-ui-acceptance.md` before editing UI files.

- If `design.md` lacks UI Contract, first add the contract and Skeleton plan; do not mark UI implementation complete.
- Before detailed UI implementation is considered complete, record 1440px desktop visual evidence or equivalent evidence. Miniapp UI requires WeChat DevTools, real-device screenshot, or equivalent evidence.
- For high-risk visual differences, record computed style, Playwright assertion, WeChat DevTools evidence, or equivalent evidence with selector/page/viewport/result.
- Mock/API boundary MUST be explicit. If real API integration is out of scope, record it as non-goal or follow-up.

Infer tags from trace, proposal/design, change id, and tasks:

| Tag | Trigger | Best-practice |
|---|---|---|
| `admin-list` | 管理端列表、分页、table-card | `admin-list-page-consistency.md` |
| `admin-filter-dropdown` | 管理端筛选区 Select、Dropdown、Popover、Combobox、date picker、可搜索下拉、`AdminFilterSelect`、`SearchableSelect`、`admin-filter-dropdown` | `admin-list-page-consistency.md` |
| `admin-form` | 表单页、设置页、保存 CTA | `admin-form-page-consistency.md` |
| `admin-modal` | 弹窗 CRUD / modal fix | `admin-modal-width-css-cascade.md` |
| `media-upload` | 图片、视频、Logo、头像上传 | `admin-media-upload-chain.md` |

Report:

```text
Change / Tags / Refs
AC-XCUT: pass|warn|n/a
knowledge_base_refs: pass|warn|n/a
best-practices read: pass|n/a
admin-filter-dropdown: pass|warn|n/a
  - best-practice read: pass|warn|n/a
  - shared component reuse: pass|warn|n/a
  - page-local overlay CSS absence: pass|warn|n/a
  - state coverage: pass|warn|n/a
  - overlay clipping check: pass|warn|n/a
  - query parameter semantics: pass|warn|n/a
  - regression test plan: pass|warn|n/a
Verdict: PROCEED | WARN-PROCEED | BLOCKED
```

BLOCKED if add-* UI lacks required cross-cutting AC. Do not edit `src/` until resolved.

When `admin-filter-dropdown` is active:

- MUST read `docs/knowledge-base/best-practices/admin-list-page-consistency.md` before editing `src/`.
- MUST prefer `AdminFilterSelect`, `SearchableSelect`, or an equivalent shared admin filter wrapper aligned with the tile category page baseline.
- MUST block if a new or modified admin filter dropdown lacks both shared-component reuse and an explicit equivalent-wrapper rationale.
- MUST verify no page-local one-off dropdown overlay CSS, raw Hex colors, token-equivalent hardcoded colors, or divergent native controls are introduced.
- MUST include focused verification for open/select/clear/reset behavior, disabled/selected/empty/loading states as applicable, overlay clipping on desktop and narrow admin viewports when CSS or positioning changes, and existing query parameter semantics.
- MAY mark the checklist `n/a` for backend-only, database-only, release-only, non-admin UI, or admin UI Changes that do not affect filter dropdown controls.

## Implementation Loop

For each pending task:

1. Announce current task.
2. Make minimal scoped changes.
3. Add/update tests when behavior changes.
4. Mark task `- [ ]` → `- [x]` immediately after completion.
5. Re-run focused checks/tests.
6. Stop and ask if task is ambiguous, gate is blocked, or implementation reveals design conflict.

When updating `tasks.md`, preserve Chinese-first wording required by `rules/language.md`; task text MUST NOT be rewritten into English-only descriptions while marking checkboxes.

## Completion Output

Report change id, schema, completed tasks this session, total progress, tests/checks run, remaining tasks, and whether archive is ready.

## Final Step — Workflow Sync（MUST）

Before Workflow Sync, run:

```bash
python scripts/validate-openspec-language.py
```

- Exit code MUST be `0`；若失败，先修正 active Change 文档中的英文脚手架标题或全英文任务项。

Run:

```bash
python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto
```

- Exit code MUST be `0`。
- Print summary Workflow Sync Report；use `--output detail` only for debugging。
- Verify linked REQ/BUG trace has `openspec_changes[].status: applied` and `/opsx-apply` in `## 变更记录`; if missing, fix workflow sync and rerun instead of hand-editing marker blocks.
- Verify linked REQ/BUG `acceptance.md` has `acceptance_status: pending` or equivalent `## 验收结果回填` with `source_change` and resolved Sprint; if missing, rerun Workflow Sync or use `--scan-issue-subdocuments --dry-run` to diagnose.
- Do not hand-edit workflow-sync marker blocks。

## Final Step — AI Usage Post-command Hook (MUST)

After Workflow Sync exits with code `0`, run:

```bash
python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change <change-id> --sprint <resolved-sprint-id> --json
```

- Print only the compact hook summary: `status`, `usage_mode`, `command_run_count`, `sprint_snapshot`, `warning_count`, and `recommended_action`.
- Use the Sprint resolved by Workflow Sync; do not pass the literal value `auto` to `extract-ai-usage.py`.
- If local session input is unavailable, report `usage_mode: unavailable` and the recommended action; do not treat that as parent command failure.

## Final Output Contract（MUST）

命令结束前，最终回复 MUST 明确包含：

```text
下一步：<可直接执行的命令；若没有则写“暂无可推进下一步”>
待用户决策/处理：
- <需要用户选择、确认、补充或处理的事项；若没有则写“无”>
```

- 如果存在明确可推进的下一步，MUST 给出可复制执行的命令，例如 `/bug-review BUG-0122`。
- 如果下一步取决于用户选择，MUST 用条件化条目列出选项；已在「下一步」中给出的命令或动作，不得在「待用户决策/处理」中重复。
- 「待用户决策/处理」只列缺失输入、需用户选择的范围/策略/证据/验收/发布确认、阻塞项或需人工处理事项；没有则写“无”。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
