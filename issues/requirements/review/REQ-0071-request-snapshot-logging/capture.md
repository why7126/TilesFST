---
req_id: REQ-0071-request-snapshot-logging
status: captured
created_at: 2026-07-26 12:49:31
updated_at: 2026-07-26 12:49:31
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0024-product-usage-logging
captured_via: capture
classification_rationale: 当前描述要求增强 API 请求日志采集字段与完整请求信息，属于尚未交付的日志治理能力增强，而非已有能力偏差，因此归类为需求。
---

# 一句话

API 请求日志需要补齐可审计、可排障的完整请求快照，覆盖前台、后台与小程序请求。

# 原始描述

采纳日志与用户行为数据优化建议：建立统一 Request Snapshot，记录 method、path、route template、query 白名单、body schema 摘要、资源 ID、状态码、错误码、耗时、用户、客户端、环境、请求/响应时间，并避免保存原始敏感 body。

# 背景与关联

- 当前主请求日志已记录 `request_id`、用户、客户端、method、path、状态码、耗时、脱敏 IP、User-Agent、`task_trace_id` 等信息。
- 当前 metadata 主要是 `query_params` 和 path，无法完整还原一次业务请求的输入上下文。
- 需要在合规脱敏前提下，为前台、后台、小程序请求提供统一排障与审计依据。

# 影响范围

- 后端：请求日志 middleware、日志服务、日志仓储、请求脱敏策略。
- 数据库：可能扩展 `request_logs.metadata` 结构或新增结构化字段。
- API：日志详情响应需要展示更完整的请求快照。
- Web 管理端：日志审计详情抽屉需要展示快照字段。
- 安全：不得记录 Authorization、Cookie、密码、Token、原始敏感 body、内部路径或真实客户隐私。

# 初步需求要点

- 每个可采集 API 请求都应生成统一 Request Snapshot。
- Snapshot 至少包含请求方法、接口路径、路由模板、查询参数白名单、请求体 schema 摘要、业务资源标识、响应状态、错误码、耗时、操作者、客户端类型、环境、请求开始时间和结束时间。
- 请求体只保存字段级摘要、长度、类型、业务安全字段或脱敏结果，不保存敏感原文。
- 日志详情页能直接查看 Snapshot，不需要从多个位置拼接。

# 待澄清

- [ ] route template 在 FastAPI middleware 中如何稳定取得。
- [ ] 各接口允许进入 Snapshot 的 query/body 字段白名单。
- [ ] 是否需要单独字段承载 environment、route_template、resource_type、resource_id。
- [ ] 生产环境日志保留周期与脱敏审计策略是否沿用系统设置。

# 建议验收要点

- [ ] 前台、后台、小程序 API 请求均能在日志详情中看到统一 Request Snapshot。
- [ ] Snapshot 包含完整排障所需字段，且敏感字段被脱敏或完全忽略。
- [ ] 错误请求能关联错误码、状态码、耗时和请求上下文。
- [ ] 日志列表与详情查询不因 Snapshot 扩展产生明显性能退化。

# 分类说明（/capture）

该条目是日志采集能力增强，属于 REQ。
