---
req_id: REQ-0075-audit-log-task-trace-linking
status: done
created_at: 2026-07-26 12:49:31
updated_at: 2026-07-26 17:09:06
recorded_by: product
source: 用户反馈
priority_hint: P2
parent_requirement: REQ-0024-product-usage-logging
captured_via: capture
classification_rationale: 当前描述要求补齐审计日志与 Task Trace 的写入和展示能力，属于审计链路增强需求。
---

# 一句话

审计操作日志需要写入并展示 `task_trace_id` 与 `task_type`，与主请求和任务链路统一关联。

# 原始描述

采纳优化建议：补齐 `AuditLogRepository.insert()` 对 `task_trace_id`、`task_type` 的支持，敏感操作可以和主请求/任务链路联动。

# 背景与关联

- `audit_logs` 表结构已预留 `task_trace_id` 与 `task_type`。
- 统一日志查询已经 left join `task_traces`。
- 当前审计仓储 insert 方法还没有接收和写入这两个字段，导致敏感操作无法完整串联任务链路。

# 影响范围

- 后端：审计仓储、系统设置服务、品牌证书管理服务，以及其他敏感操作写审计日志的位置。
- 数据库：原则上复用既有字段，确认 SQLite/MySQL schema 与迁移一致。
- 管理端：日志审计详情中审计类型日志可展示 Task Trace。
- 安全：审计 metadata 仍需脱敏。

# 初步需求要点

- 审计日志写入接口支持 `task_trace_id` 与 `task_type`。
- 触发任务型处理的审计操作应将 Task Trace 信息写入审计日志。
- 非任务型审计操作可保持为空，不影响兼容性。
- 日志审计列表与详情对 audit 类型日志展示一致的 Task Trace 信息。

# 待澄清

- [ ] 哪些审计操作首批需要关联 Task Trace。
- [ ] 系统设置修改是否需要作为任务型 trace，还是只保留普通审计。
- [ ] 审计 metadata 是否需要统一安全清洗函数。

# 建议验收要点

- [ ] 审计日志写入方法可接收并持久化 `task_trace_id`、`task_type`。
- [ ] audit 类型日志在日志审计页可按 `task_trace_id` 查询。
- [ ] audit 日志详情能展示关联 Task Trace 时间线。
- [ ] 无 Task Trace 的审计操作保持原有行为。

# 分类说明（/capture）

该条目是审计链路增强，属于 REQ。
