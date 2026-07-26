## ADDED Requirements

### Requirement: Web 请求身份注入
Web 客户端 SHALL 在管理端与店主展示端 API 请求中注入统一客户端类型和客户端请求标识，用于后端日志归因。

#### Scenario: 管理端 API 请求注入身份
- **WHEN** Web 管理端发起受控 API 请求
- **THEN** 请求 SHALL 携带 `x-client-type=web_admin` 或等价文档化客户端类型字段
- **AND** 请求 SHALL 携带客户端请求标识
- **AND** 客户端请求标识生成失败 SHALL NOT 阻断主业务请求。

#### Scenario: 店主 Web 前台 API 请求注入身份
- **WHEN** 店主 Web 前台发起公开业务 API 请求
- **THEN** 请求 SHALL 携带 `x-client-type=web_catalog` 或等价文档化客户端类型字段
- **AND** 请求 SHALL 携带客户端请求标识
- **AND** 匿名访问 SHALL NOT 因客户端类型字段获得管理端权限或内部日志访问能力。

#### Scenario: Web 请求封装测试覆盖
- **WHEN** Web 测试运行
- **THEN** 测试 SHALL 覆盖管理端 API client 注入 `web_admin`
- **AND** 测试或等价 smoke SHALL 覆盖店主 Web API client 注入 `web_catalog`
- **AND** 测试 SHALL 覆盖客户端请求标识存在且不会覆盖 Authorization 逻辑。

### Requirement: 日志审计请求身份交互
Web 管理端 SHALL 在日志审计列表和详情中展示请求身份字段，并保持管理端列表页横切一致性。

#### Scenario: 日志审计列表展示请求身份字段
- **WHEN** admin 查看 `/admin/logs`
- **THEN** 页面 SHALL 展示客户端类型和后端可信 `request_id`
- **AND** 页面 SHALL 按 design 决策展示或隐藏客户端请求标识列
- **AND** 表格中的长 ID SHALL 单行截断，不得撑破表格布局。

#### Scenario: 日志详情抽屉展示请求身份字段
- **WHEN** admin 打开日志详情抽屉
- **THEN** 抽屉 SHALL 分组展示后端可信 `request_id`、客户端请求标识和 `x-request-id` 响应头语义
- **AND** 抽屉 SHALL 保持可关闭、可滚动和不丢失列表上下文。

#### Scenario: 请求 ID 复制反馈无布局位移
- **WHEN** admin 复制后端可信 `request_id` 或客户端请求标识
- **THEN** 页面 SHALL 使用 fixed toast 或等价不改变文档流的反馈
- **AND** 页面 SHALL NOT 使用文档流 notice 推挤 hero、筛选区或表格
- **AND** Clipboard API 不可用或写入失败时 SHALL 提供手动复制兜底。

#### Scenario: 管理端列表横切 AC 保持
- **WHEN** 本 Change 修改 `/admin/logs` 列表、指标卡、筛选区或分页
- **THEN** 分页 DOM SHALL 保持 `page-summary` 与 `page-right` 基准结构
- **AND** 指标卡 DOM SHALL 使用 `.metric-label`、`.metric-value` 与 `.metric-desc`
- **AND** 实现 SHALL NOT 引入 `window.confirm`。

### Requirement: 小程序普通 API 请求身份注入
微信小程序 SHALL 在统一 request 封装中为普通 API 请求注入客户端类型和客户端请求标识。

#### Scenario: 小程序普通 API 请求注入身份
- **WHEN** 微信小程序发起普通业务 API 请求
- **THEN** 请求 SHALL 携带 `x-client-type=wechat_miniapp` 或等价文档化客户端类型字段
- **AND** 请求 SHALL 携带客户端请求标识
- **AND** usage events 与普通 API 请求 SHALL 使用一致客户端类型枚举。

#### Scenario: 小程序 fallback 重试复用客户端请求 ID
- **WHEN** 小程序同一用户动作触发 fallback base URL 重试
- **THEN** 重试请求 SHALL 复用同一个客户端请求标识
- **AND** 后端每次 HTTP 请求 SHALL 仍生成独立可信 `request_id`。

#### Scenario: 小程序请求身份测试覆盖
- **WHEN** 小程序静态测试或 request 封装测试运行
- **THEN** 测试 SHALL 覆盖普通 API 请求注入 `wechat_miniapp`
- **AND** 测试 SHALL 覆盖 fallback 重试时客户端请求标识复用策略。
