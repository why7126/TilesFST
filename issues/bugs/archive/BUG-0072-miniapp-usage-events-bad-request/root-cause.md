---
bug_id: BUG-0072-miniapp-usage-events-bad-request
title: 微信小程序 usage-events 上报接口频繁返回 400
status: done
severity: high
created_at: 2026-07-21 14:41:14
updated_at: 2026-07-22 08:47:45
related_requirement: REQ-0024-product-usage-logging
related_change: fix-miniapp-usage-events-contract-drift
---

# 直接原因

微信小程序当前代码中存在多个 `track()` 上报事件，但后端 `POST /api/v1/usage-events` 的事件字典 `EVENT_DEFINITIONS` 未覆盖这些事件名。后端在接收请求时会先按 `event_name` 查找定义；查不到时直接返回 `40001 未知埋点事件`。

已确认的高风险事件包括：

| event_name | 触发范围 | 当前后端结果 |
|---|---|---|
| `favorite_list_page_view` | 收藏页加载 | 400 |
| `favorite_list_load_failed` | 收藏页读取失败 | 400 |
| `favorite_list_empty_action_click` | 收藏页空态引导 | 400 |
| `favorite_list_item_click` | 收藏项点击 | 400 |
| `favorite_list_remove` | 收藏页取消收藏 | 400 |
| `brand_card_click` | SKU 详情页 / 品牌卡片组件 | 400 |
| `brand_card_unavailable_click` | SKU 详情页 / 品牌卡片组件 | 400 |

品牌详情页和通用卡片组件还存在动态事件名风险，例如 `brand_detail_*`、`brand_products_*`、`brand_certificates_*`、`product_card_*` 系列，需要在修复阶段完整枚举并对齐。

# 根本原因

产品使用事件上报能力采用“后端事件字典白名单 + 必填属性 + 禁止属性”的强契约设计，但小程序新增页面、组件和交互埋点时，没有建立同步校验机制来保证：

1. 小程序新增 `track()` 事件后，同步更新后端 `EVENT_DEFINITIONS`。
2. 后端新增事件定义后，小程序 payload 字段名、必填字段和安全禁止字段保持一致。
3. 测试覆盖“小程序当前全部埋点事件都能通过后端契约校验”。

因此，小程序业务页面持续演进后，事件名和字段契约与后端白名单发生漂移。

# 触发条件

满足以下任一条件即可触发：

- 小程序进入收藏页并触发页面浏览、空态引导、收藏项点击或取消收藏。
- 小程序进入品牌详情页并触发品牌详情浏览、商品加载、证书加载或证书点击。
- 小程序点击 SKU 详情页底部品牌卡片，或触发品牌卡片不可用分支。
- 小程序通用商品卡片或品牌卡片触发曝光、点击、图片失败等组件级埋点。
- 小程序上报已注册事件但缺少后端要求的必填字段，例如 `product_list_page_view` 缺少 `pageSize`、`requestId` 或 `sort`。

# 缺陷分类

| 维度 | 分类 | 说明 |
|---|---|---|
| 类型 | code / contract | 前后端埋点事件契约不一致 |
| 端 | 微信小程序 + 后端 API | 小程序发送事件，后端严格校验拒绝 |
| 模块 | product_usage_logging | 关联 `REQ-0024-product-usage-logging` |
| 数据影响 | usage_events 数据缺失 | 行为统计、热销/访问分析和排查依据不完整 |
| 安全影响 | 低 | 后端拒绝未知或非法事件是安全行为，问题在合法小程序事件未纳入契约 |

# 复现证据

后端 TestClient 已验证：

| 请求 | 结果 |
|---|---|
| `event_name=sku_detail_view` 且字段齐全 | 200，`accepted: true` |
| `event_name=favorite_list_page_view` | 400，`code: 40001`，`message: 未知埋点事件` |
| `event_name=brand_detail_view` | 400，`code: 40001`，`message: 未知埋点事件` |
| `event_name=product_list_page_view` 但缺少字段 | 400，提示缺少 `pageSize`、`requestId`、`sort` |

# 修复方向

1. 梳理 `src/miniapp/**` 中所有 `track()` 事件，包括动态事件名分支。
2. 为小程序当前合法事件补齐后端 `EVENT_DEFINITIONS`，明确 `category`、`required`、`forbidden`。
3. 对字段命名不统一的 payload 做一处收敛：优先保留后端契约字段，必要时调整小程序字段名。
4. 增加自动化测试，确保小程序事件字典与后端事件定义不会再次漂移。
