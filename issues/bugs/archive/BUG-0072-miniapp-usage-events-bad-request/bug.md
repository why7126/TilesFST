---
bug_id: BUG-0072-miniapp-usage-events-bad-request
title: 微信小程序 usage-events 上报接口频繁返回 400
severity: high
status: done
owner:
discovered_at: 2026-07-21 08:38:39
environment: 微信小程序 DevTools / macOS / mp 2.01.2510290 / lib 3.16.2；后端本地 API http://127.0.0.1:8010
related_requirement: REQ-0024-product-usage-logging
related_change: fix-miniapp-usage-events-contract-drift
created_at: 2026-07-21 10:10:00
updated_at: 2026-07-22 08:47:45
---

# 现象

微信小程序运行过程中，行为埋点请求频繁返回 400：

```text
POST http://127.0.0.1:8010/api/v1/usage-events 400 (Bad Request)
(env: macOS, mp, 2.01.2510290; lib: 3.16.2)
```

该接口是产品使用事件上报能力的一部分。小程序端通过 `track()` 统一调用 `POST /api/v1/usage-events`，后端按事件字典校验 `event_name`、必填属性和禁止属性。当前小程序多个页面或组件会上报后端尚未登记的事件名，导致请求被稳定拒绝。

# 复现

## 复现路径 A：收藏页事件

1. 在微信开发者工具中运行小程序。
2. 进入收藏页 `/pages/favorites/index`。
3. 触发页面加载、空态引导、收藏项点击或取消收藏。
4. 打开 Network 或 Console，观察 `POST /api/v1/usage-events`。

预期现象：对应 `favorite_list_page_view`、`favorite_list_item_click`、`favorite_list_remove` 等事件上报返回 400。

## 复现路径 B：品牌详情页事件

1. 从品牌列表或 SKU 详情进入品牌详情页 `/pages/brand-detail/index`。
2. 触发品牌详情加载、商品 Tab 加载、证书 Tab 加载或证书点击。
3. 观察 `POST /api/v1/usage-events` 响应。

预期现象：`brand_detail_view`、`brand_products_load`、`brand_certificates_load`、`brand_certificate_click` 等事件存在 400 风险。

## 复现路径 C：商品 / 品牌卡片组件事件

1. 进入使用通用商品卡片或品牌卡片的页面。
2. 点击商品卡片、品牌卡片，或触发图片加载失败。
3. 观察 `POST /api/v1/usage-events` 响应。

预期现象：`product_card_*`、`brand_card_*` 系列事件存在后端未知事件 400 风险。

# 已验证证据

使用后端 TestClient 对代表性 payload 进行验证：

| 场景 | event_name | 结果 | 响应摘要 |
|---|---|---|---|
| 已注册 SKU 详情事件 | `sku_detail_view` | 200 | `accepted: true` |
| 收藏页页面浏览事件 | `favorite_list_page_view` | 400 | `code: 40001`，`message: 未知埋点事件` |
| 品牌详情浏览事件 | `brand_detail_view` | 400 | `code: 40001`，`message: 未知埋点事件` |
| 商品列表字段缺失 | `product_list_page_view` | 400 | `message: 埋点事件缺少必填属性：pageSize, requestId, sort` |

静态枚举对比也显示，小程序至少存在以下后端未注册的字面量事件：

| event_name | 触发位置 | 风险 |
|---|---|---|
| `favorite_list_page_view` | 收藏页加载 | 稳定 400 |
| `favorite_list_load_failed` | 收藏页读取失败 | 稳定 400 |
| `favorite_list_empty_action_click` | 收藏页空态引导 | 稳定 400 |
| `favorite_list_item_click` | 收藏项点击 | 稳定 400 |
| `favorite_list_remove` | 收藏页取消收藏 | 稳定 400 |
| `brand_card_click` | SKU 详情页 / 品牌卡片组件 | 稳定 400 |
| `brand_card_unavailable_click` | SKU 详情页 / 品牌卡片组件 | 稳定 400 |

此外，品牌详情页和通用卡片组件通过动态事件名上报的 `brand_detail_*`、`brand_products_*`、`brand_certificates_*`、`product_card_*` 系列事件，也需要逐一与后端 `EVENT_DEFINITIONS` 对齐。

# 期望 vs 实际

期望：

- 小程序当前代码中定义并触发的合法埋点事件，都应在后端事件字典中有明确契约。
- 合法事件上报应返回成功，并写入 `usage_events`。
- 非法事件应只在真正违反契约时返回 400，且响应应能定位缺失字段或禁止字段。
- 埋点失败不得刷屏影响调试，也不得造成关键统计缺失。

实际：

- 小程序端存在多个后端未知事件，触发即返回 `40001 未知埋点事件`。
- 部分事件还可能因必填字段命名或字段缺失返回 400。
- 前端虽然 catch 了埋点失败，不阻断用户主流程，但控制台和 Network 中会持续出现 400。
- 对应页面访问、收藏、品牌入口、卡片点击等行为不会进入 `usage_events`，影响后续统计、热销排序和排查。

# 影响范围

| 范围 | 影响 |
|---|---|
| 微信小程序收藏页 | 页面浏览、空态点击、收藏项点击、取消收藏等事件统计缺失 |
| 微信小程序品牌详情页 | 品牌详情浏览、商品加载、证书加载、证书点击等事件存在统计缺失风险 |
| 微信小程序 SKU 详情页 | 品牌卡片点击、不可用点击等事件统计缺失 |
| 通用商品 / 品牌卡片组件 | 卡片曝光、点击、图片失败等组件级埋点存在 400 风险 |
| 后端日志审计 / 使用统计 | `usage_events` 数据不完整，影响行为分析、热销/访问统计和问题排查 |
| 开发调试体验 | 小程序控制台和 Network 出现大量 400 噪音，掩盖真实业务错误 |

# 严重等级说明

严重等级评估为 `high`：

- 请求错误数量多，用户反馈为“很多这个请求问题”。
- 影响面覆盖多个小程序页面和通用组件，而非单个孤立按钮。
- 虽不直接阻断用户浏览，但会造成使用行为统计缺失，并干扰开发者排查真正的业务错误。
- 该能力关联已归档的 `REQ-0024-product-usage-logging`，属于已交付能力与当前小程序实现之间的契约回归或同步缺失。

# 建议后续处理

1. `/bug-complete BUG-0072-miniapp-usage-events-bad-request` 补齐 root-cause、workaround、acceptance。
2. 修复时应统一梳理小程序全部 `track()` 事件，补齐后端 `EVENT_DEFINITIONS` 或调整小程序事件名。
3. 增加后端测试，覆盖小程序当前全部埋点事件至少能通过事件字典校验。
4. 增加前端或脚本级静态校验，防止新增小程序事件未同步后端字典。
