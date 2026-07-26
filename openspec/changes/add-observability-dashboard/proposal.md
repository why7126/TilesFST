## Why

现有日志审计能力已覆盖日志列表、详情抽屉、基础指标和 Task Trace 时间线，但排障仍需要人工在请求、行为、审计和任务节点之间来回查找。随着上传、后台任务、多端行为事件持续接入日志体系，管理端需要一个以链路健康和异常下钻为核心的观测仪表。

## What Changes

- 在管理端日志审计入口增加“链路观测”仪表，展示请求、行为、审计和 Task Trace 的统一摘要。
- 增加任务成功率、任务耗时分布、慢任务排行、最慢 span 排行、接口错误率、慢请求排行、失败原因分布和客户端分布。
- 支持按时间范围、日志类型、客户端、任务类型、接口路径、状态 / 结果和追踪 ID 筛选观测数据。
- 支持通过 `request_id` / `task_trace_id` 一键追踪到日志详情、Task Trace 时间线或相关记录集合。
- 增加或扩展管理端日志聚合查询 API，并同步 OpenAPI、Orval、API 文档、错误码和测试。
- 补充管理端页面横切验收，覆盖指标卡 DOM、分页结构、fixed toast、无 `window.confirm` 和管理端 UI smoke。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `product-usage-logging`: 扩展管理端日志查询 API、日志审计页面、Task Trace 查询和日志契约同步要求，新增链路观测仪表及聚合指标能力。

## Impact

- Backend: 管理端日志聚合查询、Task Trace 聚合、请求/行为/审计关联查询、权限和脱敏。
- Web admin: `/admin/logs` 或等价管理端入口的链路观测模式、筛选、指标、排行、追踪和详情跳转。
- API: 可能新增 `/api/v1/admin/logs/observability` 或扩展现有日志 summary；必须使用统一响应 envelope。
- Database: 首选复用现有 request logs、usage events、audit logs 和 Task Trace 存储；如需新增索引或聚合字段，必须兼容 SQLite demo 与 MySQL production。
- Orval/docs/tests: API 变更必须同步 OpenAPI、Orval、`docs/03-api-index.md`、错误码文档和后端/前端测试。
- Storage/miniapp: 不直接变更对象存储或小程序代码，但客户端分布与行为事件统计需要兼容 `miniapp` 来源。
