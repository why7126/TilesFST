## 根因结论

BUG-0143 的根因状态为 `confirmed`。小程序 `track()` 使用统一 `request()` 调用 `/api/v1/usage-events`，统一请求层对每个 API 成功或失败自动上报 `/api/v1/performance-events`，因此每条 usage 请求都会派生一条 performance 请求。商品卡曝光又在 `product` 属性 observer 中逐条上报，首页首屏多模块卡片渲染会把组件初始化数量直接转换为 usage 请求数量。

## 修复方案

### 遥测请求边界

统一请求封装需要支持请求级 `skipPerformanceTracking`、`telemetry` 或等价内部标记。`track()`、`reportPerformanceMetric()` 以及其他遥测上报调用应使用该标记，确保发送 `/api/v1/usage-events` 和 `/api/v1/performance-events` 时不再记录这些请求自身的 `api_duration` 或 `api_failed_duration`。

普通业务 API 仍默认采集性能指标，不要求调用方逐个显式开启。性能事件失败、usage 事件失败和批量 flush 失败都只能静默降级或记录受控本地状态，不得影响首页加载与商品浏览。

### 商品卡曝光控制

商品卡曝光需要从“属性 observer 触发即上报”收敛为“用户可见曝光语义下的受控上报”。实现可选择以下等价策略之一：

- 端侧维护同一页面、同一 `sourceModule`、同一 `listContext`、同一 `skuId` 的曝光去重集合。
- 将 `product_card_exposure` 事件进入 usage 队列，按短延迟、数量阈值、页面隐藏或卸载 flush。
- 对 observer 初始化触发保留一次首曝，但重复属性更新不得重复发送同一曝光事件。

若当前后端只接受单事件 usage API，端侧可以在 flush 时串行或并发受控发送少量请求；如实现后端批量 API，需同步 schema、OpenAPI、Orval、API 文档和测试。

## 测试策略

- 小程序单元或静态测试覆盖 `track()` 上报 usage 时不会触发 `reportPerformanceMetric()`。
- 小程序请求封装测试覆盖普通业务请求仍会触发 `api_duration`，失败请求仍会触发 `api_failed_duration`。
- 商品卡组件或曝光 helper 测试覆盖重复 observer、重复数据更新、同 SKU 不同模块和不同列表上下文的去重边界。
- 后端 usage event 字典测试继续覆盖 `product_card_exposure`、`miniapp_home_waterfall_load` 的合法字段、未知事件拒绝和禁止字段拒绝。
- 人工或自动化网络证据覆盖小程序冷启动首页，请求数量显著低于 BUG-0143 记录的 28 条 performance-events 与 25 条 usage-events，且 `/api/v1/performance-events` 中不再出现 `/api/v1/usage-events` 自身的样本。

## 风险与边界

- 只过滤遥测请求而不处理商品卡曝光，会保留 usage 请求线性膨胀风险。
- 只处理曝光去重而不过滤 usage 的 RUM，会继续污染 performance 数据。
- 本 Change 不要求接入外部 APM、BI、实时大屏、告警平台或管理端分析页。
- 不记录 Authorization header、Cookie、手机号、`.env` 内容、本机路径、对象存储原始 key 或真实客户隐私。
