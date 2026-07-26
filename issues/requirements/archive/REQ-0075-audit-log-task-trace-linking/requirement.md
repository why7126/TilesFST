---
requirement_id: REQ-0075-audit-log-task-trace-linking
title: 审计操作日志补齐任务链路关联字段
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P2
parent_requirement: REQ-0024-product-usage-logging
created_at: 2026-07-26 12:57:58
updated_at: 2026-07-26 17:09:06
---

# REQ-0075 审计操作日志补齐任务链路关联字段

## 1. 需求背景

平台已经具备日志审计与 Task Trace 的基础能力：`audit_logs` 表结构预留了 `task_trace_id` 与 `task_type`，统一日志查询也已能通过 `task_trace_id` 与 `task_traces` 建立关联。但当前审计日志写入链路仍存在缺口：`AuditLogRepository.insert()` 尚未接收并持久化任务链路字段，导致敏感操作、系统设置变更、品牌证书维护等审计事件无法稳定串联到用户发起的主请求或后台任务时间线。

该需求聚焦“审计操作日志与 Task Trace 关联”这一补齐项，作为 `REQ-0024-product-usage-logging` 的增强需求，并与 `REQ-0069-upload-observability-trace-logs`、`REQ-0073-task-trace-parent-request-model` 保持模型一致。目标是让审计日志既能保留现有单条操作留痕，又能在存在任务上下文时进入完整任务链路。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 系统管理员 | 在审计日志中直接看到敏感操作关联的 `task_trace_id`、任务类型和任务时间线。 |
| 安全 / 审计负责人 | 追溯关键操作由谁发起、关联了哪个主请求、影响了哪些资源，并确保 metadata 已脱敏。 |
| 开发 / 运维人员 | 通过审计日志反查 Task Trace，定位敏感操作与后台任务、对象存储、数据库写入之间的关系。 |
| 企业内部运营人员 | 在授权范围内理解某次配置、证书或媒体相关操作是否已完成，减少重复操作和人工排障成本。 |

## 3. 范围

### 3.1 本期包含

| 范围 | 说明 |
|---|---|
| 审计写入字段补齐 | `AuditLogRepository.insert()` 或等价写入接口支持 `task_trace_id` 与 `task_type`。 |
| 敏感操作接入 | 首批梳理系统设置、品牌证书管理、媒体/上传相关管理操作等敏感审计写入点。 |
| 查询展示一致性 | 日志审计列表与详情对 `audit` 类型日志展示 Task Trace 信息，与 request / usage_event 类型保持一致。 |
| 任务时间线联动 | 当审计日志存在 `task_trace_id` 时，详情抽屉可展示或引用同一任务链路的节点信息。 |
| 安全脱敏 | 审计 metadata 继续执行敏感字段过滤、长度限制和安全摘要策略。 |
| 数据兼容确认 | 复用既有 `audit_logs.task_trace_id`、`audit_logs.task_type` 字段，并确认 SQLite/MySQL schema 与迁移一致。 |

### 3.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 新增独立审计页面 | 复用现有日志审计页面，不另建与日志审计割裂的页面。 |
| 全量历史审计回填 | 历史 `audit_logs` 中缺失的任务字段不要求补写。 |
| 完整 APM 或外部日志系统 | 不接入外部追踪平台，不建设链路拓扑大屏。 |
| 保存完整请求体 / 响应体 | 仅保存必要、安全、脱敏后的上下文摘要。 |
| 扩展所有任务型接口 | 全量任务型接口覆盖由 `REQ-0074-task-trace-coverage-expansion` 继续承接。 |

## 4. 功能要求

### FR-001 审计日志写入支持任务链路字段

- 审计日志写入接口 MUST 支持可选 `task_trace_id` 与 `task_type` 参数。
- 当调用方提供合法任务上下文时，系统 MUST 将 `task_trace_id` 与 `task_type` 持久化到 `audit_logs`。
- 当审计操作没有任务上下文时，`task_trace_id` 与 `task_type` MAY 为空，且不得影响原有审计日志写入行为。
- 写入层 MUST 复用 Repository 或统一数据访问层，不得在业务服务中拼接裸 SQL。

### FR-002 敏感操作写入点补齐

- 系统 MUST 梳理首批需要关联 Task Trace 的审计写入点，并在 `/req-complete` 阶段形成清单。
- 首批候选 SHOULD 包含系统设置修改、品牌证书管理、媒体上传/替换/删除、SKU 或 Banner 等会触发多步骤处理的管理操作。
- 任务型审计操作 SHOULD 复用当前请求或任务上下文中的 `task_trace_id`，避免重复生成互不关联的任务标识。
- 非任务型审计操作 MAY 保持普通审计记录，但必须继续写入操作者、资源、动作、结果和安全 metadata。

### FR-003 日志审计查询与详情展示

- 管理端日志审计列表 MUST 能对 `audit` 类型日志展示 `task_trace_id`、`task_type` 或等价任务摘要字段。
- 日志审计筛选 MUST 支持通过 `task_trace_id` 查询关联日志；可复用“路径 / request_id / task_trace_id”关键字筛选或新增独立筛选项。
- 审计日志详情中若存在 `task_trace_id`，MUST 展示关联任务链路入口、任务类型、任务状态、关键节点或时间线摘要。
- 审计日志详情中若不存在任务链路字段，MUST 保持现有详情展示，不出现空状态报错或异常布局。

### FR-004 与 Task Trace 模型一致

- 审计日志中的 `task_trace_id` MUST 与 `task_traces`、request logs、usage events 使用同一追踪标识语义。
- `task_type` 命名 SHOULD 与 Task Trace 需求中的任务类型枚举保持一致，例如上传、证书维护、批量操作等业务语义。
- 如果一个主请求触发多个审计操作，这些审计日志 SHOULD 共享同一个 `task_trace_id`，并通过 metadata 或资源字段区分操作对象。
- 如果审计写入发生在后台子任务中，系统 SHOULD 保留关联 request_id 或父任务线索，具体模型与 `REQ-0073` 对齐。

### FR-005 数据与兼容性

- 实现阶段 MUST 确认 SQLite 与 MySQL 的 `audit_logs` 均存在 `task_trace_id` 与 `task_type` 字段；若发现不一致，必须同步 schema、迁移、数据库文档和测试。
- `task_trace_id` 查询路径 MUST 保持分页和索引友好，避免以 metadata 无界模糊扫描作为主查询方式。
- 既有审计日志查询、列表分页、详情返回结构 MUST 保持向后兼容；新增字段应为可选字段或有明确默认值。

### FR-006 安全与脱敏

- 审计 metadata MUST 继续过滤 Authorization、Cookie、Token、密码、AccessKey、SecretKey、数据库 DSN、`.env` 内容、内部绝对路径和真实客户数据。
- 前端传入的 `task_trace_id`、`task_type` 或 resource 信息 MUST NOT 作为权限判断依据。
- 日志审计查询入口 MUST 继续仅允许系统管理员访问。
- 审计写入失败或 Task Trace 关联失败不得泄露内部路径、堆栈或对象存储凭证。

## 5. UI 约束

- 管理端 UI MUST 复用现有日志审计页与详情抽屉，不新增营销式页面。
- 列表字段或筛选项新增 `task_trace_id` 时，必须保持桌面端可扫描、移动端不溢出。
- 复制 `task_trace_id`、查看任务时间线等操作应使用现有图标按钮或图标+文字按钮，并提供稳定反馈。
- 任务链路信息应作为详情抽屉中的清晰分组，与基础信息、请求信息、操作者 / 客户端、metadata JSON 分组保持一致。
- UI 实现必须使用 Design System semantic token，不得直接写裸 Hex。

## 6. 关联需求

| 类型 | ID | 关系 |
|---|---|---|
| 父需求 | `REQ-0024-product-usage-logging` | 本需求补齐产品使用日志与审计日志的任务链路关联能力。 |
| 关联需求 | `REQ-0069-upload-observability-trace-logs` | 复用 Task Trace 时间线与日志审计详情展示能力。 |
| 关联需求 | `REQ-0073-task-trace-parent-request-model` | 审计日志任务字段应与主请求、子请求关联模型保持一致。 |
| 关联需求 | `REQ-0074-task-trace-coverage-expansion` | 后续更多任务型接口接入后，可继续复用审计日志任务关联字段。 |

## 7. 状态块

```yaml
requirement_id: REQ-0075-audit-log-task-trace-linking
status: done
lifecycle_stage: review
readiness: Partially Ready
next_command: /req-opsx REQ-0075-audit-log-task-trace-linking
notes:
  - 已补齐 user-stories、business-flow、acceptance、trace 和管理端日志审计 Task Trace 展示原型策略。
  - 已完成评审并通过，可进入 /req-opsx 或纳入 Sprint 规划。
  - 实现前必须确认 SQLite/MySQL schema 中 audit_logs.task_trace_id 与 audit_logs.task_type 一致。
  - 后续 OpenSpec design 必须引用 trace.knowledge_base_refs 并明确首批敏感操作接入清单。
```
