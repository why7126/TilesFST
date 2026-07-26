---
requirement_id: REQ-0076-observability-dashboard
title: 日志审计与链路观测仪表
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0024-product-usage-logging
created_at: 2026-07-26 12:57:48
updated_at: 2026-07-26 16:58:35
---

# REQ-0076 日志审计与链路观测仪表

## 1. 需求背景

`REQ-0024-product-usage-logging` 已建立管理端日志审计、请求日志、行为事件与 Task Trace 的基础查询能力。当前日志审计页可以查看列表、详情、Task Trace 时间线和基础指标，例如今日日志总量、API 错误、慢请求、审计操作数量。

随着后台任务、媒体上传、接口请求和多端行为事件逐步接入日志体系，单纯的日志列表和详情抽屉已经不足以支撑排障。管理员和研发/运维人员需要从“发生了什么”进一步看到“哪类任务失败最多、哪里最慢、哪个客户端或接口错误率异常、如何从 `request_id` 或 `task_trace_id` 快速追踪到完整链路”。

本需求用于将现有日志审计页升级为“日志审计 + 链路观测”仪表，围绕请求、行为、审计和 Task Trace 输出可筛选、可下钻、可追踪的关键指标，提升管理端排障效率。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 系统管理员 | 在统一页面查看平台请求、操作、审计和任务链路健康状况，快速发现异常。 |
| 研发 / 运维人员 | 通过任务成功率、慢任务、最慢 span、接口错误率和 request_id / task_trace_id 定位问题。 |
| 企业内部运营人员 | 在授权范围内理解上传、维护、上下架等关键操作是否稳定成功。 |
| 产品负责人 | 观察多端使用行为、客户端分布和失败原因趋势，辅助后续体验优化。 |

## 3. 范围

### 3.1 本期包含

- 管理端日志审计页升级为链路观测仪表，或新增等价的管理端观测入口。
- 请求日志、行为事件、审计操作和 Task Trace 的统一摘要指标。
- 任务成功率、任务耗时分布、慢任务排行、失败任务排行与最慢 span 排行。
- 接口错误率、慢请求排行、失败原因分布与客户端分布。
- 按时间范围、客户端、日志类型、任务类型、接口路径、状态 / 结果筛选指标。
- 支持通过 `request_id` / `task_trace_id` 一键追踪到日志详情或 Task Trace 时间线。
- 空数据、加载失败、权限不足、指标口径说明等管理端状态反馈。

### 3.2 本期不包含

- 外部 APM、链路追踪系统或日志平台接入。
- 实时大屏、告警推送、SLA 报表和自动异常检测。
- 跨服务分布式追踪标准落地，例如 OpenTelemetry 全量接入。
- 运维级日志统一采集，例如容器 stdout、Nginx access log、数据库慢查询日志。
- 面向店主 Web 展示端或微信小程序的独立观测页面。

## 4. 功能要求

### FR-001 统一观测摘要

系统 MUST 在管理端提供请求、行为、审计和 Task Trace 的统一观测摘要。

摘要指标 SHOULD 至少包含：

| 指标 | 说明 |
|---|---|
| 总日志量 | 当前筛选范围内的请求日志、行为事件、审计操作总量。 |
| API 错误数 / 错误率 | 非成功状态码或业务错误码请求数量及占比。 |
| 慢请求数 | 超过系统慢请求阈值的请求数量。 |
| 任务成功率 | Task Trace 中成功任务占比。 |
| 慢任务数 | 超过任务慢执行阈值的任务数量。 |
| 审计操作数 | 当前筛选范围内的关键审计操作数量。 |

所有摘要指标 MUST 与当前筛选条件保持同一口径，不得与日志列表或 Task Trace 列表出现明显统计口径偏差。

### FR-002 Task Trace 观测指标

系统 MUST 基于 Task Trace 数据输出任务维度观测指标。

Task Trace 指标 MUST 支持：

- 按任务类型统计成功、失败、运行中和取消等状态分布；
- 展示任务成功率和失败任务数量；
- 展示任务耗时分布或等价分桶；
- 展示慢任务排行，包含任务类型、耗时、状态、触发来源、`task_trace_id`；
- 展示最慢 span 排行，包含 span 名称、任务类型、耗时、结果、关联 `task_trace_id`；
- 从任务、慢 span 或失败项跳转到对应 Task Trace 时间线或日志详情。

若现有数据暂不支持 P95 / P99 等分位统计，实现阶段 MAY 先采用平均耗时、最大耗时和固定耗时分桶，但 MUST 在 OpenSpec design 中说明口径。

### FR-003 请求与接口错误观测

系统 MUST 基于请求日志输出接口维度观测指标。

请求观测指标 MUST 支持：

- 按接口路径、方法、状态码统计请求量、错误量和错误率；
- 展示慢请求排行，包含路径、方法、状态码、耗时、客户端、`request_id`；
- 展示失败原因分布，优先使用错误码、异常摘要或业务失败原因；
- 支持从错误接口、慢请求或失败原因跳转到日志详情；
- 支持复制 `request_id`，并可用 `request_id` 反查关联日志和 Task Trace。

指标聚合 MUST 避免暴露完整请求体、响应体、Authorization、Cookie、Token、密码、真实密钥或数据库连接串。

### FR-004 客户端与行为分布

系统 SHOULD 展示不同客户端来源的请求和行为事件分布。

客户端分布 SHOULD 覆盖：

- `web_admin`；
- `web_catalog`；
- `miniapp`；
- `backend` 或系统任务；
- 未识别客户端。

行为事件分布 SHOULD 优先展示事件类型、模块、结果和失败原因。若行为事件与请求日志之间存在 `request_id`，页面 SHOULD 支持从行为事件追踪到同请求链路中的请求日志和 Task Trace。

### FR-005 筛选与追踪工作流

仪表 MUST 支持排障常用筛选与追踪工作流。

筛选条件 SHOULD 包含：

| 筛选项 | 说明 |
|---|---|
| 时间范围 | 默认展示近期数据；具体默认值在 `/req-complete` 阶段确认。 |
| 日志类型 | 请求日志、行为事件、审计操作、Task Trace。 |
| 客户端 | 管理端、店主端、小程序、后端任务等。 |
| 任务类型 | Task Trace 的任务分类。 |
| 接口路径 | API path 或路径关键词。 |
| 状态 / 结果 | 成功、失败、慢请求、慢任务、错误状态码等。 |
| 追踪 ID | `request_id` 或 `task_trace_id` 精确查询。 |

用户输入 `request_id` 或 `task_trace_id` 后，系统 MUST 能直接定位到对应日志详情、Task Trace 时间线或相关记录集合；找不到记录时 MUST 提供清晰空态。

### FR-006 管理端权限与信息架构

链路观测仪表 MUST 位于管理端权限边界内，仅允许系统管理员或具备日志审计权限的角色访问。

信息架构 MAY 采用以下之一，并在后续需求完善阶段确认：

| 方案 | 说明 |
|---|---|
| 扩展现有日志审计页 | 在 `/admin/logs` 或现有日志审计路由内增加观测仪表 Tab / 区块。 |
| 新增链路观测页 | 在 SYSTEM 分组新增链路观测入口，与日志审计页互相跳转。 |

无论采用哪种方案，页面 MUST 保留日志列表和详情追踪入口，避免只提供静态指标卡而无法下钻排障。

### FR-007 聚合接口与性能

后端 MUST 提供支撑仪表的聚合查询能力，具体可新增指标接口或扩展现有日志 summary。

聚合查询 MUST 满足：

- 仅管理端鉴权后可访问；
- 支持时间范围、客户端、日志类型、任务类型、接口路径等筛选；
- 返回结构化指标、分布、排行和跳转所需 ID；
- 对空数据返回空集合或零值摘要；
- 对大日志量场景使用数据库聚合、索引或分页策略，避免无条件全表扫描后在应用内聚合；
- SQLite demo 与生产 MySQL 均可运行。

API 变更在后续 OpenSpec 阶段 MUST 同步 OpenAPI、Orval、接口文档和测试。

## 5. UI 约束

- 管理端页面 MUST 遵守“工业石材 · 暗色旗舰风” Design System，使用 semantic token 与既有管理端组件。
- 页面 SHOULD 复用现有管理端列表页、筛选区、指标卡、表格、详情抽屉和 Task Trace 时间线模式。
- 仪表布局 SHOULD 支持“摘要指标 + 筛选 + 分布 / 排行 + 明细下钻”的排障工作流。
- 图表或分布视图 MUST 服务于排障判断，避免只有装饰性图形。
- 慢任务、最慢 span、接口错误、失败原因等列表项 MUST 提供可点击追踪入口。
- 空态、加载失败、权限不足和无匹配追踪 ID 状态 MUST 有清晰反馈。
- 页面文案不得展示敏感字段原值；被脱敏字段以 `******`、`已脱敏` 或等价方式呈现。

## 6. 关联需求

| 类型 | 关联项 | 说明 |
|---|---|---|
| 父需求 | `REQ-0024-product-usage-logging` | 已建立产品使用行为埋点、接口请求日志详情和管理端日志审计基础能力。 |
| 相关需求 | `REQ-0069-upload-observability-trace-logs` | 与上传排障、Task Trace 和 trace 日志可观测性相关。 |
| 相关需求 | `REQ-0034-ai-token-usage-observability` | 与命令运行观测、聚合快照和可复盘口径相关，可复用“脱敏统计优先”原则。 |

## 7. 状态

```yaml
status: done
lifecycle_stage: review
next: /req-opsx REQ-0076-observability-dashboard
readiness: Ready
needs_prototype: true
needs_api_change: true
needs_database_change: false
needs_orval: true
needs_docker_validation: false
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags:
  - admin-list
```
