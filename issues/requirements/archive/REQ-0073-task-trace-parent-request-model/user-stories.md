---
requirement_id: REQ-0073-task-trace-parent-request-model
title: Task Trace 主请求与子请求关联模型 - 用户故事
status: done
owner: product
created_at: 2026-07-26 13:03:43
updated_at: 2026-07-26 17:30:55
---

# 用户故事

## US-001 系统管理员从主请求追溯任务

作为系统管理员，我希望在日志详情中从一次上传或任务型接口的主请求 `request_id` 进入对应 Task Trace，以便确认这次用户操作触发了哪些任务链路。

验收要点：

- 主请求日志详情能展示关联 `task_trace_id` 或任务摘要入口。
- 一个主请求触发多个 Task Trace 时，详情能区分多个任务。
- 没有关联 Task Trace 的普通请求仍按现有日志详情展示。

## US-002 运维从 span 回到请求日志

作为开发 / 运维人员，我希望 Task Trace 时间线中的 span 能展示相关 `request_id`，以便从失败节点或慢节点快速定位对应请求日志。

验收要点：

- 有请求上下文的 span 必须写入当前 `request_id`。
- 无直接请求上下文的内部节点必须保留 `task_trace_id` 和时间顺序，并说明 request 归属为空或继承父请求。
- 日志详情能从 span 的 `request_id` 定位到对应请求日志。

## US-003 后端研发统一任务型接口追踪模型

作为后端研发人员，我希望所有任务型接口统一使用 `task_trace_id` 串联 request logs、usage events、audit logs、Task Trace 和 spans，以便后续上传、导入、导出、批处理等场景采用同一模型。

验收要点：

- `task_trace_id` 由后端生成或校验后确认，不信任前端任意传值。
- `parent_request_id` 来自后端请求上下文。
- 缺失或非法 `task_trace_id` 不影响主请求日志落库，并记录明确错误摘要。

## US-004 安全审计确认任务链路来源

作为安全 / 审计负责人，我希望每条任务链路都能说明由谁、从哪个请求发起，同时不泄露敏感字段，以便满足审计追溯和最小化采集要求。

验收要点：

- 任务链路包含主请求、操作者、客户端、资源摘要和脱敏 metadata。
- `request_id`、`parent_request_id`、`task_trace_id` 只用于追踪，不用于权限判断。
- 任务追踪数据不保存 Authorization、Cookie、密钥、真实本地路径或完整敏感请求体。

## US-005 产品负责人确认父需求增强边界

作为产品负责人，我希望本需求只强化 `REQ-0069` 的请求关联模型，而不重新定义完整 Task Trace 能力，以便后续 OpenSpec Change 范围清晰可控。

验收要点：

- 文档明确本需求与父需求差异。
- OpenSpec design 必须决策 `parent_request_id` 的独立字段或结构化 metadata 方案。
- 历史数据默认仅兼容缺失字段，不强制回填。
