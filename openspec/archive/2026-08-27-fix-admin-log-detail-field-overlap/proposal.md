---
created_at: 2026-08-27 00:00:00
updated_at: 2026-08-27 00:00:00
---

# 修复管理端日志详情字段重叠

## 背景

`BUG-0145-admin-log-detail-field-overlap` 已确认：管理端日志审计详情抽屉中，`parent_behavior_event_id`、`client_request_id`、`behavior_trace_id`、`task_trace_id` 等长字段名会侵入右侧值列，造成字段名和值视觉重叠。

这些字段用于请求日志、行为链路和 Task Trace 排障定位。展示重叠不会改变日志采集事实，但会降低管理员、开发者和运维人员在日志详情中识别链路 ID 的效率，并增加人工误读风险。

## 变更内容

- 修复 Web 管理端日志详情抽屉字段行布局，使基础信息、请求信息和 Request Snapshot 中的长字段名和值不再重叠。
- 为长 snake_case 字段名和字段说明图标组合建立响应式溢出策略，覆盖桌面抽屉与窄宽度视口。
- 保留字段说明 tooltip 的 hover 与 focus 可访问性。
- 补充前端回归测试和视觉证据，覆盖长字段名和值同时存在的场景。
- 明确本次不修改后端 API、数据库、日志采集字段、OpenAPI、Orval、小程序、对象存储或 Docker Compose。

## 影响范围

- 影响 Web 管理端日志审计页面：`/admin/logs` 日志详情抽屉。
- 影响前端展示样式与测试：长字段名、字段说明图标、长 ID 值、Request Snapshot 分组。
- 不影响 API 响应结构、数据库结构、日志采集逻辑、行为事件、Task Trace 写入、请求封装、Orval 生成物、小程序端或对象存储。

## 产品数据采集与链路观测

```yaml
product_data_collection_observability:
  applicability: ui_display_only
  affected_layers:
    - web_admin_log_audit_detail_display
  not_affected_layers:
    - backend_api
    - request_logs_collection
    - usage_events_collection
    - task_traces
    - task_trace_spans
    - web_request_wrapper
    - miniapp_request_wrapper
    - database
  reason: 本 Change 只修复已有日志详情字段的布局可读性，不新增或修改链路字段、采集入口、请求头、响应 schema、持久化结构或保留策略。
  validation: 实现阶段通过前端测试、桌面截图和窄宽度截图证明长链路字段展示可读；API/DB/Orval 按 N/A 记录。
```

## 回滚计划

- 若修复造成日志详情抽屉布局回归，可回滚本 Change 中的前端样式和测试修改。
- 回滚不会影响后端日志采集、数据库数据、OpenAPI、Orval 或已持久化的日志记录。
- 回滚后 BUG-0145 的长字段重叠问题会重新出现，需要保留失败截图并重新进入 `/opsx-modify` 或后续修复。

