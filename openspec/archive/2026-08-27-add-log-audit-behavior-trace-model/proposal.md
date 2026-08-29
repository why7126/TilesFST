---
change_id: add-log-audit-behavior-trace-model
source_requirement: REQ-0124-log-audit-behavior-trace-model
sprint: sprint-026
created_at: 2026-08-25 22:47:46
updated_at: 2026-08-25 22:47:46
---

# 日志审计补齐行为链路与任务链路采集模型

## 背景

当前平台已经具备 usage events、request logs、Request Snapshot、Task Trace 和管理端日志审计基础能力，也已经通过 `task_traces.parent_request_id` 建立任务与来源请求的关联。但一次用户界面行为可能触发一个或多个 API 请求，仅靠 `request_id` 无法表达“一次行为引发了哪些请求”。同时，直接 API 调用、外部系统调用或脚本调用没有界面行为上下文，仍需要从 `request_id` 独立追踪到任务链路和流程节点。

本 Change 补齐行为链路采集模型，让日志审计同时支持界面触发和直接 API 调用两种入口，并将行为事件、接口请求、任务链路和任务流程节点串联为一致的排障、审计和产品分析事实源。

## 变更内容

- `usage_events` 增加 `behavior_trace_id` 与 `behavior_event_id`，区分一次行为链路和单条行为事件。
- `request_logs` 增加 `behavior_trace_id` 与 `parent_behavior_event_id`，记录请求来源行为；直接 API 调用允许两者为空。
- 前端请求封装在界面行为触发的请求中透传 `behavior_trace_id` / `behavior_event_id`，但后端仍以服务端生成的 `request_id` 作为可信请求 ID。
- 任务类请求继续通过 `task_traces.parent_request_id` 关联 `request_logs.request_id`；任务流程节点继续由 `task_trace_spans` 承载，管理端中文展示为“流程节点”。
- 管理端日志审计支持按 `behavior_trace_id`、`request_id`、`task_trace_id` 查询，并在详情中展示行为事件、API 请求、任务链路和流程节点的关系。
- 同步 SQLite / MySQL schema、迁移、数据库文档、OpenAPI、Orval、后端测试和前端测试。
- 保持敏感字段脱敏，不保存完整请求体、完整响应体、Header、Cookie、Authorization、Token、真实密钥、本机绝对路径或未授权对象存储 key。

## 能力范围

### 新增能力

无全新 capability。

### 修改能力

- `product-usage-logging`：扩展行为事件、请求日志、日志审计、Task Trace 和链路观测模型。
- `database`：补充日志链路字段在 SQLite / MySQL 的一致存储、索引和迁移要求。
- `web-client`：扩展管理端日志审计页的链路查询、详情展示和 admin-list 横切约束。

## 影响

- 后端：影响请求日志中间件、usage events 接收、日志审计查询、Task Trace 写入和脱敏策略。
- API：影响日志审计查询参数、详情响应、usage event 接收字段和请求日志 schema；必须同步 OpenAPI 与 Orval。
- 数据库：影响 `usage_events`、`request_logs`、`task_traces`、`task_trace_spans` 相关字段、索引、迁移和数据库文档。
- Web 管理端：影响前端请求封装、行为事件采集和 `/admin/logs` 查询/详情展示。
- 管理端 UI：命中 `admin-list` 横切门禁，必须保持后端真实分页、长字段截断、统一筛选控件、fixed toast、敏感字段脱敏和权限边界。
- 小程序 / 店主 Web：本期不建设独立分析页；如共享请求封装或埋点字段可复用，必须保持主流程不受埋点失败影响。
- 对象存储 / Docker Compose：不涉及存储 Bucket、key、Nginx 或 Compose 拓扑变更。
