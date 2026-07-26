---
requirement_id: REQ-0075-audit-log-task-trace-linking
title: 审计操作日志补齐任务链路关联字段 - 验收标准
status: pending_review
owner: product
created_at: 2026-07-26 13:02:25
updated_at: 2026-07-26 13:02:25
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags:
  - admin-list
---

# 验收标准

## 功能 AC

- [ ] AC-001 `AuditLogRepository.insert()` 或等价审计写入接口 MUST 支持可选 `task_trace_id` 与 `task_type` 参数。
- [ ] AC-002 当调用方提供合法任务上下文时，系统 MUST 将 `task_trace_id` 与 `task_type` 持久化到 `audit_logs`。
- [ ] AC-003 当审计操作无任务上下文时，`task_trace_id` 与 `task_type` MAY 为空，且原有审计日志写入、查询和详情展示不回归。
- [ ] AC-004 首批敏感操作接入清单 MUST 在 OpenSpec design 或任务清单中明确，至少评估系统设置、品牌证书、媒体/上传、SKU、Banner 等写审计日志位置。
- [ ] AC-005 任务型审计操作 SHOULD 复用当前请求或任务上下文中的 `task_trace_id`，不得为同一任务重复生成互不关联的任务标识。
- [ ] AC-006 同一主请求触发多条审计操作时，相关审计日志 SHOULD 共享同一个 `task_trace_id`，并通过资源字段或 metadata 区分操作对象。
- [ ] AC-007 管理端日志审计列表 MUST 能对 `audit` 类型日志展示 `task_trace_id`、`task_type` 或等价任务摘要字段。
- [ ] AC-008 日志审计筛选 MUST 支持通过 `task_trace_id` 查询关联日志，可复用“路径 / request_id / task_trace_id”关键字筛选或新增独立筛选项。
- [ ] AC-009 审计日志详情中若存在 `task_trace_id`，MUST 展示关联任务链路入口、任务类型、任务状态、关键节点或时间线摘要。
- [ ] AC-010 审计日志详情中若不存在 `task_trace_id`，MUST 保持现有详情展示，不出现空时间线错误、异常布局或前端报错。
- [ ] AC-011 审计日志中的 `task_trace_id` MUST 与 `task_traces`、request logs、usage events 使用同一追踪标识语义。
- [ ] AC-012 `task_type` 命名 SHOULD 与 Task Trace 任务类型枚举保持一致，并在实现设计中说明新增或复用的枚举值。
- [ ] AC-013 SQLite demo 与生产 MySQL 的 `audit_logs` MUST 均存在 `task_trace_id` 与 `task_type` 字段；若发现不一致，MUST 同步 schema、迁移、数据库文档和测试。
- [ ] AC-014 `task_trace_id` 查询路径 MUST 使用结构化字段和索引友好条件，不得以 metadata 无界模糊扫描作为主查询路径。
- [ ] AC-015 若新增或调整日志列表/详情 API 字段，MUST 同步 OpenAPI、Orval、`docs/03-api-index.md`、错误码文档和后端/前端测试。
- [ ] AC-016 日志审计查询入口 MUST 继续仅允许系统管理员访问，非授权用户直链访问 MUST 返回 403 或管理端无权限页。
- [ ] AC-017 审计 metadata MUST 过滤 Authorization、Cookie、Token、密码、AccessKey、SecretKey、数据库 DSN、`.env` 内容、内部绝对路径和真实客户数据。
- [ ] AC-018 前端传入的 `task_trace_id`、`task_type`、resource 信息 MUST NOT 作为权限判断依据。
- [ ] AC-019 审计写入失败或 Task Trace 关联失败 MUST 不泄露内部路径、堆栈、对象存储凭证或未脱敏 metadata。
- [ ] AC-020 本需求 MUST 不创建独立审计页面，不要求历史审计数据回填；全量任务型接口覆盖由 `REQ-0074` 承接。
- [ ] AC-021 原型策略 MUST 至少提供日志审计列表和详情抽屉中 Task Trace 分组的 HTML/context；PNG Golden Reference 可在后续设计确认后导出。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 管理端列表页一致性复发类缺陷。

- [ ] AC-XCUT-001 日志审计列表新增 `task_trace_id` 展示或筛选后，分页 DOM MUST 对齐用户管理基准：左侧 `.page-summary`，右侧 `.page-right` 页码 + 每页条数。
- [ ] AC-XCUT-002 日志审计指标摘要如因任务链路新增或调整，MUST 使用 `.metric-label` / `.metric-value` / `.metric-desc` 结构，不得只复用外层卡片后用裸 `strong` / `span` 承载数值。
- [ ] AC-XCUT-003 查询、复制 `task_trace_id` / `request_id`、打开详情或加载失败反馈 MUST 使用 fixed toast 或等价固定层，不得造成页面头部、筛选区或表格纵向位移。
- [ ] AC-XCUT-004 N/A — 本需求首期日志审计列表只查询和查看任务链路，不包含启停、删除、重置等危险状态变更；若后续新增清理、删除、导出等危险操作，MUST 使用 DS confirm modal。
- [ ] AC-XCUT-005 日志审计列表与详情实现 MUST 不调用 `window.confirm`；本期无确认操作时以静态检查或代码 review 说明 N/A。
- [ ] AC-XCUT-006 日志审计页在 1440x1024 与移动端管理端视口下 MUST 完成列表/详情 smoke，覆盖分页、筛选、复制反馈和详情抽屉任务分组；Sprint 010 复盘指出管理端 UI 细节需要共享 smoke matrix 前置。
