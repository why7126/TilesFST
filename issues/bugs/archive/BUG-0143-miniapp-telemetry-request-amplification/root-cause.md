---
bug_id: BUG-0143-miniapp-telemetry-request-amplification
root_cause_status: confirmed
created_at: 2026-08-25 22:44:14
updated_at: 2026-08-25 22:44:14
category: design
---

# 根因分析

## 根因状态

`confirmed`

## 直接原因

小程序行为埋点 `track()` 复用了统一 API 请求函数 `request()` 上报 `/api/v1/usage-events`。统一请求函数会对每个 API 请求成功或失败自动调用 `reportPerformanceMetric()`，因此每条 usage-events 请求自身都会额外生成一条 `/api/v1/performance-events` 请求。

同时，商品卡组件在 `product` 属性 observer 中直接上报 `product_card_exposure`。首页首屏同时渲染新品、热销与全部产品列表，商品卡数量会直接转换为逐条 usage-events 请求，再被统一请求层转换为同等数量的 performance-events 请求。

## 根本原因

小程序埋点链路缺少“遥测请求边界”和“曝光事件批量/去重策略”：

- 统一 API 请求层没有区分业务请求与遥测请求，导致遥测请求也被 RUM 记录。
- usage 事件上报只有逐条接口消费方式，小程序端没有批量队列或 flush 机制。
- 商品卡曝光绑定在属性 observer 上，语义更接近“组件数据初始化/更新”，不是严格的“用户可见曝光”，缺少同一页面、同一模块、同一 SKU 的幂等去重。

## 触发条件

- 小程序冷启动进入首页。
- 首页成功请求 `/api/v1/miniapp/home` 并渲染 `new_products`、`hot_products`。
- 首页延迟触发瀑布流第一页 `/api/v1/miniapp/products?page=1&page_size=12` 并渲染 `allProducts`。
- 商品卡组件 `product` observer 被批量触发。
- `track()` 上报 usage-events 时继续走统一 `request()`。

## 证据链

| 证据类型 | 证据入口 | 摘要 |
|---|---|---|
| 用户复现 | `issues/bugs/archive/BUG-0143-miniapp-telemetry-request-amplification/capture.md` | 用户观察到启动小程序即产生约 28 条 performance-events 与 25 条 usage-events 请求。 |
| 代码定位 | `src/miniapp/services/api.ts` `track()` | `track()` 调用 `request('/api/v1/usage-events', ...)`，每条行为埋点都是独立 API 请求。 |
| 代码定位 | `src/miniapp/services/api.ts` `request()` success/fail | 统一请求成功或失败都会调用 `reportPerformanceMetric()` 上报 `api_duration` 或 `api_failed_duration`。 |
| 代码定位 | `src/miniapp/services/performance.ts` `reportPerformanceMetric()` | 每次性能指标调用都会立即 `wx.request` 到 `/api/v1/performance-events`，请求体虽支持 `events` 数组，但当前每次只发送 1 条。 |
| 代码定位 | `src/miniapp/components/product-card/index.ts` observer | `product, imageFallback` observer 中直接调用 `trackCard('product_card_exposure', normalized)`。 |
| 代码定位 | `src/backend/app/services/miniapp_home_service.py` `get_home()` | 首页聚合返回最多 6 个新品与 6 个热销商品。 |
| 代码定位 | `src/miniapp/pages/index/index.ts` 首页瀑布流 | 首页延迟加载第一页全部产品，前端默认 `PAGE_SIZE = 12`，并额外上报 `miniapp_home_waterfall_load`。 |
| 数量闭合 | 代码路径推导 | 25 条 usage-events 可由 12 个新品/热销卡片曝光、12 个瀑布流卡片曝光和 1 条瀑布流加载事件解释；28 条 performance-events 可由 25 条 usage 请求派生性能事件、1 条 app launch 性能事件、2 条首页业务 API 性能事件解释。 |

## 验证方式

修复前：

1. 冷启动小程序进入首页，观察网络面板。
2. 统计 `/api/v1/usage-events` 与 `/api/v1/performance-events` 请求数量。
3. 检查 performance-events 中 `page_key` 是否包含 `/api/v1/usage-events`，确认埋点请求被纳入 API duration。
4. 检查 usage-events 中 `product_card_exposure` 数量是否随首页卡片渲染数量增长。

修复后：

1. 冷启动小程序进入首页，`/api/v1/usage-events` 请求数量应显著下降，或变为批量 flush 后的少量请求。
2. `/api/v1/performance-events` 不应再记录 `/api/v1/usage-events` 自身的 API duration。
3. 首页业务 API 的 `api_duration` 仍应正常上报。
4. 同一页面、同一模块、同一 SKU 的商品卡曝光不应重复上报。

## 人工补证

当前根因已确认。若评审前需要补充可视化证据，可由测试人员执行：

1. 在微信开发者工具网络面板中冷启动首页，截图记录 usage-events 与 performance-events 请求数量。
2. 导出或人工记录 performance-events 请求体中的 `page_key` 分布，重点确认是否存在 `/api/v1/usage-events`。
3. 记录 usage-events 中 `event_name=product_card_exposure` 的数量，以及首页新品、热销、瀑布流首屏商品数量。
4. 所有证据只记录接口路径、事件名、数量和脱敏 request_id，不记录 Authorization header、Cookie、用户隐私或真实客户数据。
