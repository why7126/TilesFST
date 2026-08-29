---
change_id: add-log-audit-behavior-trace-model
source_requirement: REQ-0124-log-audit-behavior-trace-model
sprint: sprint-026
acceptance_status: pending
created_at: 2026-08-25 22:47:46
updated_at: 2026-08-27 23:10:25
---

# 验收记录

## 验收范围

- `usage_events` 行为链路字段。
- `request_logs` 行为来源字段。
- 前端请求透传 `behavior_trace_id` / `behavior_event_id`。
- 直接 API 调用空行为链路兼容。
- `task_traces.parent_request_id` 与 `task_trace_spans` 流程节点联动。
- 管理端日志审计按 `behavior_trace_id`、`request_id`、`task_trace_id` 查询。
- DB / API / Orval / Web / 测试 / 文档同步。

## 产品数据采集与链路观测门禁

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - usage_events
    - request_logs
    - task_traces
    - task_trace_spans
    - backend_api
    - web_admin
    - web_request_wrapper
    - database
  na_reason:
    web_catalog: 本期不改店主端页面或店主端请求封装。
    wechat_miniapp: 本期不改小程序页面或小程序请求封装。
    app: 本项目当前无 App 代码接入范围。
    object_storage: 本期不改对象存储 bucket、key 或上传存储拓扑。
  validation:
    result: pass
    summary: 已对照 `docs/standards/product-data-collection-observability.md` 完成行为事件、请求日志、任务链路、流程节点、直接 API 兼容、脱敏、API / DB / Orval 和 Web 管理端请求封装验证。
```

## 验收结果回填

```yaml
acceptance_status: pending
accepted_at: null
accepted_by: null
evidence:
  - command: uv run pytest src/backend/tests/test_product_usage_logging.py tests/test_mysql_schema_drift.py tests/test_mysql_migrations.py
    result: pass
    summary: 32 passed，覆盖 behavior_trace_id / behavior_event_id 入库、直接 API 空行为链路、Task Trace parent_request_id 与 span 行为链路、SQLite/MySQL 字段索引与迁移幂等。
  - command: corepack pnpm test -- LogAuditPage usage-tracking auth-api
    result: pass
    summary: 62 test files / 364 tests passed，覆盖前端行为 ID 生成、axios 请求头透传、日志审计 behavior_trace_id 筛选/展示/复制和 admin-list DOM 契约。
  - command: bash scripts/generate-openapi-client.sh
    result: pass
    summary: OpenAPI 与 Orval generated.ts 已同步新增查询参数和响应字段。
failed_items: []
source_event: opsx.apply
notes: 待验收；由 opsx.apply 标记，后续 archive 时回填最终验收结论。
```
