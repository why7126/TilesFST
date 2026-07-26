---
sprint_id: sprint-012
title: Sprint 012 Release Note
status: planning
created_at: 2026-07-26 15:15:24
updated_at: 2026-07-26 15:40:00
---

# Sprint 012 Release Note

## 计划发布内容

| 类型 | ID | Change | 用户价值 |
|---|---|---|---|
| REQ | REQ-0071-request-snapshot-logging | update-request-snapshot-logging | API 请求日志补齐统一 Request Snapshot，提升日志审计、错误排障和跨端请求上下文还原能力 |
| REQ | REQ-0072-client-request-identity-standard | standardize-client-request-identity | 统一 Web 管理端、店主 Web 前台和微信小程序普通 API 请求的客户端类型和请求标识，提升跨端日志归因与排障能力 |
| REQ | REQ-0073-task-trace-parent-request-model | fix-task-trace-parent-request-model | 补强 Task Trace 与主请求、子请求、span 的关联模型，让任务链路可从主请求和 span 请求双向追溯 |
| REQ | REQ-0074-task-trace-coverage-expansion | update-task-trace-coverage-expansion | 将 Task Trace 从上传链路扩展到首批任务型业务接口，提升复杂保存、批量、异步和媒体处理排障效率 |
| REQ | REQ-0075-audit-log-task-trace-linking | link-audit-logs-to-task-trace | 补齐审计操作日志与 Task Trace 关联字段，让敏感操作可回到任务链路排障 |
| REQ | REQ-0076-observability-dashboard | add-observability-dashboard | 将日志审计升级为链路观测仪表，帮助管理员按请求、行为、审计与任务链路快速定位问题 |
| REQ | REQ-0075-audit-log-task-trace-linking | link-audit-logs-to-task-trace | 审计操作日志补齐任务链路关联字段，让 audit 类型日志能定位 Task Trace 并保持敏感审计写入点可追溯 |

## 影响范围

- 后端：请求日志 middleware、Snapshot builder、日志服务、日志仓储和脱敏策略。
- API：管理端日志详情响应新增或扩展 Request Snapshot 结构。
- 数据库：可能扩展 `request_logs.metadata` 或新增结构化字段，需保持 SQLite/MySQL 兼容。
- Web 管理端：日志详情抽屉展示 Snapshot 分组、JSON 辅助视图、空态和脱敏状态。
- 小程序 / 店主 Web：请求来源和 `client_type` 需与统一 Snapshot 字段兼容。
- 跨端请求身份：Web 管理端、店主 Web 前台和微信小程序请求封装注入统一 `client_type` 与客户端请求标识。
- 日志审计：展示并区分后端可信 `request_id`、客户端请求标识和客户端类型，长 ID 支持截断与复制反馈。
- 日志审计：补齐 `parent_request_id` 与 span `request_id`，支持从主请求进入 Task Trace、从 Task Trace span 回到请求日志。
- 日志审计：任务型接口首批接入 Task Trace，覆盖候选清单、统一 helper、同步/异步/批量 span 和复杂任务追踪标识反馈。
- 日志审计：audit 类型审计日志支持 `task_trace_id` 与 `task_type` 字段，敏感操作可在详情中定位任务链路。
- 链路观测：新增统一摘要、分布、排行、追踪 ID 查询和明细下钻，覆盖请求日志、行为事件、审计操作与 Task Trace。
- 日志审计：audit log 写入入口支持可选 `task_trace_id` 与 `task_type`，audit 类型日志详情支持任务链路联动。
- API / Orval：如新增请求头、响应头、日志字段或筛选参数，必须同步 OpenAPI 与生成客户端。
- 安全：以后端白名单、黑名单、脱敏和截断作为最终安全边界。

## 不包含

- 不接入外部 APM、链路追踪平台或日志全文检索。
- 不对历史日志做批量回填。
- 不统一接入 Nginx access log、容器 stdout 或数据库慢查询日志。
- 不保存完整原始请求体、完整响应体或未脱敏 Header。
- 不把前端脱敏作为最终安全边界。
- 不使用客户端字段覆盖后端可信 `request_id`。
- 不把客户端类型或客户端请求标识作为认证授权依据。
- 不新增真实用户画像、漏斗分析、实时大屏、复杂 BI 或外部分布式链路追踪平台。
- 不一次性覆盖所有历史接口，不新增导入导出业务能力，不保存完整请求体或响应体。
- 不为历史 Task Trace 回填 `parent_request_id` 或 span `request_id`，仅做新增数据写入与历史缺失字段兼容。
- 不回填历史审计日志任务字段。
- 不回填历史 audit log，不新增独立审计页面，不把任务字段作为权限判断依据。

## 发布前检查

- Request Snapshot 至少包含 method、path、route template、query 白名单摘要、body schema 摘要、业务资源标识、status code、error code、duration、操作者、客户端、环境、请求开始时间和响应结束时间。
- route template 获取失败时有明确降级状态。
- Authorization、Cookie、密码、Token、真实密钥、数据库 DSN、MinIO AccessKey/SecretKey、内部路径、原始文件名和原始敏感 body 不进入 Snapshot。
- 日志详情 API 返回结构化 Snapshot，并同步 OpenAPI / Orval。
- 三端普通 API 请求分别记录 `web_admin`、`web_catalog`、`wechat_miniapp` 客户端类型。
- 后端每次请求继续生成可信 `request_id`，并通过响应头返回 `x-request-id`。
- 客户端请求标识非法、缺失或超长时不得导致 500，也不得污染日志 metadata。
- 小程序 fallback base URL 重试的客户端请求标识复用或重建策略已文档化并覆盖测试。
- 日志审计列表或详情展示客户端类型、可信 `request_id` 与客户端请求标识，并保持 fixed toast、分页 DOM 和指标卡 DOM 一致。
- 管理端日志详情抽屉展示 Snapshot 分组，metadata 为空或 JSON 解析失败时页面不崩溃。
- 首批任务型接口清单至少评估保存 SKU、批量操作、导入导出、媒体处理、异步任务和复杂查询六类场景。
- 首批接入接口生成或透传同一个 `task_trace_id`，关键步骤写入可排序 span，失败、超时和部分成功能定位到失败节点。
- 管理端复杂任务反馈在成功、失败、处理中或部分成功状态展示或支持复制 `task_trace_id`，无 trace 时保持旧交互。
- Task Trace summary 能展示触发主请求 `parent_request_id`；有请求上下文的 span 能展示并定位对应 `request_id`。
- 日志详情可以从主请求 `request_id` 展示关联 Task Trace，也可以从 Task Trace span 回到对应请求日志。
- audit 类型审计日志写入支持 `task_trace_id` 与 `task_type`，无任务上下文时保持兼容。
- 链路观测仪表的摘要、分布、排行和明细入口与筛选条件保持同一统计口径。
- 审计日志写入入口支持可选 `task_trace_id` 与 `task_type`，无任务上下文保持兼容。
- 系统设置、品牌证书、媒体/上传、SKU、Banner 等敏感审计写入点完成接入评估。
- audit 类型日志存在 `task_trace_id` 时，日志详情展示 Task Trace 分组或等价入口。
- SQLite demo 与 MySQL production 的 `audit_logs.task_trace_id`、`task_type` 字段、索引和迁移路径保持一致。
- SQLite demo 与 MySQL production schema 或 metadata 兼容策略已同步文档。
- 后端 pytest、前端 Vitest、OpenSpec 校验通过。
