---
purpose: BUG-0144 小程序 usage-events 过量上报修复证据
content: 记录列表曝光口径、搜索输入频控、商品卡曝光去重和测试结论
source: /opsx-apply BUG-0144-miniapp-usage-events-overreporting
created_at: 2026-08-26 09:50:30
updated_at: 2026-08-26 10:02:13
---

# 实现证据

## 修复前风险

- 商品列表页 `loadProducts()` 成功后调用 `trackItems()`，对首屏前 12 个商品逐条发送 `product_list_item_exposure`。
- 同一批商品还通过 `product-card` observer 进入 `product_card_exposure` 聚合队列，形成列表页页面级曝光与组件级曝光双口径。
- 搜索页 `onInput()` 每次输入变化即时发送 `search_input`，但搜索建议请求才具备 300ms 防抖。
- 商品卡曝光去重键未包含 `keyword` 与 `requestId`，同一 SKU 在不同关键词或不同请求上下文下的去重窗口不够清晰。

## 修复后口径

- 商品列表页移除首屏逐条 `product_list_item_exposure` 调用，SKU 级曝光以 `product-card` 的 `product_card_exposure` 为主口径。
- 后端事件字典继续保留 `product_list_item_exposure`，用于兼容历史数据和后续明确列表级语义，不新增后端 API。
- `product_card_exposure` 去重键和批量键包含 `page_path`、`sourcePage`、`sourceModule`、`listContext`、`keyword`、`requestId` 和 `skuId`。
- 搜索页新增 `inputTrackTimer` 与 `scheduleSearchInputTrack()`，连续输入只在 300ms 防抖窗口结束后发送一次 `search_input`。
- 清空关键词会清除 pending 输入埋点，并发送 `inputAction: clear` 的受控 `search_input`；提交搜索会清除 pending 输入埋点并保留 `search_submit`。
- `search_result_exposure` 保留为结果集合语义，SKU 卡片曝光仍由商品卡主口径负责。

## 验证结果

| 验证项 | 结果 | 证据 |
|---|---|---|
| 小程序 JS 语法检查 | pass | `node --check src/miniapp/components/product-card/index.js`、`node --check src/miniapp/pages/product-list/index.js`、`node --check src/miniapp/pages/search/index.js` |
| 小程序静态测试 | pass | `uv run pytest tests/test_miniapp_static.py -q`，37 passed |
| 后端 usage event 字典测试 | pass | `uv run pytest tests/test_miniapp_home.py -q -k "usage_events_validate_dictionary or contract_drift_usage_events"`，8 selected passed |
| API / Orval / DB | pass | 本实现未新增或调整 API，沿用 `POST /api/v1/usage-events`；不涉及 Orval、数据库结构或 Docker Compose。 |
| 微信开发者工具 Network 截图 | pass | 见 `issues/bugs/review/BUG-0144-miniapp-usage-events-overreporting/screenshots/20260826095600-product-list-usage-events.png`、`20260826095610-search-input-usage-events.png`、`20260826095620-search-result-usage-events.png`。 |

## 人工网络证据

| 场景 | 截图 | 观察摘要 |
|---|---|---|
| 商品列表页首屏 | `issues/bugs/review/BUG-0144-miniapp-usage-events-overreporting/screenshots/20260826095600-product-list-usage-events.png` | Network 过滤 `events` 后显示 usage-events 请求数量受控，列表 SKU 曝光不再按首屏商品逐条线性铺满请求列表。 |
| 搜索连续输入 | `issues/bugs/review/BUG-0144-miniapp-usage-events-overreporting/screenshots/20260826095610-search-input-usage-events.png` | 输入关键词后 Network 中 usage-events 与 performance-events 数量受控，未表现为逐字符即时上报的线性放大。 |
| 搜索结果展示 | `issues/bugs/review/BUG-0144-miniapp-usage-events-overreporting/screenshots/20260826095620-search-result-usage-events.png` | 搜索结果页显示 48 条 SKU 结果，Network 中 events 请求数量保持低位，搜索结果集合曝光与商品卡曝光边界可验收。 |
