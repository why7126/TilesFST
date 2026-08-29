---
req_id: REQ-0126-product-data-collection-observability-standard
status: done
created_at: 2026-08-26 09:56:28
updated_at: 2026-08-27 23:17:27
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0124-log-audit-behavior-trace-model
---

# 一句话

建立通用产品数据采集与链路观测规范，覆盖小程序、店主端、App、Web 管理端和后端 API，让每个产品从开发阶段就按统一模型采集行为事件、请求日志、任务链路和流程节点。

# 原始描述

用户确认在 REQ-0124 本项目落地之后，需要进一步沉淀为通用规范：

- 规范覆盖小程序、店主端、App、Web 管理端和后端 API。
- 要求所有 API 请求必须记录 `request_logs`。
- 行为事件采用“全量点击采集”方向。
- 确认采用“Task Trace 分级覆盖”。
- 确认默认保留周期按 `request_logs 90天 / usage_events 180天 / task trace 90天 / 聚合1年`。

# 背景与关联

- 关联需求：`REQ-0124-log-audit-behavior-trace-model`
- 关联能力：产品行为事件、请求日志、Request Snapshot、Task Trace、日志审计、链路观测、数据留存治理
- 业务价值：把 REQ-0124 的项目内实现提升为跨产品标准，避免每个新产品重复讨论埋点字段、请求日志、任务节点、脱敏、保留周期和验收口径。
- 预期后续：形成可执行规范，约束新产品从开发时接入采集模型，并为后续 `/req-generate`、`/req-complete` 和 OpenSpec Change 提供验收基础。

# 影响范围

- 全端：Web 管理端、店主端、小程序、App。
- 后端：所有业务 API 请求日志、请求中间件、链路 ID 透传、直接 API 调用兼容。
- 数据模型：`usage_events`、`request_logs`、`task_traces`、`task_trace_spans`、后续聚合数据。
- 规范与治理：API 治理、数据库设计、Task Trace 覆盖、测试标准、数据安全与留存周期。
- 安全与合规：敏感字段脱敏、禁止采集字段、日志保留和超期删除 / 匿名化策略。

# 建议验收要点

- [ ] 规范明确覆盖小程序、店主端、App、Web 管理端和后端 API。
- [ ] 规范明确所有 API 请求 MUST 写入 `request_logs`，并列出健康检查、静态资源、预检请求、文档资源、内部探活等可排除项。
- [ ] 规范明确用户行为事件采集口径：关键业务点击、页面访问、搜索、筛选、详情、保存、删除、上传、分享、收藏等应采集；纯视觉或无业务含义的 UI 噪音可排除。
- [ ] 规范明确四层链路：`usage_events -> request_logs -> task_traces -> task_trace_spans`。
- [ ] 规范明确直接 API 调用不伪造行为事件，允许 `behavior_trace_id` 为空，并继续从 `request_logs.request_id` 进入任务链路。
- [ ] 规范明确 Task Trace 分级覆盖：所有 API 有 request log；长耗时、多步骤、批量、异步、外部依赖、高风险写操作 MUST 有 Task Trace；普通简单写操作 MAY 只保留 request log。
- [ ] 规范明确默认保留周期：`request_logs` 90 天、`usage_events` 明细 180 天、`task_traces/task_trace_spans` 90 天、聚合数据 1 年。
- [ ] 规范明确超期数据删除或匿名化策略，不允许无限期保留明细日志。
- [ ] 规范明确敏感字段、请求体、响应体、Header、Cookie、Authorization、Token、真实密钥、本机路径、完整内部对象 key 和真实客户敏感数据不得进入采集 payload 或 metadata 原文。
- [ ] 规范明确新产品接入清单：前端 SDK/helper、后端 middleware、DB migration、OpenAPI/Orval、测试模板、脱敏 helper 和验收清单。

# 待澄清

- [ ] “全量点击采集”是否最终表述为“所有可命名业务行为必须采集，纯 UI 噪音点击可排除”。
- [ ] App 端是否需要单独定义离线缓存、重试上报和设备标识脱敏策略。
- [ ] 小程序与店主端是否采用与 Web 管理端完全一致的 `behavior_trace_id` / `behavior_event_id` 生成格式。
- [ ] 默认保留周期是否允许不同产品按合规要求上调或下调；如允许，需要定义审批和记录要求。
- [ ] 聚合数据的粒度与表结构是否纳入本规范首版，还是只定义保留周期和后续扩展原则。

# 探索结论

本需求来自 `/explore` 讨论结论。推荐将 REQ-0124 的项目内模型沉淀为“通用产品数据采集与链路观测规范 v1”。

推荐规范口径：

```text
全端覆盖：
Web 管理端 / 店主端 / 小程序 / App / 后端 API

采集层级：
用户行为事件 -> API 请求日志 -> 任务链路 -> 流程节点

强制要求：
所有 API 请求记录 request_logs
所有关键用户行为记录 usage_events
长耗时/多步骤/批量/异步/外部依赖/高风险写操作记录 Task Trace

默认保留：
request_logs 90 天
usage_events 180 天
task_traces / task_trace_spans 90 天
聚合数据 1 年
```

首版建议不纳入外部 APM、OpenTelemetry、第三方埋点平台、实时告警、BI 大屏、复杂用户画像或历史数据强制回填。
