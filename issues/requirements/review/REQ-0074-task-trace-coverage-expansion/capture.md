---
req_id: REQ-0074-task-trace-coverage-expansion
status: captured
created_at: 2026-07-26 12:49:31
updated_at: 2026-07-26 12:49:31
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0069-upload-observability-trace-logs
captured_via: capture
classification_rationale: 当前描述要求把 Task Trace 从上传扩展到更多任务型业务接口，是新增覆盖范围需求。
---

# 一句话

将 Task Trace 从上传链路扩展到所有长耗时、任务型或多步骤业务接口。

# 原始描述

采纳优化建议：把 Task Trace 从上传扩展到保存 SKU、批量操作、导入导出、媒体处理、异步任务、复杂查询等任务型操作。

# 背景与关联

- 当前 Task Trace 主要覆盖上传类任务。
- 用户预期每个请求及其子请求都有明确完整请求信息，任务型子请求需要和用户请求关联。
- 复杂保存、批量处理与异步任务若没有 span，排障只能依赖单条请求日志。

# 影响范围

- 后端：任务型接口梳理、Task Trace 接入工具封装、业务服务 span 埋点。
- Web 管理端：复杂任务发起后展示或复制 task_trace_id。
- API：任务型接口响应可能需要返回 task_trace_id。
- 测试：任务链路 span 完整性和失败节点记录。

# 初步需求要点

- 先定义“任务型接口”判定标准：长耗时、多步骤、跨服务、异步、批量、媒体处理或复杂保存。
- 每个任务型接口都应生成或接收 `task_trace_id`。
- 每个关键步骤写入 span，记录顺序、耗时、状态、错误码、资源信息和安全 metadata。
- 失败时必须有失败 span，并能定位最慢或失败节点。

# 待澄清

- [ ] 首批接入哪些任务型接口。
- [ ] 同步接口和异步任务是否使用同一个 Task Trace 模型。
- [ ] Task Trace helper 是否需要封装装饰器或上下文管理器。
- [ ] 是否需要任务状态查询接口。

# 建议验收要点

- [ ] 首批任务型接口响应或日志中可获得 task_trace_id。
- [ ] 每个任务至少包含开始、核心处理、持久化或外部服务、响应等 span。
- [ ] 失败任务能在日志审计详情中看到失败节点和错误码。
- [ ] 未接入 Task Trace 的任务型接口有清单和后续排期说明。

# 分类说明（/capture）

该条目是任务链路覆盖范围扩展，属于 REQ。
