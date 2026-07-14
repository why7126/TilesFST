---
note: workflow-sync — 2/3 Change 已 archive；1 applied；待人工 sign-off
sprint_id: sprint-007
title: Sprint 007 验收报告
status: planning
lifecycle_stage: change
created_at: 2026-07-11 23:39:00
updated_at: 2026-07-12 10:22:40
owner: product
source: /sprint-propose sprint-007
---

# Sprint 007 验收报告

## 最终验收摘要

当前正式纳入 `REQ-0036-clipboard-helper-best-practice-docs` / `add-clipboard-helper-best-practice-docs`、`REQ-0035-ai-usage-snapshot-sprint-close-exps` / `update-ai-usage-snapshot-sprint-close-exps` 与 `REQ-0037-auto-token-fact-source-for-workflow-commands` / `add-auto-token-fact-source-for-workflow-commands`。最终验收以 OpenSpec tasks、REQ acceptance、文档索引入口、AI usage snapshot actual/fallback 输出、工作流命令后置 hook 和敏感内容安全检查为准。

## 横切验收 Gate

本 Sprint 承接 Sprint 006 A-004。后续任何主题相关页面新增或改造，必须在对应 Change 的 `acceptance.md`、`test-plan.md` 或 `tasks.md` 中落地以下检查：

| Gate | 要求 | 状态 |
|---|---|---|
| 复用主题矩阵 | 引用 `REQ-0020-theme-comfort-refine` 的四主题矩阵，并说明新增页面适配哪些代表面 | pending |
| 截图检查 | 使用 Playwright 或等价方式保存关键视口与主题状态截图，或记录无法截图的原因 | pending |
| DOM 检查 | 覆盖分页、MetricCard、fixed toast、DS modal、弹窗宽度/滚动等适用 DOM 契约 | pending |
| N/A 说明 | 登录页、列表页、表单页、弹窗、媒体上传、`/design-system` 中不适用的项必须写明原因 | pending |

## 原始 AC 引用

- `issues/requirements/archive/REQ-0036-clipboard-helper-best-practice-docs/acceptance.md`
- `openspec/changes/archive/2026-07-11-add-clipboard-helper-best-practice-docs/tasks.md`
- `issues/requirements/review/REQ-0035-ai-usage-snapshot-sprint-close-exps/acceptance.md`
- `openspec/changes/update-ai-usage-snapshot-sprint-close-exps/tasks.md`
- `issues/requirements/review/REQ-0037-auto-token-fact-source-for-workflow-commands/acceptance.md`
- `openspec/changes/add-auto-token-fact-source-for-workflow-commands/tasks.md`
- `issues/requirements/archive/REQ-0020-theme-comfort-refine/acceptance.md`
- `docs/knowledge-base/retrospectives/sprint-006-retrospective.md` A-004

## 正式范围验收

| 类型 | 编号 | 状态 | 验收结论 |
|---|---|---|---|
| REQ | `REQ-0036-clipboard-helper-best-practice-docs` | done | 已完成 `/opsx-archive`；AC-001 ~ AC-019 已在需求验收记录中勾选 |
| Change | `add-clipboard-helper-best-practice-docs` | archived | 已归档到 `openspec/changes/archive/2026-07-11-add-clipboard-helper-best-practice-docs/` |
| REQ | `REQ-0035-ai-usage-snapshot-sprint-close-exps` | done | 已完成 `/opsx-archive`；物理迁入 archive 等待 Sprint close 后由 promote gate 处理 |
| Change | `update-ai-usage-snapshot-sprint-close-exps` | archived | 已归档到 `openspec/changes/archive/2026-07-11-update-ai-usage-snapshot-sprint-close-exps/` |
| REQ | `REQ-0037-auto-token-fact-source-for-workflow-commands` | in_sprint | 已纳入 Sprint；待 `/opsx-apply` 实现与验收 |
| Change | `add-auto-token-fact-source-for-workflow-commands` | proposed | 已创建 OpenSpec Change；待 `/opsx-apply` |

## REQ-0035 关键 AC 摘要

| AC | 验收点 | 当前状态 |
|---|---|---|
| AC-001 ~ AC-003 | Sprint close / archive 默认检查、生成或失败 warning | pass：`source-command-sprint-archive` 接入 Fact Sheet gate；CLI 缺失场景输出 recommended_action |
| AC-004 ~ AC-005 | `/sprint-exps` 使用 actual 或显式 estimated_fallback | pass：Fact Sheet 输出 `ai_usage_mode`；测试覆盖 actual、missing、stale fallback |
| AC-006 ~ AC-008 | snapshot 新鲜度、覆盖范围与状态摘要 | pass：校验 Sprint ID、generated_at、scope coverage、关键指标与 warning_count |
| AC-009 ~ AC-010 | 技能默认步骤与脱敏继承 | pass：技能已更新；脱敏测试覆盖 prompt、绝对路径、工具输出正文与 unsafe key |

## REQ-0037 关键 AC 摘要

| AC | 验收点 | 当前状态 |
|---|---|---|
| AC-001 ~ AC-002 | 每个 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 命令后自动构建或刷新 Token fact source | pending：待 `/opsx-apply` 实现统一 post-command hook |
| AC-003 ~ AC-004 | 命令级 fact source 记录 command family、command name、resource id、usage mode 与生成时间 | pending：待实现结构化输出与覆盖测试 |
| AC-005 ~ AC-006 | 失败降级不阻断主命令，并输出 recommended action | pending：待覆盖本地 session 缺失、过期与不可访问场景 |
| AC-007 ~ AC-008 | 继承 `REQ-0034` 脱敏边界，不写 prompt、系统指令、绝对路径或工具输出全文 | pending：待补充 redaction regression tests |
| AC-009 ~ AC-010 | Sprint snapshot 与 command run fact source 可被后续 `/sprint-exps`、review 和 opsx 流程复用 | pending：待验证消费链路 |

## 校验记录

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-07-11 23:39:00 | `/sprint-propose sprint-007` | planning 壳创建；正式 scope 为空；A-004 横切 gate 已写入 |
| 2026-07-12 00:03:31 | `/sprint-propose REQ-0036 sprint-007` | 纳入 Clipboard helper best-practice 文档需求与 OpenSpec Change；容量门禁 pass |
| 2026-07-12 00:07:29 | `/sprint-propose REQ-0035 sprint-007` | 纳入 AI usage snapshot close/exps 默认流程需求与 OpenSpec Change；Sprint 总估算 4/30 人天 |
| 2026-07-12 00:43:39 | `uv run pytest tests/test_ai_usage.py tests/test_generate_sprint_fact_sheet.py` | 13 passed |
| 2026-07-12 00:43:39 | `python scripts/extract-ai-usage.py --check-snapshot --sprint sprint-999 --json` | 输出 `snapshot_status: missing`、`usage_mode: estimated_fallback` 与 recommended_action |
| 2026-07-12 10:06:42 | `/sprint-propose REQ-0037 sprint-007` | 纳入工作流命令自动构建 Token 事实源需求与 OpenSpec Change；Sprint 总估算 9/30 人天 |
