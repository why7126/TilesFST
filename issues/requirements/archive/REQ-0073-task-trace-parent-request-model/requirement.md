---
requirement_id: REQ-0073-task-trace-parent-request-model
title: Task Trace 主请求与子请求关联模型
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0069-upload-observability-trace-logs
created_at: 2026-07-26 12:57:24
updated_at: 2026-07-26 17:30:55
---

# REQ-0073 Task Trace 主请求与子请求关联模型

## 1. 需求背景

`REQ-0069-upload-observability-trace-logs` 已建立 Task Trace 能力方向：使用 `task_trace_id` 串联一次多节点任务，并在审计日志详情中展示任务时间线、span、耗时、结果和关联 `request_id`。

但当前链路关联模型仍有薄弱点：`request_logs`、`usage_events`、`audit_logs` 已预留或支持 `task_trace_id`，Task Trace span 模型也已有 `request_id` 字段，但上传记录 span 时尚未稳定写入 `request_id`；同时 Task Trace 与触发它的用户主请求之间缺少明确、结构化、可查询的父级关系。对于一次上传或未来导入、导出、批量处理等任务，排障人员仍可能只能从 `task_trace_id` 看到任务内部节点，却难以从主请求、子请求、span 三者之间形成完整闭环。

本需求作为 `REQ-0069` 的子需求，目标是收紧 Task Trace 的关联事实源：明确主请求、子请求与 span 的字段模型、写入时机和查询关系，让每条任务链路都能追溯到用户发起的请求，也能从任务时间线回到相关请求日志。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 系统管理员 | 从日志详情中看清一次任务由哪个用户请求触发，以及任务过程中产生了哪些相关请求。 |
| 开发 / 运维人员 | 基于 `request_id`、`parent_request_id`、`task_trace_id` 快速定位主请求、子请求、span 和失败节点。 |
| 企业内部运营人员 | 当上传或长耗时任务异常时，能获得可解释、可追踪的排障编号。 |
| 安全 / 审计负责人 | 确认任务行为与请求日志、审计日志之间存在一致的追溯关系，避免孤立日志。 |

## 3. 范围

### 3.1 本期包含

- 明确 Task Trace 与触发它的主请求 `request_id` 的关联模型。
- 明确 span 与对应 API 子请求或任务节点 `request_id` 的写入策略。
- 统一任务型接口使用 `task_trace_id` 串联 request logs、usage events、audit logs、task trace 和 task spans。
- 支持从主请求日志进入 Task Trace，也支持从 Task Trace span 回到相关请求日志。
- 明确 `parent_request_id` 使用独立字段或等价结构化字段的产品约束，并要求 OpenSpec design 中给出实现取舍。
- 上传任务作为首批验证场景，覆盖图片、视频、文件上传的主请求与子请求关联。
- 补充后端数据模型、Repository、Service、API 响应和测试的同步要求。

### 3.2 本期不包含

- 建设完整分布式追踪、跨服务 Trace Topology 或外部 APM 集成。
- 为历史上传任务补全 `parent_request_id` 或 span `request_id`。
- 新增视频转码、压缩、多清晰度或封面生成能力。
- 为店主 Web 展示端或小程序新增任务追踪展示入口。
- 引入未授权对象存储直连、完整请求体保存或敏感字段长期留存。

## 4. 核心概念

### 4.1 主请求

主请求是用户发起一次业务任务时的入口请求，例如管理端视频上传 API 请求。主请求拥有全局唯一的 `request_id`，并触发或绑定一个 `task_trace_id`。

### 4.2 子请求

子请求是同一任务过程中产生的后续 API 请求或查询请求，例如任务状态查询、补充事件上报、前端完成/失败事件上报。子请求应继续携带同一个 `task_trace_id`，并保留自身 `request_id`。

### 4.3 parent_request_id

`parent_request_id` 表示 Task Trace 所属的触发请求。实现阶段可以选择：

| 方案 | 要求 |
|---|---|
| 独立字段 | 在 `task_traces` 或等价任务摘要表中新增 `parent_request_id`，并建立查询索引。 |
| 结构化字段 | 在 metadata 或等价 JSON 字段中标准化保存 `parent_request_id`，但必须可稳定读取、校验和展示，不得依赖临时约定。 |

无论采用哪种方案，OpenSpec design 必须说明取舍、索引策略、SQLite/MySQL 兼容性和迁移边界。

## 5. 功能要求

### FR-001 Task Trace 必须关联主请求

- 每个由 API 请求触发的 Task Trace MUST 能关联到触发它的主请求 `request_id`。
- 关联字段 SHOULD 命名为 `parent_request_id`；如实现采用 metadata 结构化字段，语义必须保持一致。
- `parent_request_id` MUST 来自后端请求上下文，不得信任前端自行声明。
- 上传任务创建 Task Trace 时 MUST 同步写入或绑定 `parent_request_id`。
- 一个主请求触发多个 Task Trace 时，系统 MUST 保留一对多关系，并在日志详情中能区分每个任务摘要。

### FR-002 span 必须记录相关 request_id

- 每个 span 如对应一次 API 请求、子请求或可归属到当前请求上下文的后端节点，MUST 写入该请求的 `request_id`。
- 无直接请求上下文的后端内部节点 MAY 继承当前任务的 `parent_request_id` 或标记为空，但必须保留 `task_trace_id` 和可排序时间信息。
- span 写入失败不得覆盖主业务错误；追踪失败时应按可观测性降级策略记录安全摘要。
- span 的 `request_id` 不得保存 Authorization、Cookie、密钥、真实本地路径或完整敏感请求体。

### FR-003 任务型接口统一透传 task_trace_id

- 所有任务型接口 MUST 使用 `task_trace_id` 串联请求日志、行为事件、审计日志、Task Trace 和 span。
- 后端生成或确认 `task_trace_id` 后，相关响应、日志和事件 MUST 使用同一个值。
- 前端如携带 `task_trace_id`，后端 MUST 校验格式、权限边界和任务归属；不可信或非法值不得直接落库。
- 缺失或非法 `task_trace_id` MUST 不影响主请求日志落库，并应返回或记录明确的可观测错误摘要。

### FR-004 支持 request_id 与 task_trace_id 双向定位

- 日志详情 MUST 能从主请求 `request_id` 展示关联 Task Trace 摘要或入口。
- Task Trace 时间线 MUST 能展示 span 关联的 `request_id`，并支持定位到对应请求日志详情。
- 日志列表或详情中的查询能力 SHOULD 支持按 `request_id`、`parent_request_id`、`task_trace_id` 定位同一任务链路。
- 当某条日志没有 `task_trace_id` 或某个 span 没有 `request_id` 时，页面 MUST 保持可用，不得展示空状态错误或误导性关联。

### FR-005 上传任务首批验证

- 图片、视频、文件上传 MUST 作为首批验证场景。
- 上传主请求 MUST 生成或绑定 `task_trace_id`，并让 Task Trace 记录 `parent_request_id`。
- 上传相关 span MUST 尽量写入当前 API 请求的 `request_id`，至少覆盖后端接收、文件校验、对象存储写入、数据库落库、响应返回等节点。
- 日志详情 MUST 能回答“这次上传由哪个请求触发”“哪些节点属于同一任务”“哪些 span 对应哪些请求”。

### FR-006 数据模型与兼容性

- 实现阶段如新增 `task_traces.parent_request_id`，MUST 同步 SQLite schema、生产 MySQL 迁移、Pydantic Schema、Repository、测试和数据库文档。
- 如采用 metadata 结构化字段，MUST 定义稳定 JSON 结构、读取兼容策略和缺失字段兜底。
- `parent_request_id`、`task_trace_id`、span `request_id` 的查询路径 MUST 索引友好，避免以无界 metadata 模糊扫描作为主查询方式。
- 历史数据 MAY 不迁移，但页面和 API MUST 对历史缺失字段提供安全兜底。

### FR-007 权限与安全

- 管理端任务链路查询仍 MUST 仅允许系统管理员访问。
- `parent_request_id`、`request_id`、`task_trace_id` 只用于追踪与定位，不得作为权限判断依据。
- 任务追踪数据 MUST 遵守日志脱敏、保留周期和最小化采集原则。
- 上传链路不得暴露对象存储真实凭证、内部绝对路径、临时文件路径或未授权直连地址。

## 6. UI 约束

- 管理端复用现有日志审计详情入口，不新增独立营销式页面。
- 日志详情中 Task Trace 分组应清晰展示主请求、任务标识、任务状态、span 列表和关联请求。
- `parent_request_id`、`task_trace_id`、span `request_id` 应支持复制或跳转查看，但复制反馈不得造成布局位移。
- UI 必须遵守 Design System semantic token，不得直接写裸 Hex。
- 移动或窄屏布局下，关联 ID 不得挤压时间线主体内容，可折行或使用等宽截断展示。

## 7. 关联需求

| 类型 | ID | 关系 |
|---|---|---|
| 父需求 | `REQ-0069-upload-observability-trace-logs` | 本需求强化其 Task Trace 与 request_id 的关联模型。 |
| 上游需求 | `REQ-0024-product-usage-logging` | 现有请求日志、行为事件与审计日志能力的事实源基础。 |

## 8. 状态块

```yaml
requirement_id: REQ-0073-task-trace-parent-request-model
status: done
lifecycle_stage: review
readiness: Ready
next_command: /req-opsx REQ-0073-task-trace-parent-request-model
notes:
  - 已评审通过，可进入 req-opsx。
  - OpenSpec design 必须明确 parent_request_id 使用独立字段还是 metadata 结构化字段。
  - 历史数据是否迁移暂未确认，默认仅要求新数据生效并兼容历史缺失字段。
```
