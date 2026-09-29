---
name: "opsx-apply"
description: "Implement tasks from an OpenSpec change"
created_at: 2026-09-08 17:17:14
updated_at: 2026-09-10 10:31:52
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
- Evidence source MUST be clear: DevTools, static tests, local smoke and development API evidence may satisfy development acceptance, but MUST NOT be described as trial, real-device, or online proof. Gaps that cannot be verified in the current workflow should record the current evidence source, unavailable reason, follow-up owner or N/A rationale. `production_only_pending` is historical compatibility wording only and is not recommended for new records.

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

MUST 读取并执行 `docs/standards/command-execution-order.md` §5 Apply 持续执行契约。

1. 持续选择依赖满足的未完成任务；分组完成与进度汇报不结束当前命令。
2. 在当前范围内实现并运行聚焦验证；可恢复错误先定位、修复、复测。
3. 验证通过后才勾选任务，继续下一项；必需验证和同步收尾仍需跟踪。
4. 真正阻塞按详细契约记录证据与恢复条件，继续独立任务；必要人工确认只暂停相关依赖，用户明确停止则停止全部工作。
5. 上下文恢复承接已完成任务、证据与既有决策，不重复请求继续授权。
6. 全部适用任务与必需验证完成后走完成收尾；否则仅在无可执行任务时报告部分完成。

When updating `tasks.md`, preserve Chinese-first wording required by `rules/language.md`; task text MUST NOT be rewritten into English-only descriptions while marking checkboxes.

## 产品数据采集与链路观测门禁（MUST）

Before implementation, if the Change touches API, DB, audit logs, usage events, Task Trace, Web request wrapper, miniapp request wrapper, or App request wrapper, MUST read `docs/standards/product-data-collection-observability.md` and confirm the Change has `product_data_collection_observability` with `affected_layers`, `reason`, and `validation`.

Run `python scripts/validate-product-data-observability-gates.py --change <change-id>` when the script exists or when this gate is in scope. Missing declaration, weak N/A reason, or missing validation evidence is a blocker before marking related tasks complete.

## 收尾前执行核对

MUST 执行共享契约§5.6–5.8：收尾前逐项检查剩余任务的授权、依赖、资源和必需验证，仍有可执行任务即继续，不发最终回复等待“继续”。集中已知人工问题并映射受阻项，承接已有答复；进度问询用中间消息回答后继续实际工作。

分别展示实现完成、自动验证通过、人工待验、外部阻塞。连续两次同类失败且无进展时记录失败签名、次数及恢复条件并切换独立任务，新条件可验证后才恢复，保留累计历史。不要删除或放宽验收项。

持续执行治理的验收必须运行实际行为场景；通过 `scripts/validate-apply-behavior.py` 检查脱敏证据，不把关键词检查或理想夹具当实际Agent通过。执行入口为 `scripts/run-apply-behavior.py`，环境受阻仅保留相关任务待验，继续其他工作。

## Completion Output

按详细契约区分完成与部分完成，报告 Change、schema、实际进度、验证结果、剩余任务及阻塞恢复条件。部分完成时 archive_ready 为 false，不建议归档；全部完成也须核对人工验收门禁。

## Final Step — Workflow Sync（MUST）

按 `docs/standards/command-execution-order.md` §5.4–5.5 选择状态同步分支。部分完成仅执行无完成事件的事实刷新，不要求 applied；以下完成事件和验收检查仅用于全部适用任务及必需验证完成的路径。

Before Workflow Sync, run:

```bash
python scripts/validate-openspec-language.py
```

- Exit code MUST be `0`；若失败，先修正 active Change 文档中的英文脚手架标题或全英文任务项。

完成路径运行：

```bash
python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto
```

- Exit code MUST be `0`。
- Print summary Workflow Sync Report；use `--output detail` only for debugging。
- Verify linked REQ/BUG trace has `openspec_changes[].status: applied` and `/opsx-apply` in `## 变更记录`; if missing, fix workflow sync and rerun instead of hand-editing marker blocks.
- Verify linked REQ/BUG `acceptance.md` has `acceptance_status: pending` or equivalent `## 验收结果回填` with `source_change` and resolved Sprint; if missing, rerun Workflow Sync or use `--scan-issue-subdocuments --dry-run` to diagnose.
- Do not hand-edit workflow-sync marker blocks。

## Final Step — AI Usage Post-command Hook (MUST)

完成或部分完成的真实状态同步成功后，运行以下 best-effort 用量 hook；workflow-event 仅用于命令用量归因，不替代完成状态判定：

```bash
python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change <change-id> --sprint <resolved-sprint-id> --json
```

- Print only the compact hook summary: `status`, `usage_mode`, `command_run_count`, `sprint_snapshot`, `warning_count`, and `recommended_action`.
- Use the Sprint resolved by Workflow Sync; do not pass the literal value `auto` to `extract-ai-usage.py`.
- If local session input is unavailable, report `usage_mode: unavailable` and the recommended action; do not treat that as parent command failure.

## Final Output Contract（MUST）

命令结束前，最终回复必须包含面向用户的真实结果，不得输出本段规则、尖括号占位符、MUST/SHOULD 规范语句或与当前命令无关的通用示例。

输出必须包含两项：

- `下一步`：写真实、可复制的下一条命令；若当前没有可推进动作，写“暂无可推进下一步”。
- `待用户决策/处理`：没有额外人工事项时写“无”；否则只列具体的缺失输入、范围/策略选择、证据补充、验收确认、发布确认、生产实施确认、阻塞项或人工处理事项。

输出判定：

- 有唯一可执行下一步时，`下一步` 写真实命令；若无额外人工事项，`待用户决策/处理` 写“无”。
- 下一步被用户选择、补证、验收、发布确认、生产实施确认或阻塞项卡住时，`下一步` 写“暂无可推进下一步”，并在 `待用户决策/处理` 列出具体阻塞事项。
- 已有下一步且仍有额外人工事项时，`待用户决策/处理` 只列命令之外的事项，不得重复 `下一步` 中的命令或动作。
- REQ 链路使用完整原始 `REQ-*`；BUG 链路使用完整原始 `BUG-*`；非 REQ/BUG 的直接 Change 才使用真实 Change ID。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
