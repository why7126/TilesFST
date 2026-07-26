## Why

REQ-0069 已批准建立通用 Task Trace 能力，用于把一次用户可感知的业务任务与多个请求、行为事件、审计操作和后端节点串联起来。BUG-0085 暴露了当前上传链路只靠 request_id 和单条日志难以拆解 99% 卡顿耗时的问题。

现有 `product-usage-logging` 已提供请求日志、使用事件和管理端日志审计入口，但缺少以 `task_trace_id` 为中心的任务时间线、节点耗时和跨日志关联能力。该变更将在现有日志审计基础上增加任务链路追踪，并以图片、视频、文件上传作为首批落地场景。

## What Changes

- 新增通用 `task_trace_id` / `task_type` / task span 模型，支持一次任务关联多个 `request_id`、usage event 和 audit log。
- 扩展管理端日志审计列表与详情：支持按 `task_trace_id` 查询，并在详情抽屉展示任务时间线、节点耗时、状态、错误码和关联请求。
- 首批覆盖图片、视频、文件上传，记录前端、后端、对象存储、数据库和后处理节点，支撑 BUG-0085 的 99% 耗时分析。
- 明确安全脱敏、权限、日志保留、SQLite/MySQL schema、OpenAPI/Orval/docs/tests 同步要求。
- 保留复杂 APM、外部日志系统、完整请求/响应体保存、视频转码增强为 Out of Scope。

## Capabilities

### New Capabilities

无。该能力作为既有日志审计与对象存储能力的扩展，不新增顶层 capability。

### Modified Capabilities

- `product-usage-logging`: 增加 Task Trace 任务链路追踪、审计日志查询与详情时间线能力。
- `object-storage`: 增加图片、视频、文件上传首批 Task Trace span 记录和 Docker Web 上传边界验证要求。

## Impact

- 后端：可能新增 `task_traces` / `task_trace_spans` 表或扩展 `request_logs` / `usage_events` / `audit_logs` 字段；需要 Repository / Service 层记录任务节点。
- API：`GET /api/v1/admin/logs` 与 `GET /api/v1/admin/logs/{id}` 可能新增 `task_trace_id`、`task_type`、`task_status`、`task_duration_ms`、`task_trace` / `task_spans` 字段；如新增任务事件接口，需同步契约。
- Web 管理端：日志审计列表筛选和详情抽屉需展示 Task Trace；上传组件需携带或接收任务上下文并记录前端节点。
- 对象存储：上传链路需记录对象存储写入 span，继续遵守后端授权、MinIO 单桶、禁止前端直连未授权对象存储。
- 数据库：SQLite demo 与 MySQL production schema 必须兼容并建立 `task_trace_id` / `task_type` / `created_at` 等索引。
- 测试：补充后端 pytest、前端 Vitest、OpenAPI/Orval 生成验证和 Docker `http://localhost:3000` 上传边界 smoke。

## Rollback Plan

1. 回滚 UI 展示时保留现有日志审计列表和详情能力，不删除既有 request log / usage event / audit log。
2. 若 Task Trace 持久化出现异常，可临时关闭任务 span 写入，保留 request_id 日志和上传主流程。
3. 若新增 schema 影响生产，回滚前端 task trace 查询入口，并保留新增表/字段为兼容空字段，避免破坏历史日志读取。
4. 回滚后必须重新验证图片、视频、文件上传仍经后端授权对象存储适配层写入，且日志审计基础查询不回归。
