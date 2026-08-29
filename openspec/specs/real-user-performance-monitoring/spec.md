# real-user-performance-monitoring Specification

## Purpose
TBD - created by archiving change add-real-user-page-load-rum. Update Purpose after archive.
## Requirements
### Requirement: 真实用户页面性能采集

系统 SHALL 采集微信小程序、Web 管理端和店主 Web 展示端的真实用户页面加载性能事件，用于慢页面定位、版本性能回归分析和体验优化优先级判断。小程序端 SHALL 区分业务请求与遥测上报请求，遥测上报请求 SHALL NOT 被再次记录为接口耗时类 RUM 样本。

#### Scenario: Web 页面采集首屏可用指标
- **WHEN** Web 管理端或店主 Web 展示端用户进入受控页面
- **THEN** 客户端 SHALL 采集页面导航、首屏可用、完整加载、关键接口或关键资源的受控性能指标
- **AND** 性能事件 SHALL 区分 `web_admin` 与 `web_catalog`
- **AND** Web 端 SHALL 在浏览器支持网络类型 API 时采集网络类型；浏览器不支持时允许显示为未知
- **AND** 上报失败 SHALL NOT 阻断页面加载、筛选、列表、详情、上传或管理操作主流程。

#### Scenario: 小程序页面采集生命周期指标
- **WHEN** 微信小程序用户进入受控页面
- **THEN** 小程序 SHALL 采集页面进入、`onLoad`、`onShow`、`onReady`、首个关键接口完成、首屏渲染就绪或页面可交互的性能指标
- **AND** 小程序 SHALL NOT 依赖 Web 浏览器专属 API
- **AND** 小程序 SHALL 使用微信网络状态能力采集 `network_type`，仅在获取失败时上报 `unknown`
- **AND** 上报失败 SHALL NOT 阻断首页、品牌、商品列表、搜索、详情或收藏等主流程。

#### Scenario: 采样与降级
- **WHEN** RUM 采集启用
- **THEN** 端侧 SHALL 支持默认采样、批量上报、节流或等价压力控制策略
- **AND** 当采样关闭、上报超时、服务端限流或网络异常时，客户端 SHALL 静默降级或记录受控本地状态
- **AND** 普通用户 SHALL NOT 看到内部监控错误详情。

#### Scenario: 小程序遥测请求不触发接口耗时 RUM
- **WHEN** 小程序端发送 `/api/v1/usage-events`、`/api/v1/performance-events` 或等价遥测上报请求
- **THEN** 小程序 SHALL NOT 为该请求生成 `api_duration` 或 `api_failed_duration` 性能事件
- **AND** `/api/v1/performance-events` 中 SHALL NOT 出现 `page_key` 指向 `/api/v1/usage-events` 或 `/api/v1/performance-events` 的样本
- **AND** 遥测上报成功、失败、超时或降级 SHALL NOT 阻断首页加载、商品卡展示、搜索、分享或详情跳转。

#### Scenario: 小程序业务接口性能观测保留
- **WHEN** 小程序冷启动首页并调用 `/api/v1/miniapp/home`、`/api/v1/miniapp/products` 或其他业务 API
- **THEN** 小程序 SHALL 继续为业务请求上报 `api_duration`
- **AND** 业务 API 请求失败时 SHALL 继续按既有策略上报 `api_failed_duration`
- **AND** `app_launch_ready` 性能事件 SHALL 继续上报。

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

### Requirement: 小程序真实环境性能证据
系统 SHALL 在小程序发布或验收时保留真实环境或体验版网络证据入口，避免仅以单次本地开发工具结果替代真实用户性能判断。

#### Scenario: 体验版证据标记
- **WHEN** 小程序 RUM 能力进入验收
- **THEN** 验收记录 SHALL 标明使用 DevTools、体验版或真实环境的证据来源
- **AND** 无法自动化验证的网络面板证据 SHALL 标记为人工来源
- **AND** 证据 SHALL NOT 包含真实用户隐私、Authorization、Cookie、Token 或签名 URL。

### Requirement: 管理端性能观测空态展示

管理端性能观测列表 SHALL 在无聚合数据时提供与管理端表格体验一致的空态展示。

#### Scenario: 聚合列表没有性能样本
- **WHEN** 管理员进入性能观测页或筛选后没有匹配的聚合数据
- **THEN** 聚合列表 SHALL 显示“暂无性能样本”或等价空态文案
- **AND** 空态 SHALL 使用表格内空态样式，字号、颜色、间距、最小高度和对齐方式 SHALL 与管理端列表保持一致
- **AND** 空态 SHALL NOT 使用过大的标题字号或造成表格布局跳动。

