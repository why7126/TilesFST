---
change_id: add-auto-token-fact-source-for-workflow-commands
requirement_id: REQ-0037-auto-token-fact-source-for-workflow-commands
status: applied
created_at: 2026-07-12 10:02:48
updated_at: 2026-07-12 10:35:00
---

# Change Trace

## 来源

| 类型 | ID | 路径 |
|---|---|---|
| REQ | REQ-0037-auto-token-fact-source-for-workflow-commands | `issues/requirements/archive/REQ-0037-auto-token-fact-source-for-workflow-commands/` |
| Parent REQ | REQ-0034-ai-token-usage-observability | `issues/requirements/archive/REQ-0034-ai-token-usage-observability/` |
| Related REQ | REQ-0035-ai-usage-snapshot-sprint-close-exps | `issues/requirements/archive/REQ-0035-ai-usage-snapshot-sprint-close-exps/` |

## 影响面

| Area | Impact |
|---|---|
| Backend API | No product API changes |
| Database | No schema changes |
| Web / Admin / Miniapp | No UI changes |
| Agent workflow | Adds post-command AI usage fact source hook requirements |
| Scripts | Added unified post-command hook options to `scripts/extract-ai-usage.py` / `scripts/ai_usage.py` |
| Data | Uses existing `data/ai-usage/` fact source |
| Docs / Skills | Shared Workflow Sync skill and AI usage docs describe automatic hook behavior |

## Knowledge Base

- `docs/knowledge-base/retrospectives/sprint-006-retrospective.md`：记录 AI usage snapshot 缺失导致 `/sprint-exps` 只能 estimated fallback，并提出纳入默认流程的行动项。

## 条件通过项追踪

| 条件 | 后续处理 |
|---|---|
| design.md MUST 明确统一 post-command hook 与 Workflow Sync 职责边界 | 已在 design.md D2 说明 Workflow Sync 不直接持久化 session 内容 |
| 自动构建失败默认不阻断主命令 | 已在 design.md D4 与 delta spec failure fallback 场景中说明 |
| 复用 REQ-0034 脱敏边界 | 已在 design.md、delta spec 和 tasks 中列入 |
| 避免每个 skill 复制长逻辑 | 已在 design.md D1 与 tasks 3.x 中列入 |
| 实现后验证 skill 未复制 session 解析逻辑 | `rg` 检查仅命中安全边界说明，无解析逻辑复制 |

## 验证计划

| Command | Purpose | Status |
|---|---|---|
| `openspec validate add-auto-token-fact-source-for-workflow-commands --strict` | Validate Change spec structure | passed |
| `python scripts/sync-workflow-status.py --event req.opsx --req REQ-0037-auto-token-fact-source-for-workflow-commands --change add-auto-token-fact-source-for-workflow-commands --sprint auto` | Sync REQ trace and registry | passed |
| `python scripts/sync-workflow-status.py --event sprint.propose --sprint sprint-007` | Sync Sprint scope, REQ trace and registry after inclusion | passed |
| `uv run pytest tests/test_ai_usage.py tests/test_generate_sprint_fact_sheet.py` | Validate AI usage hook, fallback, idempotency and Fact Sheet behavior | passed |
| `python scripts/validate-agent-context-budget.py` | Validate command-skill context budget guardrails | passed |
| `python scripts/extract-ai-usage.py --post-command-hook --workflow-event req.capture --req REQ-9999-demo --json` | Validate unavailable session summary does not fail parent command | passed |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-12 10:35:00 | /opsx-apply | 实现统一 AI usage post-command hook、共享技能接入说明、AI usage README、测试与校验 |
| 2026-07-12 10:06:42 | /sprint-propose | 纳入 `sprint-007` 正式范围；REQ trace iteration 已更新 |
| 2026-07-12 10:02:48 | /req-opsx | 创建 OpenSpec Change proposal/design/spec/tasks/trace |
