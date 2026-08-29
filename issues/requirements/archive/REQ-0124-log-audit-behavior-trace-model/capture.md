---
req_id: REQ-0124-log-audit-behavior-trace-model
status: done
created_at: 2026-08-25 22:20:40
updated_at: 2026-08-27 23:11:59
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0024-product-usage-logging
---

# 一句话

日志审计需要补齐 `behavior_trace_id`、`behavior_event_id`、`parent_behavior_event_id` 与任务链路采集模型，支持界面行为、直接 API 调用、接口请求和任务流程节点之间的统一追踪。

# 原始描述

数据采集模型支持两种入口：

A. 界面触发

```text
usage_events.behavior_trace_id
  -> request_logs.behavior_trace_id
      -> task_traces.parent_request_id
          -> task_trace_spans
```

B. 直接 API 调用

```text
request_logs.request_id
  -> task_traces.parent_request_id
      -> task_trace_spans
```

需要覆盖：

- `usage_events` 增加行为链路字段。
- `request_logs` 增加行为来源关联字段。
- 前端请求统一透传 `behavior_trace_id` / `behavior_event_id`。
- 直接 API 调用保持 `behavior_trace_id` 可空。
- 任务类请求继续通过 `parent_request_id` 关联 `request_logs`。
- `task_trace_spans` 保持流程节点拆分。
- 日志审计页支持按 `behavior_trace_id` / `request_id` / `task_trace_id` 查询。

# 背景与关联

- 关联需求：`REQ-0024-product-usage-logging`、`REQ-0071-request-snapshot-logging`、`REQ-0073-task-trace-parent-request-model`、`REQ-0075-audit-log-task-trace-linking`、`REQ-0076-observability-dashboard`
- 涉及端与模块：Web 管理端、后端 API 请求日志、产品行为事件、Task Trace、日志审计页、前端请求封装
- 业务价值：让管理员、研发和运维人员可以从一次界面行为追踪到多个后端请求，再追踪到任务型请求的具体流程节点；直接 API 调用也能从请求日志开始进入任务链路排障。
- 预期后续：在 PRD / OpenSpec 中明确字段语义、数据库变更、请求头透传、兼容旧日志、查询筛选、脱敏策略、索引与测试验收。

# 影响范围

- 后端：影响请求日志中间件、日志服务、日志仓储、Task Trace 关联模型与日志审计查询。
- Web 管理端：影响行为事件上报、请求封装、日志审计筛选和详情展示。
- API：可能新增或扩展日志审计查询参数、响应字段和请求头约定。
- 数据库：可能为 `usage_events`、`request_logs`、`task_traces` 增加行为链路字段和索引。
- 小程序 / 店主端：若后续纳入行为采集，应复用同一行为链路字段和客户端类型策略。
- Orval：若 API contract 变化，后续实现阶段需要同步 OpenAPI 与 Orval。
- Docker Compose：本需求本身不直接改变部署拓扑；若新增环境变量或清理任务，后续 Change 需说明。

# 建议验收要点

- [ ] 界面行为事件写入 `usage_events.behavior_trace_id` 和 `behavior_event_id`。
- [ ] 同一次界面行为触发的多个 API 请求写入同一个 `request_logs.behavior_trace_id`。
- [ ] `request_logs.parent_behavior_event_id` 能关联触发该请求的行为事件。
- [ ] 直接 API 调用在缺少行为上下文时仍正常写入 `request_logs.request_id`，且 `behavior_trace_id` 可为空。
- [ ] 任务类请求继续通过 `task_traces.parent_request_id` 关联 `request_logs.request_id`。
- [ ] `task_trace_spans` 保持流程节点拆分，并可通过 `task_trace_id` 联动任务链路。
- [ ] 日志审计页或接口支持按 `behavior_trace_id`、`request_id`、`task_trace_id` 查询和定位链路。
- [ ] 敏感字段、请求体、响应体、Header、Cookie、Token、真实密钥和内部路径不得进入 metadata 原文。
- [ ] SQLite 与 MySQL schema、索引、迁移和数据库文档保持一致。
- [ ] 覆盖前端请求透传、后端日志写入、直接 API 调用、任务节点联动和日志审计查询的测试。

# 待澄清

- [ ] `behavior_event_id` 由前端生成还是后端在接收行为事件时生成。
- [ ] `parent_behavior_event_id` 是否必须持久化为一等字段，还是可先通过 `behavior_trace_id` 与 metadata 关联。
- [ ] 哪些前端事件首批必须接入：页面访问、按钮点击、搜索筛选、表单提交、上传、登录退出是否全部纳入本期。
- [ ] 日志审计页是否新增独立 `behavior_trace_id` 筛选项，还是复用现有路径 / request_id 搜索框。
- [ ] 历史日志是否需要兼容展示空行为链路，是否需要回填。

# 探索结论

本需求来自 `/explore` 讨论结论：采用通用四层采集模型，保留前一版命名，不做字段精简调整。

```text
usage_events        用户行为事件
request_logs        后端接口请求
task_traces         任务型请求 / 后台任务
task_trace_spans    任务流程节点
```

核心 ID 语义：

- `behavior_trace_id`：一次用户行为链路，可关联多个 API 请求。
- `behavior_event_id`：一次具体行为事件。
- `request_id`：一次后端 HTTP 请求。
- `parent_behavior_event_id`：请求来源行为事件。
- `parent_request_id`：任务来源请求。
- `task_trace_id`：任务链路。
- `span`：任务流程节点，中文展示可称为“流程节点”。
