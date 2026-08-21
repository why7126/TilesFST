## MODIFIED Requirements

### Requirement: 性能事件模型与隐私边界

系统 SHALL 使用统一性能事件模型承载 RUM 数据，并 SHALL 以白名单字段、长度限制和脱敏规则保护隐私与安全。

#### Scenario: 性能事件字段最小化
- **WHEN** 客户端生成性能事件
- **THEN** 事件 SHALL 至少包含 `client_type`、`page_key`、`app_version`、`network_type`、`device_class`、`metric_name`、`duration_ms`、`sample_rate` 和 `occurred_at`
- **AND** 服务端 SHALL 记录接收时间
- **AND** `page_key` SHALL 使用受控页面标识，不得使用包含敏感查询参数的完整 URL。
- **AND** Web 端 `app_version` SHALL 与管理端左上角产品版本徽标同源
- **AND** 小程序端 `app_version` SHALL 使用与 Web 管理后台一致的产品版本号口径
- **AND** 小程序端 SHALL NOT 将 `production`、`development`、`dev` 或其他运行环境名作为 `app_version` 上报
- **AND** Web 端 SHALL 为每个 RUM 事件生成受控 `request_id`，用于管理端样本定位
- **AND** 小程序端 SHALL 为每个 RUM 事件生成或传递受控 `request_id`，接口耗时指标 SHOULD 复用统一 API 封装的请求追踪标识
- **AND** 小程序端开发环境 API 配置 SHALL 由根目录 `.env` 的 `HOST_PORT_BACKEND` 生成 dev `apiBaseUrl` 与 fallback，缺失或非法时退回 `.env.example` 与默认 `8000`
- **AND** 小程序端 RUM 上报 SHALL 复用小程序 API 的开发环境 baseUrl 与 fallback 策略；当前 baseUrl 连接失败或返回 5xx 时 SHALL 尝试下一个 fallback，4xx 校验错误 SHALL 停止重试
- **AND** 小程序端 RUM fallback 返回 2xx 后 SHOULD 缓存该可用 baseUrl，并在后续 RUM 上报中优先使用它。

### Requirement: 性能聚合查询

系统 SHALL 支持按端类型、页面、版本、网络、设备和时间范围聚合真实用户性能数据。

#### Scenario: 聚合基础指标
- **WHEN** 管理端或授权研发查询性能聚合数据
- **THEN** 系统 SHALL 返回样本量、平均耗时、最大耗时、P50、P75、P95、P99 或等价分位指标
- **AND** 聚合结果 SHALL 支持按端类型、页面 key、版本、网络类型、设备类别和时间范围过滤
- **AND** 聚合结果 SHALL 返回 `total`、`page`、`page_size` 和 `total_pages`，支持管理端后端真实分页
- **AND** 管理端聚合列表 SHALL 展示完整分组键，至少包含页面 key、版本、端类型、指标、网络类型和设备类别
- **AND** 管理端从聚合行查看样本时 SHALL 携带同一分组上下文，避免隐藏分组维度导致不同聚合组被误判为重复项。

#### Scenario: 管理端样本明细查询
- **WHEN** 管理员从性能观测页聚合行查看最近样本
- **THEN** 系统 SHALL 仅返回 `page_key`、指标名、耗时、版本、网络、设备、`request_id` 和事件/接收时间等受控字段
- **AND** 系统 SHALL NOT 返回完整 URL、Header、Cookie、签名 URL、raw payload、Authorization、Token 或用户隐私字段
- **AND** 管理端 SHALL 使用独立性能样本页承载样本明细，而非弹窗承载
- **AND** 样本明细 SHALL 支持后端真实分页，并返回 `total`、`page`、`page_size` 和 `total_pages`
- **AND** 管理端样本页 SHALL 复用日志审计页复制样式支持复制 `request_id`
- **AND** 管理端聚合页、指标筛选和样本页 SHALL 对小程序指标显示可读中文标签
- **AND** 小程序指标至少 SHALL 包含 `app_launch_ready`、`api_duration` 和 `api_failed_duration` 的中文展示名称
- **AND** 样本明细 SHALL 归属于性能观测能力，而非日志审计查询。

## ADDED Requirements

### Requirement: 管理端性能观测空态展示

管理端性能观测列表 SHALL 在无聚合数据时提供与管理端表格体验一致的空态展示。

#### Scenario: 聚合列表没有性能样本
- **WHEN** 管理员进入性能观测页或筛选后没有匹配的聚合数据
- **THEN** 聚合列表 SHALL 显示“暂无性能样本”或等价空态文案
- **AND** 空态 SHALL 使用表格内空态样式，字号、颜色、间距、最小高度和对齐方式 SHALL 与管理端列表保持一致
- **AND** 空态 SHALL NOT 使用过大的标题字号或造成表格布局跳动。
