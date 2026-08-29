---
bug_id: BUG-0144-miniapp-usage-events-overreporting
root_cause_status: confirmed
root_cause_category: design
created_at: 2026-08-26 08:38:14
updated_at: 2026-08-26 08:38:14
---

# 根因状态

`confirmed`

# 直接原因

小程序商品列表页与搜索页存在多套可同时触发的曝光和输入埋点口径，且其中部分高频事件缺少统一的防抖、合并或跨场景去重策略。

具体表现为：

- 商品列表页在接口加载成功后，对前 12 个商品逐条上报 `product_list_item_exposure`。
- 同一商品列表页同时使用 `product-card` 组件渲染商品卡，组件在 `product` observer 触发时又进入 `product_card_exposure` 聚合队列。
- 搜索页 `search_input` 在每次输入变化时立即调用 `track()`，而搜索建议请求本身才使用 300ms 防抖。
- 搜索结果页在结果加载成功时上报 `search_result_exposure`，结果中的 SKU 卡片继续通过 `product-card` 上报 `product_card_exposure`，两者边界未明确互斥。

# 根本原因

BUG-0143 的修复重点是阻断遥测请求自我触发 RUM，并聚合首页商品卡曝光；但商品列表页、搜索页和通用商品卡组件之间尚未建立统一的行为埋点口径治理规则。

当前设计同时保留了页面级曝光、组件级曝光和搜索结果级曝光，缺少以下约束：

- 页面级曝光和组件级曝光哪个是主口径。
- 搜索输入是否允许逐字符上报。
- 同一 SKU 在同一页面、同一模块、同一 `requestId` 或同一列表实例中的曝光去重窗口。
- 列表刷新、分页、筛选切换、搜索结果切换时去重窗口如何重置。

# 触发条件

满足任一条件即可触发 usage-events 偏多：

1. 进入商品列表页并加载首屏商品，页面逻辑触发 `product_list_item_exposure`，商品卡组件同时触发 `product_card_exposure`。
2. 在搜索页连续输入关键词，每次输入变化即时触发 `search_input`。
3. 搜索结果页展示 SKU 商品卡时，结果级 `search_result_exposure` 与卡片级 `product_card_exposure` 同时存在。
4. 商品列表或搜索结果发生刷新、分页、筛选切换时，旧曝光和新曝光之间缺少清晰的去重窗口说明。

# 证据链

| 证据类型 | 证据入口 | 说明 |
|---|---|---|
| 代码定位 | `src/miniapp/pages/product-list/index.ts` `loadProducts()` / `trackItems()` | 列表加载成功后调用 `this.trackItems(merged)`，`trackItems()` 对 `items.slice(0, 12)` 逐条调用 `trackListEvent('product_list_item_exposure', ...)`。 |
| 代码定位 | `src/miniapp/pages/product-list/index.wxml` 商品卡渲染 | 商品列表页使用 `<product-card wx:for="{{items}}">` 渲染同一批商品，并传入 `source-page="product-list"`、`request-id="{{requestId}}"`。 |
| 代码定位 | `src/miniapp/components/product-card/index.ts` `observeProduct()` / `queueProductCardExposure()` | 商品卡 `product` observer 调用 `trackCardExposure()`，最终队列 flush 时上报 `product_card_exposure`。 |
| 代码定位 | `src/miniapp/pages/search/index.ts` `onInput()` | 搜索页每次输入变化都会立即调用 `track('search_input', ...)`；同函数内仅建议请求 `loadSuggestions()` 使用 `DEBOUNCE_MS` 延迟。 |
| 代码定位 | `src/miniapp/pages/search/index.ts` `loadResults()` | 搜索结果加载成功后上报 `search_result_exposure` 或 `search_no_result`，结果 SKU 同时在 WXML 中通过 `product-card` 展示。 |
| 事件字典 | `src/backend/app/services/log_service.py` `EVENT_DEFINITIONS` | 后端同时允许 `product_list_item_exposure`、`product_card_exposure`、`search_input`、`search_suggestion_exposure` 和 `search_result_exposure`，说明当前不是事件被拒绝，而是前端上报口径偏多。 |
| 测试定位 | `tests/test_miniapp_static.py` | 现有静态测试只断言商品列表和商品卡曝光事件存在、商品卡曝光具备聚合结构，未约束商品列表页双口径互斥或搜索输入防抖。 |

# 影响范围

- 微信小程序商品列表页：分类商品、品牌商品、新品榜、热销榜、搜索承接列表。
- 微信小程序搜索页：搜索输入、搜索建议、搜索结果、筛选、结果商品卡。
- `product-card` 组件曝光事件。
- 后端 `/api/v1/usage-events` 写入量、日志审计噪音和行为分析报表。

# 验证方式

修复前验证：

1. 打开微信开发者工具网络面板，过滤 `/api/v1/usage-events`。
2. 进入商品列表页首屏，观察同一批商品是否出现 `product_list_item_exposure` 与 `product_card_exposure` 双口径。
3. 在搜索页连续输入 4-6 个字符，观察 `search_input` 是否按字符变化逐条上报。
4. 搜索并展示结果，观察 `search_result_exposure` 与结果商品卡 `product_card_exposure` 是否同时上报且无明确边界。

修复后验证：

1. 商品列表页同一批首屏 SKU 只保留一套主曝光口径，或双口径具备可解释的互斥/层级边界。
2. 搜索输入过程 usage-events 数量受控，不再随每个字符变化线性增长。
3. 搜索结果曝光和商品卡曝光的去重键、重置窗口和事件数量符合设计说明。
4. 后端事件字典仍接受保留的事件 payload，埋点失败仍不阻断浏览、搜索、点击或分享。

# 人工补证步骤

当前根因已由代码路径闭环确认。后续实现或验收时仍建议补充小程序开发者工具网络面板截图或请求导出，记录修复前后 `/api/v1/usage-events` 的事件名分布和数量对比。
