## ADDED Requirements

### Requirement: 真实用户页面性能采集
系统 SHALL 采集微信小程序、Web 管理端和店主 Web 展示端的真实用户页面加载性能事件，用于慢页面定位、版本性能回归分析和体验优化优先级判断。

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

### Requirement: 性能事件模型与隐私边界
系统 SHALL 使用统一性能事件模型承载 RUM 数据，并 SHALL 以白名单字段、长度限制和脱敏规则保护隐私与安全。

#### Scenario: 性能事件字段最小化
- **WHEN** 客户端生成性能事件
- **THEN** 事件 SHALL 至少包含 `client_type`、`page_key`、`app_version`、`network_type`、`device_class`、`metric_name`、`duration_ms`、`sample_rate` 和 `occurred_at`
- **AND** 服务端 SHALL 记录接收时间
- **AND** `page_key` SHALL 使用受控页面标识，不得使用包含敏感查询参数的完整 URL。
- **AND** Web 端 `app_version` SHALL 与管理端左上角产品版本徽标同源
- **AND** Web 端 SHALL 为每个 RUM 事件生成受控 `request_id`，用于管理端样本定位。

#### Scenario: 敏感字段禁止入库
- **WHEN** 性能事件 payload 包含 Authorization、Cookie、Token、签名 URL、手机号、openid、完整请求体、完整响应体、真实客户数据或内部路径
- **THEN** 服务端 SHALL 拒绝、移除或脱敏这些字段后再持久化
- **AND** SHALL NOT 将前端脱敏作为唯一安全边界。

#### Scenario: 字段校验与错误响应
- **WHEN** 性能事件缺少必填字段、枚举非法、字符串超长或 `duration_ms` 超出允许范围
- **THEN** 后端 SHALL 返回统一错误响应和文档化错误码
- **AND** 客户端 SHALL 将该失败视为监控降级，不得影响主业务流程。

### Requirement: 性能聚合查询
系统 SHALL 支持按端类型、页面、版本、网络、设备和时间范围聚合真实用户性能数据。

#### Scenario: 聚合基础指标
- **WHEN** 管理端或授权研发查询性能聚合数据
- **THEN** 系统 SHALL 返回样本量、平均耗时、最大耗时、P50、P75、P95、P99 或等价分位指标
- **AND** 聚合结果 SHALL 支持按端类型、页面 key、版本、网络类型、设备类别和时间范围过滤
- **AND** 聚合结果 SHALL 返回 `total`、`page`、`page_size` 和 `total_pages`，支持管理端后端真实分页。

#### Scenario: 慢页面与样本不足
- **WHEN** 聚合结果用于展示慢页面排行、慢指标排行或版本对比
- **THEN** 系统 SHALL 标识样本量
- **AND** 对低于统计阈值的结果 SHALL 标记样本不足
- **AND** 样本不足项 SHALL NOT 被当作可靠趋势结论。

#### Scenario: 管理端访问控制
- **WHEN** 用户访问性能聚合查询或管理端性能观测入口
- **THEN** 系统 SHALL 校验管理端权限
- **AND** 未授权用户 SHALL NOT 读取性能事件明细、聚合数据或内部排障信息。

#### Scenario: 管理端样本明细查询
- **WHEN** 管理员从性能观测页聚合行查看最近样本
- **THEN** 系统 SHALL 仅返回 `page_key`、指标名、耗时、版本、网络、设备、`request_id` 和事件/接收时间等受控字段
- **AND** 系统 SHALL NOT 返回完整 URL、Header、Cookie、签名 URL、raw payload、Authorization、Token 或用户隐私字段
- **AND** 管理端 SHALL 使用独立性能样本页承载样本明细，而非弹窗承载
- **AND** 样本明细 SHALL 支持后端真实分页，并返回 `total`、`page`、`page_size` 和 `total_pages`
- **AND** 管理端样本页 SHALL 复用日志审计页复制样式支持复制 `request_id`
- **AND** 样本明细 SHALL 归属于性能观测能力，而非日志审计查询。

### Requirement: 小程序真实环境性能证据
系统 SHALL 在小程序发布或验收时保留真实环境或体验版网络证据入口，避免仅以单次本地开发工具结果替代真实用户性能判断。

#### Scenario: 体验版证据标记
- **WHEN** 小程序 RUM 能力进入验收
- **THEN** 验收记录 SHALL 标明使用 DevTools、体验版或真实环境的证据来源
- **AND** 无法自动化验证的网络面板证据 SHALL 标记为人工来源
- **AND** 证据 SHALL NOT 包含真实用户隐私、Authorization、Cookie、Token 或签名 URL。
