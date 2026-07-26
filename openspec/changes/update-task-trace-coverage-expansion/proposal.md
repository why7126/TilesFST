## Why

REQ-0069 已经把 Task Trace 建成上传链路的可观测基础，但 REQ-0074 指出保存 SKU、批量操作、导入导出、媒体处理、异步任务、复杂查询等任务型接口仍缺少统一链路追踪。若这些接口只依赖单条 request log，管理员和开发人员仍无法定位慢节点、失败节点、子请求或后台任务与用户请求的关系。

本 Change 将现有 Task Trace 从上传样例扩展为任务型业务接口的通用覆盖策略，并要求首批接口清单、helper 封装、span 完整性、失败诊断、安全脱敏和契约同步在 OpenSpec 层固化。

## What Changes

- 扩展“任务链路追踪”规格：定义任务型接口判定标准，并要求首批覆盖保存 SKU、批量操作、导入导出、媒体处理、异步任务和复杂查询候选。
- 要求首批任务型接口生成或接收可信 `task_trace_id`，并在请求日志、审计日志、task span、异步任务和子请求中保持关联。
- 要求 Task Trace helper 或等价封装支持任务上下文绑定、span 写入、降级记录和失败节点记录。
- 要求同步、异步、批量任务的关键 span 覆盖策略，包含部分成功、超时、最慢节点和失败分类摘要。
- 要求管理端复杂任务反馈中展示或复制 `task_trace_id`，并复用日志审计详情查看任务时间线。
- 要求 API、SQLite/MySQL schema、OpenAPI、Orval、docs 和测试随实际实现同步。

## Capabilities

### New Capabilities

无。本 Change 扩展既有 `product-usage-logging` 能力，不新增顶层 capability。

### Modified Capabilities

- `product-usage-logging`: 扩展 Task Trace 从上传链路到任务型业务接口，补充任务型接口清单、helper、同步/异步/批量 span、管理端追踪标识反馈和同步测试要求。

## Impact

- 后端：任务型接口梳理、Task Trace helper 或服务封装、业务服务 span 埋点、异步任务上下文继承、失败节点记录。
- API：首批接口可能新增 `task_trace_id` 或任务摘要字段；若新增任务状态或事件接口，必须使用统一 `ApiResponse`。
- 数据库：如新增或调整 Task Trace 存储字段，必须同步 SQLite / MySQL schema、迁移、索引和数据库文档。
- Web 管理端：复杂任务成功、失败、处理中或部分成功反馈需展示 / 复制 `task_trace_id`，并可进入日志审计查看任务时间线。
- 对象存储 / 媒体：媒体处理类任务仍必须经过后端授权和对象存储适配层，不能前端直连未授权对象存储。
- 测试：补充后端 pytest、Web Vitest / Testing Library、OpenAPI / Orval 生成验证；涉及生产 DB、对象存储、上传或异步边界时，tasks 应前置 smoke evidence stub。
