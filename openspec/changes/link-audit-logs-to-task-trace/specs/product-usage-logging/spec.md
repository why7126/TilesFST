## ADDED Requirements

### Requirement: 审计日志任务链路关联

系统 SHALL 让审计操作日志支持可选 Task Trace 关联，使敏感操作可从 audit log 串联到主请求、任务节点和日志审计详情。

#### Scenario: 审计写入接口接收任务上下文
- **WHEN** 后端服务调用 `AuditLogRepository.insert()` 或等价审计写入入口并提供合法 `task_trace_id` 与 `task_type`
- **THEN** 系统 SHALL 将 `task_trace_id` 与 `task_type` 持久化到 `audit_logs`
- **AND** 审计基础字段、操作者、资源、动作、结果和脱敏 metadata SHALL 保持原有写入语义。

#### Scenario: 无任务上下文保持兼容
- **WHEN** 审计操作没有任务上下文或调用方未提供 `task_trace_id`
- **THEN** 系统 SHALL 正常写入审计日志
- **AND** `task_trace_id` 与 `task_type` SHALL 为空
- **AND** 日志列表、详情和权限行为 SHALL NOT 回归。

#### Scenario: 首批敏感操作清单
- **WHEN** 实现 REQ-0075
- **THEN** 系统 SHALL 梳理并记录首批审计写入点接入清单
- **AND** 清单 SHALL 至少评估系统设置、品牌证书、媒体或上传、SKU、Banner 等管理端敏感操作。

#### Scenario: 任务型审计操作复用任务标识
- **WHEN** 敏感操作发生在已有 Task Trace 上下文中
- **THEN** 审计日志 SHALL 复用当前请求或任务上下文中的 `task_trace_id`
- **AND** 同一业务任务触发的多条审计日志 SHALL 可通过同一个 `task_trace_id` 关联。

#### Scenario: 审计日志任务查询使用结构化字段
- **WHEN** admin 使用 `task_trace_id` 查询 audit 类型日志
- **THEN** 系统 SHALL 使用结构化字段和索引友好条件查询
- **AND** 系统 SHALL NOT 以 metadata 无界模糊扫描作为主查询路径。

#### Scenario: audit 类型日志详情展示任务链路
- **WHEN** admin 打开一条存在 `task_trace_id` 的 audit 类型日志详情
- **THEN** 日志详情 SHALL 展示 Task Trace 分组或等价任务链路入口
- **AND** 分组 SHALL 包含 `task_trace_id`、`task_type`、任务状态、关键节点摘要或任务时间线。

#### Scenario: 任务字段不参与权限判断
- **WHEN** 前端或客户端提交 `task_trace_id`、`task_type` 或资源相关字段
- **THEN** 系统 SHALL NOT 将这些字段作为权限判断依据
- **AND** 权限判断 SHALL 继续基于认证上下文、角色和服务端资源校验。

#### Scenario: 审计 metadata 安全脱敏
- **WHEN** 系统写入或展示带 Task Trace 的 audit log metadata
- **THEN** metadata SHALL 过滤 Authorization、Cookie、Token、密码、AccessKey、SecretKey、数据库 DSN、`.env` 内容、内部绝对路径和真实客户数据
- **AND** 审计写入失败或 Task Trace 关联失败 SHALL NOT 泄露内部路径、堆栈、对象存储凭证或未脱敏 metadata。

#### Scenario: 审计字段 schema 一致
- **WHEN** 实现或验证审计日志任务链路关联
- **THEN** SQLite demo 与 MySQL production 的 `audit_logs` SHALL 均包含兼容的 `task_trace_id` 与 `task_type` 字段
- **AND** 若 schema 或索引不一致，系统 SHALL 同步 schema、migration、数据库文档和测试。

#### Scenario: 契约与生成物同步
- **WHEN** 日志列表或详情 API 为 audit 类型日志新增或确认任务摘要字段
- **THEN** OpenAPI SHALL 暴露相关字段
- **AND** Orval SHALL 生成或更新对应 Web client types
- **AND** generated files SHALL NOT be hand-edited。

### Requirement: 审计日志任务链路管理端横切验收

系统 SHALL 在管理端日志审计页面实现 audit log Task Trace 展示时遵守管理端列表页一致性与 REQ-0075 原型策略。

#### Scenario: 分页 DOM 对齐管理端基准
- **WHEN** 日志审计列表新增或调整 `task_trace_id` 展示、筛选或复制能力
- **THEN** 分页 DOM SHALL 对齐用户管理基准
- **AND** 左侧 SHALL 使用 `.page-summary`
- **AND** 右侧 SHALL 使用 `.page-right` 页码与每页条数组合。

#### Scenario: 指标卡 DOM 保持一致
- **WHEN** 日志审计指标摘要因任务链路新增或调整
- **THEN** 指标卡 SHALL 使用 `.metric-label`、`.metric-value`、`.metric-desc` 结构
- **AND** SHALL NOT 仅复用外层卡片后用裸 `strong` 或 `span` 承载数值与说明。

#### Scenario: 复制和查询反馈不造成布局位移
- **WHEN** admin 查询、复制 `task_trace_id` 或打开日志详情
- **THEN** 成功、失败或兜底反馈 SHALL 使用 fixed toast 或等价固定层
- **AND** 页面头部、筛选区、指标区和表格 SHALL NOT 因反馈产生纵向位移。

#### Scenario: 不使用 window confirm
- **WHEN** 实现日志审计列表和详情中的 Task Trace 操作
- **THEN** Web client SHALL NOT 调用 `window.confirm`
- **AND** 若后续新增清理、删除、导出等危险操作，系统 SHALL 使用 Design System confirm modal。

#### Scenario: 日志页 smoke 覆盖任务分组
- **WHEN** 实现完成
- **THEN** Web 测试或 smoke SHALL 覆盖 1440x1024 与移动端管理端视口下的分页、筛选、复制反馈和详情抽屉 Task Trace 分组
- **AND** UI SHALL 使用 Design System semantic token。
