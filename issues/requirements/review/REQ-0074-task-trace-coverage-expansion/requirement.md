---
requirement_id: REQ-0074-task-trace-coverage-expansion
title: 任务型接口 Task Trace 覆盖扩展
terminal: multi
version: v1
status: in_sprint
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0069-upload-observability-trace-logs
created_at: 2026-07-26 12:57:18
updated_at: 2026-07-26 15:34:18
---

# REQ-0074 任务型接口 Task Trace 覆盖扩展

## 1. 需求背景

`REQ-0069-upload-observability-trace-logs` 已建立上传链路的 Task Trace 与日志审计查看能力，使图片、视频、文件上传可以通过 `task_trace_id` 串联请求日志、任务节点、耗时和失败原因。

但平台中仍存在大量非上传类任务型操作：保存 SKU、批量上下架、批量删除、导入导出、媒体后处理、异步任务、复杂查询等。这些操作同样具备长耗时、多步骤、跨服务、异步或批量处理特征。若这些接口仍只留下单次请求日志，管理员和开发人员无法稳定回答：

- 一次复杂保存或批量操作拆成了哪些关键步骤；
- 哪个子请求、数据库写入、对象存储调用或异步节点最慢；
- 用户请求与后续后台任务之间如何关联；
- 失败发生在参数校验、业务校验、持久化、外部服务还是响应阶段；
- 后续排障是否能复用统一的 `task_trace_id` 与 span 时间线。

因此，本需求将 Task Trace 从上传链路扩展为任务型业务接口的通用覆盖策略，让所有长耗时、多步骤或需要排障还原的操作具备一致的链路追踪能力。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 系统管理员 | 在日志审计中通过 `task_trace_id` 查看一次任务型操作的完整处理过程。 |
| 企业内部运营人员 | 发起保存、批量、导入导出等操作后，获得可追溯的问题定位依据。 |
| 开发 / 运维人员 | 基于 span 时间线快速定位慢节点、失败节点、错误码和关联资源。 |
| 产品负责人 | 识别高频慢任务与复杂操作失败原因，支持后续体验优化排序。 |
| 安全 / 审计负责人 | 追踪关键操作由谁发起、影响哪些资源，同时保证 metadata 脱敏。 |

## 3. 需求目标

- 定义“任务型接口”的判定标准，并形成首批接入清单。
- 为首批任务型接口生成或接收 `task_trace_id`。
- 为每个任务的关键处理步骤写入可排序 span。
- 将用户请求、子请求、异步任务、批量子项和外部服务调用关联到同一个任务链路。
- 在失败、超时或部分成功时记录失败 span、错误码、资源摘要和耗时。
- 复用 `REQ-0069` 已建立的 Task Trace 模型、审计日志详情与脱敏边界，避免形成新的割裂日志体系。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 任务型接口判定标准 | 明确长耗时、多步骤、跨服务、异步、批量、媒体处理、复杂保存、复杂查询等判定条件。 |
| 首批接口清单 | 梳理并确认首批接入 Task Trace 的管理端业务接口。 |
| Task Trace helper | 复用或封装统一工具，支持生成、透传、上下文绑定和 span 写入。 |
| 业务服务 span 埋点 | 在首批接口的关键服务步骤记录顺序、耗时、状态、错误码和资源摘要。 |
| 子请求 / 异步关联 | 同一用户操作触发的子请求或异步任务必须与原始 `task_trace_id` 关联。 |
| 失败节点记录 | 参数校验、业务校验、持久化、对象存储、导入导出、异步处理等失败必须落失败 span。 |
| 管理端可见性 | 复杂任务发起后，管理端应能展示、复制或在错误反馈中带出 `task_trace_id`。 |
| 测试覆盖 | 补充首批接口的 span 完整性、失败节点和 task_trace_id 透传测试。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 覆盖所有历史接口 | 本期只要求完成首批任务型接口清单，未接入项需记录后续排期。 |
| 新建独立 APM 平台 | 继续复用日志审计与 Task Trace 能力，不建设链路拓扑、采样平台或外部观测系统。 |
| 保存完整请求体 / 响应体 | 仅记录脱敏摘要、资源标识、错误码和必要诊断字段。 |
| 重构所有业务服务 | 仅围绕首批任务型接口做最小必要接入，不进行无关架构重写。 |
| 新增导入导出业务能力 | 可为已有或已规划导入导出任务接入追踪，不借本需求扩展导入导出功能本身。 |

## 5. 任务型接口判定标准

业务接口满足以下任一条件时，SHOULD 纳入 Task Trace 候选清单；满足多项或已暴露排障痛点时，MUST 优先纳入首批清单：

| 条件 | 示例 |
|---|---|
| 长耗时 | 大文件处理、复杂查询、批量保存、导入导出。 |
| 多步骤 | 保存 SKU 时同时处理基础信息、规格、价格、媒体、类目或品牌关联。 |
| 跨服务 / 外部依赖 | 调用对象存储、媒体处理、导出文件生成、消息队列或后台任务。 |
| 异步或后台任务 | 用户请求返回后仍有后续处理、轮询或状态查询。 |
| 批量处理 | 批量上下架、批量删除、批量导入、批量更新排序。 |
| 失败需精确定位 | 单条请求日志不足以判断失败节点、慢节点或部分成功明细。 |
| 安全审计价值高 | 影响商品、SKU、媒体、展示状态或大量业务数据的关键操作。 |

## 6. 功能要求

### FR-001 首批任务型接口梳理

- 系统 MUST 形成首批 Task Trace 接入接口清单。
- 清单 MUST 至少评估保存 SKU、批量操作、导入导出、媒体处理、异步任务和复杂查询六类场景。
- 每个候选接口 MUST 标注接入优先级、任务类型、关键步骤、预期 span、是否异步、是否涉及对象存储或批量资源。
- 未纳入首批的候选接口 MUST 记录原因和后续排期建议。
- 首批清单不得绕过评审直接进入实现，应在后续 `/req-complete` 与 OpenSpec Change 中细化。

### FR-002 task_trace_id 生成与透传

- 首批任务型接口 MUST 生成或接收 `task_trace_id`。
- 后端生成的 `task_trace_id` MUST 在响应、日志、审计事件和 span 中保持一致。
- 前端或子请求传入的 `task_trace_id` MUST 做格式校验，不得作为权限判断依据。
- 异步任务、后台任务和子请求 MUST 继承原始用户操作的 `task_trace_id`。
- 无法继承上下文时，系统 MUST 记录降级 span 或明确的关联缺失原因。

### FR-003 span 写入与上下文封装

- 系统 MUST 提供统一 Task Trace helper 或等价封装，减少业务服务重复埋点。
- helper SHOULD 支持上下文管理器、装饰器或显式 begin/end span 调用；具体形态在 OpenSpec design 中确定。
- 每个 span MUST 包含 `task_trace_id`、`span_name`、`status`、开始时间、结束时间或耗时。
- 每个 span SHOULD 包含 `request_id`、`actor_user_id`、`resource_type`、`resource_id`、错误码、摘要和脱敏 metadata。
- span 写入失败不得掩盖原业务错误；系统 MUST 有可观测性降级策略。

### FR-004 关键业务步骤覆盖

- 复杂保存类任务 MUST 覆盖参数校验、业务校验、主记录保存、关联资源保存、媒体关联、审计记录和响应阶段。
- 批量任务 MUST 覆盖批量解析、单项处理、成功 / 失败计数、部分失败摘要和最终结果阶段。
- 导入导出任务 MUST 覆盖文件接收或生成、解析、校验、持久化、结果文件生成和任务状态更新阶段。
- 媒体处理任务 MUST 覆盖校验、对象存储、元数据提取、后处理、数据库更新和失败回滚或补偿阶段。
- 复杂查询任务 SHOULD 覆盖查询条件解析、权限过滤、数据库查询、聚合统计和响应序列化阶段。

### FR-005 失败、超时与部分成功记录

- 任务失败时 MUST 写入失败 span，并记录统一错误码或失败摘要。
- 超时任务 MUST 能区分用户请求超时、后台处理超时和外部依赖超时。
- 批量任务出现部分成功时 MUST 记录成功数、失败数和失败分类摘要。
- 系统 SHOULD 能标识最慢 span 或超过阈值的慢节点。
- 错误 metadata MUST 做脱敏和长度限制，不得保存完整敏感请求体。

### FR-006 管理端任务标识展示

- 管理端发起复杂任务后 SHOULD 在成功、失败或处理中反馈中展示 `task_trace_id` 或提供复制入口。
- 错误提示 SHOULD 包含可供管理员或运维排障的追踪标识。
- 任务标识展示不得造成页面布局位移或移动端溢出。
- 如果任务没有 Task Trace，页面 MUST 保持现有交互，不显示空错误态。
- 复制入口应遵守现有 Design System 组件与交互反馈。

### FR-007 日志审计关联

- 首批任务型接口产生的请求日志、审计日志和任务 span MUST 能通过 `task_trace_id` 串联。
- 审计日志详情中的 Task Trace 时间线 SHOULD 能展示新增任务类型的 span。
- 日志列表或详情展示新增任务类型时，必须复用 `REQ-0069` 的权限和脱敏边界。
- 任务类型、状态、耗时、错误码等字段命名应与既有 Task Trace 模型保持一致。

### FR-008 API、数据与测试同步

- 若接口响应新增 `task_trace_id` 或任务摘要字段，MUST 同步 OpenAPI、Orval 和前端类型。
- 若新增或调整 Task Trace 存储字段，MUST 同步 SQLite / MySQL schema、数据库文档和迁移策略。
- 后端 MUST 为首批任务型接口补充单元或集成测试，验证 task_trace_id 生成、span 写入和失败节点记录。
- Web 管理端 SHOULD 补充复制追踪标识、错误提示展示或复杂任务反馈的最小测试。
- Docker Compose 验证是否需要执行，应在后续 OpenSpec tasks 中按实际涉及的后端、Web、对象存储或异步任务范围确定。

### FR-009 安全与脱敏

- Task Trace metadata MUST 不保存 Authorization、Cookie、AccessKey、SecretKey、数据库 DSN、`.env` 内容、真实客户数据或完整敏感请求体。
- 不得记录用户本地绝对路径、对象存储真实凭证或未授权直连地址。
- 资源 ID、任务类型、错误码和摘要必须经过长度限制和格式约束。
- 管理端查询与详情查看 MUST 复用系统管理员权限边界。
- 前端传入的追踪字段不得扩大可访问资源范围。

## 7. UI 约束

- 管理端应复用现有任务发起、列表、表单、抽屉、Toast 或 Alert 组件，不新增独立营销式页面。
- `task_trace_id` 展示应优先使用紧凑文本、复制按钮或详情入口，不应挤占主要业务操作区域。
- 错误态文案应清楚提示可复制追踪标识，但不得暴露内部路径、堆栈或敏感 metadata。
- 复杂查询或批量操作结果中如展示追踪标识，需保证表格、筛选区和移动端布局不溢出。
- UI 必须遵守 Design System semantic token，不得直接写裸 Hex。
- 需要复杂任务反馈原型时，在 `/req-complete` 阶段补充 prototype。

## 8. 关联需求

| 类型 | ID | 关系 |
|---|---|---|
| 父需求 | `REQ-0069-upload-observability-trace-logs` | 本需求在已落地的上传 Task Trace 基础上扩展到更多任务型业务接口。 |
| 关联能力 | `add-task-trace-audit-log-view` | 父需求已归档的 OpenSpec Change，提供 Task Trace 模型与日志审计查看基础。 |

## 9. 状态块

```yaml
requirement_id: REQ-0074-task-trace-coverage-expansion
status: in_sprint
lifecycle_stage: review
readiness: Ready
next_command: /opsx-apply update-task-trace-coverage-expansion
notes:
  - 已补齐 user-stories、business-flow、acceptance、trace 和复杂任务追踪标识反馈原型策略。
  - 2026-07-26 13:09:36 已评审通过，可进入 /req-opsx。
  - 2026-07-26 13:34:21 已创建 OpenSpec Change `update-task-trace-coverage-expansion`；实现前必须先纳入 Sprint。
  - 2026-07-26 15:34:18 已改纳入 `sprint-012`，可在 Sprint 编排下执行 `/opsx-apply update-task-trace-coverage-expansion`。
  - 后续必须明确首批接入任务型接口清单，并区分同步接口、异步任务与批量任务的 Task Trace 接入策略。
  - 如 API 响应、Task Trace 存储或管理端展示发生变化，后续 OpenSpec Change 必须同步 OpenAPI、Orval、DB 文档和测试。
```
