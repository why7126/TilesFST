---
name: "opsx-modify"
description: "验收返修：在 OpenSpec Change 已 opsx-apply、未 archive 前，根据验收反馈调整实现并同步文档、验证和 AI Usage"
---

# opsx-modify

Use this skill when the user asks `/opsx-modify <change-id|REQ-id|BUG-id> <修改内容>` or wants to adjust implementation after `/opsx-apply` during acceptance, before `/opsx-archive`.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，优先摘要复用，不重复全量读取。
- 返修定位先读验收反馈、`tasks.md`、`trace.md`、相关 acceptance 摘要；不要全量重读 Issue、Sprint、archive 或 generated 文件。
- 大 diff 先用 `git diff --stat` / `git diff --name-only`；只展开手写源码、测试和本次文档片段。
- 命令输出优先 `max_output_tokens <= 8000`；测试失败只展开失败用例、关键栈和相关片段。

## Prototype UI Modify Gate（MUST）

若验收反馈或目标 Change 涉及 `prototype/`、`prototype_refs`、`AC-PROTOTYPE-*`、UI Skeleton 或明确视觉参照，MUST 读取 `docs/standards/prototype-ui-acceptance.md`，并复核 UI Contract、Skeleton、1440px 视觉证据、computed style、Mock/API 边界和最终一致性。任何 UI 返修会使相关旧截图 stale，必须重新取证并更新 Change `trace.md` 或验收记录。

若验收反馈包含附件截图、标注图、原型截图或实际截图，返修前 MUST 建立“附件截图逐项视觉对照表”，逐项记录截图编号、页面/状态、期望表现、实际表现、偏差项、检查方式、处置结论和证据入口；证据不足时先补证，不得直接返修。

## Root-cause Evidence Gate（MUST）

涉及 BUG、回归失败、效果不如预期或原因判断的返修 MUST 遵守 `rules/root-cause-evidence.md`。无证据不得确认根因；证据不足时输出人工补证步骤，并将根因状态保持为 `unknown`、`hypothesis` 或 `probable`。

## 产品数据采集与链路观测返修门禁（MUST）

若返修影响 API、DB、日志审计、行为埋点、Task Trace、Web 请求封装、小程序请求封装或 App 请求封装，MUST 读取 `docs/standards/product-data-collection-observability.md`，复核并更新 `product_data_collection_observability` 的适用层级、N/A 原因和验证摘要。

返修完成前 SHOULD 运行 `python scripts/validate-product-data-observability-gates.py --change <change-id>`；若缺少声明或验收证据，先修复当前 Change 材料。

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

## Input

```text
/opsx-modify <change-id|REQ-id|BUG-id> <修改内容>
```

Examples:

```text
/opsx-modify add-login-page 登录按钮 hover 色和验收稿不一致，改成金色 token，并补截图验收说明
/opsx-modify REQ-0008-login-page 验收发现移动端标题溢出，修正响应式布局
```

## Scope

`/opsx-modify` 用于 **apply 后、archive 前** 的验收返修。

适用：

- 原验收项未满足。
- 原实现的 UI、API、数据、测试或文档存在偏差。
- 验收反馈仍属于当前 Change 的目标与边界。
- 需要补充二次验证证据和 AI Usage 统计。

不适用：

- 新增原需求未包含的功能。
- 改变新的 API / DB / 权限 / 部署 / 对象存储边界。
- 发现独立缺陷且影响范围超出当前 Change。
- 当前 Change 已 archive。

超出范围时 MUST stop，并建议走 `/req-capture`、`/bug-capture` 或新 OpenSpec Change。

## Stage Routing（MUST）

`/opsx-modify` MUST 先按阶段判断是否允许返修：

| 阶段 / 条件 | 处理 |
|---|---|
| Change 已 `/opsx-apply`、未 `/opsx-archive`，且反馈仍属于原需求、原 Change、原验收项或原能力边界 | 允许继续 `/opsx-modify` |
| Change 未归档，但反馈新增原需求未包含的功能，或改变 API / DB / 权限 / 部署 / 对象存储边界 | BLOCKED；建议 `/req-capture` 或 `/capture` |
| Change 未归档，但反馈是独立缺陷且影响范围超出当前 Change | BLOCKED；建议 `/bug-capture` 或 `/capture`，能确认父需求时关联 `related_requirement` |
| 原 REQ / Change 已归档，但所属 Sprint 未归档 | BLOCKED；不得返修原 Change；已交付能力偏差建议 `/bug-capture`，新增能力建议 `/req-capture` |
| 所属 Sprint 已归档 | BLOCKED；作为新生命周期输入处理；偏差走 `/bug-capture`，增强走 `/req-capture` |

若一个反馈同时包含当前 Change 内偏差与范围外事项，MUST 只处理范围内偏差；范围外事项输出标准 capture 文案，且明确“未自动创建 Issue”，除非用户在当前命令中明确授权自动 capture。

## Must Read

```text
AGENTS.md
openspec/project.md
rules/global.md
rules/coding.md
rules/testing.md
rules/security.md
rules/document-governance.md
rules/directory-structure.md
rules/requirement-management.md
rules/bug-management.md
rules/iterations-lifecycle.md
.agents/skills/workflow-sync/SKILL.md
```

Resolve target:

- If input is `REQ-*` / `BUG-*`, read its `trace.md` and resolve linked `openspec_changes[]`.
- If multiple active Changes match, ask user to choose.
- If target Change is archived, BLOCKED.

Then read focused snippets:

```text
openspec/changes/<change-id>/tasks.md
openspec/changes/<change-id>/trace.md（存在时）
openspec/changes/<change-id>/acceptance.md（存在时）
issues/requirements|bugs/**/<REQ-or-BUG>/acceptance.md
issues/requirements|bugs/**/<REQ-or-BUG>/trace.md
iterations/change|archive/<sprint>/acceptance-report.md
iterations/change|archive/<sprint>/sprint.yaml
```

Run preflight:

```bash
python scripts/sync-workflow-status.py --event opsx.modify --change <change-id> --sprint auto --dry-run
```

If sprint cannot resolve for a REQ/BUG-sourced Change, BLOCKED and ask to fix Sprint trace/scope first.

## Workflow

1. **Clarify Feedback**
   - Summarize the acceptance issue in 1-3 bullets.
   - Identify whether it is in-scope for the current Change.
   - Identify affected files and tests.

2. **Modify Implementation**
   - Make minimal scoped code changes.
   - Add or adjust tests when behavior changes.
   - Do not mark new feature scope as complete under this command.

3. **Update Documents**
   - Documentation update is a **MUST gate**, not optional bookkeeping. Before validation, decide whether the acceptance feedback changes any behavior, UI rule, validation rule, user-visible text, API/DB contract, release note, acceptance criterion, or archive-bound spec wording.
   - Update `openspec/changes/<change-id>/tasks.md` with a `## 验收返修记录` section if absent.
   - Update Change `trace.md` when present with feedback, adjustment, and validation summary.
   - If feedback changes or clarifies acceptance criteria, update the linked Issue `acceptance.md` or BUG acceptance/repro document, preserving frontmatter and refreshing `updated_at`.
   - If feedback changes or clarifies product behavior, UI/UE behavior, boundary, non-goal, validation strategy, or implementation decision while staying within the same Change scope, update the active Change docs such as `proposal.md`, `design.md`, `acceptance.md`, `test-plan.md`, or `implementation/` notes as applicable.
   - If feedback changes archive-bound capability wording, update `openspec/changes/<change-id>/specs/**/spec.md` delta so `/opsx-archive` will merge the corrected behavior into `openspec/specs/`.
   - If feedback changes Sprint-visible scope, acceptance evidence, release note, or user-visible behavior, update `iterations/change|archive/<sprint>/acceptance-report.md`, `sprint.md`, and/or `release-note.md` as applicable. Do not hand-edit workflow-sync marker blocks in `sprint.md`.
   - If feedback changes long-lived API, DB, deployment, compatibility, security, media, or product documentation, update the corresponding `docs/**` file required by `rules/document-governance.md`.
   - Update linked Issue `trace.md` through Workflow Sync rather than hand-editing marker blocks.
   - If docs/spec wording must change but capability boundary is unchanged, update the active Change docs; if boundary changes, BLOCKED and suggest `/req-capture`, `/bug-capture`, or a new OpenSpec Change.
   - Run focused documentation checks after edits: at minimum `openspec validate <change-id> --strict` when active Change docs/specs change, and `git diff --check -- <touched-docs>` for touched Markdown/spec files.

   Documentation decision matrix:

   | Feedback touches | MUST update |
   |---|---|
   | Acceptance wording, pass/fail criteria, or verification evidence | `openspec/changes/<change-id>/tasks.md`, Change `trace.md`, linked Issue `acceptance.md` if criteria changed, Sprint `acceptance-report.md` |
   | Product/UI behavior that should survive archive | Change `design.md` and/or `proposal.md`, `openspec/changes/<change-id>/specs/**/spec.md`, linked Issue `requirement.md` / BUG doc when applicable |
   | User-visible release behavior | Sprint `release-note.md` |
   | Sprint plan, scope notes, risk notes, or implementation notes | Sprint `sprint.md` outside workflow-sync marker blocks |
   | API, DB, deployment, environment, security, media, compatibility, or public product docs | Corresponding `docs/**` file per `rules/document-governance.md` |
   | Pure implementation-only bug with no behavior/spec/docs drift | Still update `tasks.md` + Change `trace.md`; explicitly record “无需更新其他文档” with reason |

4. **Validate**
   - Run focused tests/checks for touched areas.
   - Run broader checks when API / DB / UI / deployment / security boundary is touched.
   - Keep validation output summarized.

5. **Workflow Sync**

```bash
python scripts/sync-workflow-status.py --event opsx.modify --change <change-id> --sprint auto
```

- Exit code MUST be `0`.
- Print summary Workflow Sync Report.
- Do not hand-edit workflow-sync marker blocks.

6. **AI Usage（MUST）**

After successful workflow sync, run the post-command hook:

```bash
python scripts/extract-ai-usage.py \
  --post-command-hook \
  --workflow-event opsx.modify \
  --change <change-id> \
  --sprint <sprint-id|auto-resolved-id-if-known> \
  --json
```

Rules:

- If session JSONL is unavailable, report the compact `usage_mode: unavailable` summary and recommended action.
- Do not fail `/opsx-modify` solely because AI Usage session input is unavailable.
- Do not persist prompt text, raw session logs, tool outputs, secrets, `.env` content, cookies, tokens, or local absolute paths.

## Completion Output

Report:

```text
Change:
验收反馈:
调整内容:
文档更新:
文档未更新项与原因:
验证:
Workflow Sync:
AI Usage:
是否仍可 archive:
```

## Event

Workflow event: `opsx.modify`

This event means “验收返修已同步”，not first implementation and not archive.

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
