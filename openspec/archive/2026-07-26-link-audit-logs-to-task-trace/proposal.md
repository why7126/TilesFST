## Why

REQ-0075 已批准补齐审计操作日志与 Task Trace 的关联字段。当前 `audit_logs` 表结构和日志查询能力已具备 `task_trace_id` / `task_type` 基础，但审计写入接口尚未稳定接收和持久化任务上下文，导致系统设置、品牌证书、媒体上传等敏感操作无法从 audit log 串联回主请求和任务时间线。

## What Changes

- 扩展审计日志写入契约：`AuditLogRepository.insert()` 或等价写入接口支持可选 `task_trace_id` 与 `task_type`。
- 让任务型敏感审计操作复用当前请求或 Task Trace 上下文，非任务型审计操作保持兼容为空。
- 明确首批需要评估和接入的审计写入点：系统设置、品牌证书、媒体/上传、SKU、Banner 等管理端敏感操作。
- 保持日志审计列表与详情对 `audit` 类型日志的 Task Trace 展示一致性，避免重复建设独立页面。
- 确认 SQLite / MySQL `audit_logs.task_trace_id`、`audit_logs.task_type` schema 一致，并同步 OpenAPI、Orval、数据库文档、错误码文档和测试。
- 将 REQ-0075 的 `admin-list` 横切 AC 纳入实现验收：分页 DOM、指标卡 DOM、fixed toast、无 `window.confirm`、日志页 smoke matrix。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `product-usage-logging`: 补齐 audit log 与 Task Trace 的写入、查询、详情展示、契约同步和横切 UI 验收要求。

## Impact

- 后端：审计仓储、日志服务、系统设置服务、品牌证书服务、媒体/上传相关管理服务，以及其他写入 `audit_logs` 的敏感操作位置。
- API：如日志列表/详情响应尚未包含 audit 类型任务摘要，需要同步 response schema、OpenAPI 和 Orval 生成物。
- 数据库：确认 SQLite demo 与 MySQL production `audit_logs` 字段和索引一致；如不一致，补 migration、schema 和数据库文档。
- Web 管理端：复用现有 `/admin/logs` 列表和详情抽屉，展示 audit 类型日志的任务摘要和 Task Trace 分组。
- 安全：审计 metadata 脱敏、权限边界、禁止前端 task 字段作为权限依据。
- 测试：后端 pytest、前端 Vitest、日志审计 smoke、OpenAPI/Orval 和 schema drift 验证。
