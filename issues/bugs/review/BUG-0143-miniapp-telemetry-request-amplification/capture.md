---
bug_id: BUG-0143-miniapp-telemetry-request-amplification
status: captured
created_at: 2026-08-25 22:34:46
updated_at: 2026-08-25 22:34:46
severity_hint: medium
environment: local
related_requirement:
related_bug:
lifecycle_stage: plan
---

# 现象

启动微信小程序后，网络面板短时间内出现大量埋点请求：约 28 条 `/api/v1/performance-events` 请求与 25 条 `/api/v1/usage-events` 请求。

# 复现步骤

1. 启动本地后端服务与微信小程序开发环境。
2. 打开微信开发者工具并进入小程序首页。
3. 清空或观察网络面板中启动阶段的请求。
4. 统计 `/api/v1/performance-events` 与 `/api/v1/usage-events` 请求数量。
5. 对比首屏业务请求数量、商品卡片曝光数量与埋点请求数量。

# 期望 vs 实际

- 期望：小程序启动和首页首屏加载阶段只产生必要的业务请求与少量聚合埋点；埋点请求自身不应继续触发性能埋点，卡片曝光应去重、采样或批量上报，避免请求数量随卡片数量线性膨胀。
- 实际：启动首页后产生 28 条 performance-events 与 25 条 usage-events 请求，疑似存在埋点请求被统一 API 性能监控再次上报，以及商品卡曝光逐条上报导致的请求放大。

# 影响范围

- 微信小程序启动、首页首屏加载、首页商品推荐与瀑布流展示。
- `/api/v1/usage-events` 行为埋点数据质量。
- `/api/v1/performance-events` RUM 性能数据质量。
- 本地、测试或生产环境中的网络请求噪音、服务端日志量、数据库写入量和性能观测报表口径。

# 初步线索

- `src/miniapp/services/api.ts` 的 `track()` 通过统一 `request()` 上报 `/api/v1/usage-events`。
- 同一文件的 `request()` 会对每个 API 成功或失败调用 `reportPerformanceMetric()`，因此 usage 埋点请求本身会再派生 performance 埋点。
- `src/miniapp/app.ts` 启动时会主动上报 `app_launch_ready` 性能事件。
- `src/miniapp/pages/index/index.ts` 首页加载会请求 `/api/v1/miniapp/home`，并延迟触发 `/api/v1/miniapp/products?page=1&page_size=12`。
- `src/miniapp/components/product-card/index.ts` 在 `product` observer 中上报 `product_card_exposure`，首页同时渲染新品、热销和全部产品卡片时，usage-events 数量会随卡片数量增加。

# 建议验收或复现要点

- [ ] 小程序冷启动进入首页时，`/api/v1/usage-events` 不再因商品卡属性初始化产生大量逐条请求，或已改为批量、去重、采样后的可控数量。
- [ ] `/api/v1/usage-events` 请求本身不再派生 `/api/v1/performance-events`，避免埋点自我放大。
- [ ] 首页业务 API 的 `api_duration` 仍可正常上报，非埋点业务请求的性能观测不退化。
- [ ] 商品卡曝光事件不重复上报同一 SKU、同一模块、同一首屏渲染上下文。
- [ ] 埋点失败仍不阻断小程序浏览、搜索、商品点击或分享。

# 附件

- 暂无。
