---
requirement_id: REQ-0124-log-audit-behavior-trace-model
title: 日志审计补齐行为链路与任务链路采集模型 - 用户故事
owner: product
source: requirement.md
created_at: 2026-08-25 22:31:11
updated_at: 2026-08-25 22:31:11
---

# 用户故事

## US-001 从一次界面行为追踪全部后端请求

作为系统管理员，我希望在日志审计中输入一次页面访问、按钮点击或表单提交产生的 `behavior_trace_id`，即可看到该行为触发的一个或多个 API 请求，以便判断一次用户操作的完整影响范围。

验收要点：

- `usage_events` 中每条可追踪行为都有 `behavior_trace_id` 和 `behavior_event_id`。
- 同一次行为触发的多个 API 请求共享同一个 `behavior_trace_id`。
- 每条来源于行为事件的请求日志都能通过 `parent_behavior_event_id` 指向具体行为事件。
- 页面访问、按钮点击、搜索筛选、详情查看、表单提交、上传、发布、删除等典型行为具备统一采集口径。

## US-002 从请求追踪任务链路与流程节点

作为研发 / 运维人员，我希望从 `request_logs.request_id` 继续追踪到 `task_traces.parent_request_id` 和 `task_trace_spans`，以便定位任务型接口失败或变慢时具体落在哪个流程节点。

验收要点：

- 任务类请求写入 `request_logs.request_id` 后，任务摘要通过 `task_traces.parent_request_id` 关联该请求。
- 同一个任务的流程节点继续由 `task_trace_spans` 承载，中文展示为“流程节点”。
- 每个流程节点至少可表达节点名称、状态、耗时和脱敏错误摘要。
- 一个请求触发一个或多个任务节点时，日志审计能联动展示请求、任务摘要与节点明细。

## US-003 直接 API 调用也能独立排障

作为外部系统接入方或后台接口调用排障人员，我希望不经过界面操作的 API 调用也能被请求日志和任务链路记录，以便无需伪造用户行为上下文也能定位问题。

验收要点：

- 直接 API 调用允许 `request_logs.behavior_trace_id` 和 `parent_behavior_event_id` 为空。
- 直接 API 调用仍必须生成服务端可信 `request_id`。
- 若该请求触发任务链路，`task_traces.parent_request_id` 继续引用 `request_logs.request_id`。
- 日志审计支持从 `request_id` 进入任务链路和流程节点，不依赖 `usage_events`。

## US-004 管理端日志审计支持多入口查询

作为内部运营人员，我希望日志审计页支持按 `behavior_trace_id`、`request_id`、`task_trace_id` 查询和查看详情，以便根据手头线索快速切入。

验收要点：

- 查询条件支持 `behavior_trace_id`、`request_id`、`task_trace_id`，且与既有时间、用户、状态、路径等筛选协同工作。
- 详情区可以从行为事件查看相关请求，从请求查看任务链路，从任务链路查看流程节点。
- 历史日志或直接 API 调用缺少行为链路时，以空态或“无界面行为来源”展示，不报错。
- 复制或展示链路 ID 时不暴露请求体、响应体、密钥、Token、Cookie 或本机路径。

## US-005 数据采集模型可沉淀为产品通用规范

作为产品和研发负责人，我希望本项目先落地一套清晰的数据采集结构，再抽象为通用产品数据采集与链路观测规范，以便后续产品从开发阶段就具备行为、请求、任务节点的可观测能力。

验收要点：

- 字段语义稳定，不把 `request_id` 混用为用户行为 ID。
- 界面触发和直接 API 调用两种入口都能成立。
- 数据结构兼容 SQLite / MySQL，并具备必要索引建议。
- 后续规范化时可复用本需求的字段注释、采集边界、脱敏策略和测试口径。
