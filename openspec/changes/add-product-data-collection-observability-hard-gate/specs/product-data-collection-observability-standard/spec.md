## ADDED Requirements

### Requirement: 产品数据采集与链路观测规范硬门禁
系统 SHALL 将 `docs/standards/product-data-collection-observability.md` 接入项目治理入口、规则、技能和实现级校验，使 API、DB、日志审计、行为埋点、Task Trace、Web 请求封装、小程序请求封装和 App 请求封装相关变更必须读取、声明、验证并验收该规范。

#### Scenario: 任务入口路由到采集规范
- **WHEN** 变更涉及 API、DB / 数据模型、日志审计、行为埋点、Task Trace、Web 请求封装、小程序请求封装或 App 请求封装
- **THEN** `AGENTS.md` SHALL 将 `docs/standards/product-data-collection-observability.md` 列为追加读取材料
- **AND** 完成检查清单 SHALL 要求报告门禁适用性、N/A 原因和验证结果。

#### Scenario: 规则文件声明触发条件
- **WHEN** 相关规则约束 API、数据库、测试、文档治理、需求管理、Sprint 或 OpenSpec 流程
- **THEN** 规则 SHALL 声明采集规范门禁触发条件
- **AND** SHALL 要求触发范围内的变更记录 `product_data_collection_observability` 或等价固定声明
- **AND** SHALL 避免复制完整采集规范正文。

#### Scenario: 技能检查清单执行门禁
- **WHEN** req、opsx 或 sprint 技能处理触发范围内的 REQ、BUG、Change 或 Sprint
- **THEN** 技能 SHALL 检查是否已读取采集规范
- **AND** SHALL 要求记录适用层级、N/A 原因、验证计划或验收结果
- **AND** SHALL 在缺少声明或验收证据时输出可执行修复路径。

### Requirement: 采集规范适用性声明可审计
系统 SHALL 为需求、OpenSpec Change、Sprint 验收和实现校验提供可审计的采集规范适用性声明格式。

#### Scenario: 适用声明包含固定字段
- **WHEN** 需求或 Change 命中采集规范门禁触发范围
- **THEN** 文档 SHALL 记录 `product_data_collection_observability`
- **AND** SHALL 包含适用状态、`affected_layers`、`reason` 和 `validation`
- **AND** 适用层级 SHALL 覆盖命中的 API、database、request_logs、usage_events、task_trace、web_request_wrapper、miniapp_request_wrapper、app_request_wrapper 或 workflow_governance。

#### Scenario: N/A 原因可审计
- **WHEN** 需求或 Change 声明采集规范不适用
- **THEN** 声明 SHALL 使用 `status: not_applicable` 或等价明确状态
- **AND** `reason` SHALL 说明为什么不影响 API、DB、日志审计、行为埋点、Task Trace 或端请求封装
- **AND** SHALL NOT 仅使用“无”“不涉及”作为不适用说明。

#### Scenario: 输出摘要不膨胀
- **WHEN** workflow 命令、校验脚本或验收材料报告采集规范门禁状态
- **THEN** 输出 SHALL 只包含门禁状态、适用层级、N/A 原因、缺失项或校验命令摘要
- **AND** SHALL NOT 输出完整采集规范正文、完整 Workflow Sync 派生块、敏感日志、密钥、Cookie、Authorization header、真实客户数据或本机绝对路径。

### Requirement: 采集规范门禁实现级校验
系统 SHALL 提供实现级校验脚本，检查采集规范门禁入口、规则、技能和 active Change 声明。

#### Scenario: 校验治理入口完整性
- **WHEN** 运行采集规范门禁校验脚本
- **THEN** 脚本 SHALL 检查 `AGENTS.md`、相关 `rules/` 和 req / opsx / sprint 技能文件是否引用 `docs/standards/product-data-collection-observability.md`
- **AND** SHALL 检查是否包含必读、必声明、必验收、N/A 原因和实现级验证要求。

#### Scenario: 校验目标触发范围和声明
- **WHEN** 校验脚本按 Change、REQ、Sprint 或当前 diff 聚焦运行
- **THEN** 脚本 SHALL 通过路径级和语义级规则识别 API、DB、日志审计、行为埋点、Task Trace 或端请求封装触发范围
- **AND** 命中触发范围时 SHALL 检查目标材料是否存在 `product_data_collection_observability` 或等价固定声明
- **AND** SHALL 报告缺失文件、缺失字段、触发依据和修复建议。

#### Scenario: 默认扫描范围受控
- **WHEN** 未显式要求历史审计
- **THEN** 校验脚本 SHALL 聚焦 active Change、指定 REQ、指定 Sprint 或当前 diff
- **AND** SHALL NOT 默认扫描全部历史 archive
- **AND** SHALL NOT 读取或输出 `.env`、真实客户数据、运行时数据库、密钥、Authorization header、Cookie 或本机绝对路径。

### Requirement: 后续 API DB 与端请求封装变更受门禁约束
系统 SHALL 要求后续具体变更在影响 API contract、DB schema、日志审计、行为事件、Task Trace 或端请求封装时同步对应治理资产和测试，或记录明确不适用依据。

#### Scenario: API contract 变化同步治理
- **WHEN** 后续 Change 修改请求头、请求日志字段、响应字段、错误码、OpenAPI contract 或 Orval 生成输入
- **THEN** Change SHALL 读取采集规范并声明 API 与请求日志影响
- **AND** SHALL 同步 OpenAPI、Orval、API 文档和测试
- **AND** 若不需要同步 SHALL 记录具体 N/A 原因。

#### Scenario: DB 结构或保留周期变化同步治理
- **WHEN** 后续 Change 修改 `usage_events`、`request_logs`、`task_traces`、`task_trace_spans`、索引、迁移或保留周期
- **THEN** Change SHALL 读取采集规范并声明 database、request_logs、usage_events 或 task_trace 影响
- **AND** SHALL 同步 SQLite / MySQL schema、迁移、数据库文档和测试
- **AND** 若不适用 SHALL 记录具体 N/A 原因。

#### Scenario: 端请求封装和行为埋点变化同步治理
- **WHEN** 后续 Change 修改 Web、小程序或 App 请求封装、行为埋点、链路 ID 透传、离线重试或错误摘要
- **THEN** Change SHALL 读取采集规范并声明对应端侧 affected layer
- **AND** SHALL 说明 `behavior_trace_id`、`behavior_event_id`、`client_request_id` 或等价字段的生成、透传、脱敏和验证策略
- **AND** 若仓库未承载某端实现 SHALL 记录具体 N/A 原因。
