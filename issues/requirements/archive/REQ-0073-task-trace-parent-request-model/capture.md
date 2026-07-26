---
req_id: REQ-0073-task-trace-parent-request-model
status: done
created_at: 2026-07-26 12:49:31
updated_at: 2026-07-26 17:30:55
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0069-upload-observability-trace-logs
captured_via: capture
classification_rationale: 当前描述要求强化 Task Trace 与主请求、子请求的关联模型，属于既有上传观测能力的增强需求。
---

# 一句话

Task Trace 需要建立主请求、子请求与 span 的强关联模型，确保每条任务链路可追溯到用户发起的请求。

# 原始描述

采纳优化建议：给 `task_traces` 增加或逻辑补齐 `parent_request_id`；span 写入 `request_id`；所有任务型接口统一使用 `task_trace_id` 串联。

# 背景与关联

- 当前 request_logs、usage_events、audit_logs 已预留或支持 `task_trace_id`。
- 当前 Task Trace span 模型已有 `request_id` 字段，但上传记录 span 时尚未写入 request_id。
- 日志详情可通过 `task_trace_id` 查看时间线，但主请求到子请求的关系仍偏弱。

# 影响范围

- 后端：Task Trace service、repository、上传接口与未来任务型接口。
- 数据库：可能新增 `task_traces.parent_request_id` 或在 metadata 中标准化保存。
- 日志审计：详情页需要展示主请求与子请求关联。
- 测试：需要覆盖 request_id 与 task_trace_id 的双向追踪。

# 初步需求要点

- 每个 Task Trace 必须能关联到触发它的主请求 request_id。
- 每个 span 如对应一次 API 子请求或任务节点，应记录 request_id。
- 日志详情应能从主请求进入 Task Trace，也能从 Task Trace span 回到对应请求。
- 关联字段命名和写入策略应统一，不依赖临时 metadata 约定。

# 待澄清

- [ ] `parent_request_id` 使用独立字段还是 metadata 结构化字段。
- [ ] 一个用户请求触发多个 Task Trace 时如何展示。
- [ ] 一个 Task Trace 跨多个 API 子请求时是否需要 `parent_task_trace_id` 或 child trace。
- [ ] 历史上传数据是否需要迁移或仅新数据生效。

# 建议验收要点

- [ ] 上传任务的 Task Trace summary 能显示触发它的主 request_id。
- [ ] Task Trace spans 中可查看相关 request_id。
- [ ] 日志详情页可以从 request_id 与 task_trace_id 双向定位。
- [ ] 缺失或非法 task_trace_id 不影响主请求日志落库。

# 分类说明（/capture）

该条目是任务链路关联模型增强，属于 REQ。
