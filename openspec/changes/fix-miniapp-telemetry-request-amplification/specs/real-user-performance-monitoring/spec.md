## MODIFIED Requirements

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
