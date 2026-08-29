---
change_id: add-log-audit-behavior-trace-model
source_requirement: REQ-0124-log-audit-behavior-trace-model
sprint: sprint-026
status: applied
lifecycle_stage: change
created_at: 2026-08-25 22:47:46
updated_at: 2026-08-27 23:10:25
---

# Change 追踪

## 基本信息

```yaml
change_id: add-log-audit-behavior-trace-model
source_requirement: REQ-0124-log-audit-behavior-trace-model
sprint: sprint-026
status: applied
type: add
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: true
  storage: false
  api: true
capabilities:
  new: []
  modified:
    - product-usage-logging
    - database
    - web-client
cross_cutting_tags:
  - admin-list
prototype:
  has_prototype_dir: true
  html: false
  png: false
  context: true
ui_contract: true
tasks_total: 28
tasks_completed: 28
```

## Readiness

```yaml
requirement_readiness: ready
review_gate: pass
sprint_inclusion_gate: pass
change_type: add
conflict_report:
  result: no_conflict
  reason: 仅存在 prototype/web/context.md，要求复用既有日志审计页；与 acceptance、ui-design 和既有 specs 一致。
next: /opsx-archive REQ-0124-log-audit-behavior-trace-model
```

## Cross-Cutting Apply Gate

```yaml
checked_at: 2026-08-25 23:20:00
tags:
  - admin-list
references:
  - docs/standards/prototype-ui-acceptance.md
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
prototype:
  html: false
  png: false
  context: true
ui_scope: reuse_existing_admin_logs_page
admin_filter_dropdown_gate:
  result: pass
  reason: 新增 `behavior_trace_id` 为文本输入；既有 Select/Combobox 继续复用共享筛选控件。
admin_list_gate:
  result: pass
  evidence: Vitest 覆盖后端真实分页 DOM、长 ID 截断、fixed toast、粘性操作列、筛选重置和敏感信息不展示。
visual_evidence:
  result: equivalent_test_evidence
  reason: 本次未新建页面或复杂视觉结构，仅在既有日志审计页增加一个文本筛选项和一列表格字段；以 DOM/契约测试覆盖 1440px 管理端列表关键结构。
verdict: PROCEED
```

## 实现验证

```yaml
implemented_at: 2026-08-25 23:20:00
checks:
  - command: bash scripts/generate-openapi-client.sh
    result: pass
    summary: Orval v8.17.0 converted tileApi，已同步 openapi.json 与 generated.ts。
  - command: uv run pytest src/backend/tests/test_product_usage_logging.py tests/test_mysql_schema_drift.py tests/test_mysql_migrations.py
    result: pass
    summary: 32 passed，59 warnings；覆盖行为链路字段、直接 API 空链路、任务 parent_request_id / spans、脱敏和 SQLite/MySQL 迁移。
  - command: corepack pnpm test -- LogAuditPage usage-tracking auth-api
    result: pass
    summary: 62 test files / 364 tests passed；覆盖前端行为 ID 生成、axios 透传、日志审计筛选、详情展示、复制 fixed toast 和 admin-list DOM 契约。
docs:
  - docs/03-api-index.md
  - docs/04-database-design.md
api: OpenAPI / Orval 已同步。
database: SQLite schema / migration 与 MySQL baseline / compat migration 已同步。
```

## Product Data Collection Observability Gate

```yaml
product_data_collection_observability:
  status: applicable
  standard: docs/standards/product-data-collection-observability.md
  affected_layers:
    - usage_events
    - request_logs
    - task_traces
    - task_trace_spans
    - backend_api
    - web_admin
    - web_request_wrapper
    - database
  na_layers:
    web_catalog: 本期不改店主端页面或店主端请求封装。
    wechat_miniapp: 本期不改小程序页面或小程序请求封装。
    app: 本项目当前无 App 代码接入范围。
    object_storage: 本期不改对象存储 bucket、key 或上传存储拓扑。
  validation:
    - `usage_events` 已新增 `behavior_trace_id` / `behavior_event_id`，并同步 SQLite / MySQL schema、迁移、索引和数据库设计文档。
    - `request_logs` 已新增 `behavior_trace_id` / `parent_behavior_event_id`，直接 API 调用和历史日志允许空行为来源。
    - 任务类请求继续通过 `task_traces.parent_request_id` 关联 `request_logs.request_id`，流程节点继续由 `task_trace_spans` 展示为“流程节点”。
    - Web 管理端请求封装已透传 `behavior_trace_id` / `behavior_event_id`，日志审计页支持 `behavior_trace_id`、`request_id`、`task_trace_id` 查询。
    - 后端脱敏、长度截断、非法链路字段和敏感字段过滤已有后端测试覆盖。
    - `bash scripts/generate-openapi-client.sh` 已同步 OpenAPI / Orval。
    - `uv run pytest src/backend/tests/test_product_usage_logging.py tests/test_mysql_schema_drift.py tests/test_mysql_migrations.py` 通过。
    - `corepack pnpm test -- LogAuditPage usage-tracking auth-api` 通过。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-27 23:10:25 | `/opsx-archive` | 归档前补齐 `product_data_collection_observability` 硬门禁声明，记录适用层级、N/A 原因和验证摘要。 |
| 2026-08-25 22:47:46 | `/req-opsx` | 根据 REQ-0124 创建 OpenSpec Change，生成 proposal、design、spec delta、tasks、test-plan、acceptance 和 trace |
| 2026-08-25 23:20:00 | `/opsx-apply` | 完成日志审计行为链路模型落地，补齐 DB/API/Web/Orval/文档/测试，并记录 admin-list 横切验收证据 |
