## Context

`REQ-0044-miniapp-sku-detail-page` 已在 sprint-008 中评审通过并纳入迭代。现有 `miniapp-home` spec 已覆盖首页、搜索和基础商品详情闭环，但 SKU 详情页只定义到公开字段展示与分享/咨询，尚未覆盖 REQ-0044 要求的图片/视频混合轮播、图片全屏预览、SKU 粒度收藏、微信分享卡片、品牌入口、同系列/同品牌推荐、异常状态和非功能验收。

本 Change 新增独立 capability `miniapp-sku-detail-page`，并在 `product-usage-logging` 中追加 SKU 详情页行为事件字典。管理端 SKU 资料维护继续以 `tile-sku-management` 为事实源，本 Change 只消费已公开的 SKU、品牌、类目、规格、媒体和价格展示信息。

原型与验收优先级：

```text
prototype/miniapp/sku-detail.html
> prototype/miniapp/*.png
> prototype/miniapp/prototype-context.md
> prototype/miniapp/interaction.md
> acceptance.md
> rules/ui-design.md
> openspec/specs
```

Conflict Resolution：

- `miniapp-home` 既有 spec 写明本期商品详情不提供收藏持久化；REQ-0044 已明确收藏粒度为 SKU，并要求收藏页一致性。本 Change 将 SKU 详情页收藏作为新增能力纳入，后续实现必须同时更新收藏接口与收藏页一致性，不能再按首页首期的非持久化收藏占位处理。
- `miniapp-home` 已有基础商品详情字段；本 Change 扩展为 SKU 详情完整字段、媒体、推荐和异常状态，不删除原闭环要求。
- 原型存在系统导航视觉说明；实现不得模拟微信系统状态栏、分享按钮、关闭按钮或胶囊控件，应使用微信小程序真实导航环境和安全区能力。

## Goals / Non-Goals

**Goals:**

- 提供微信小程序 SKU 详情页，承接首页、分类、搜索、品牌页、收藏页和微信分享卡片入口。
- 详情首屏一次性返回或等价聚合 SKU 主体、媒体、品牌、收藏状态和推荐数据，减少小程序串行请求。
- 支持图片/视频混合轮播、图片全屏预览、视频播放控制、收藏/取消收藏、微信分享、品牌跳转、同系列/同品牌推荐和异常状态。
- 确保小程序只展示公开字段、安全媒体 URL 和脱敏埋点，不暴露后台内部字段、未授权 object key、Authorization、Cookie 或原始手机号。
- 以测试和文档门禁约束 API、DB、OpenAPI、Orval、小程序页面和对象存储安全 URL 的同步。

**Non-Goals:**

- 不新增购物车、立即购买、在线下单、支付、库存、优惠券、促销倒计时或询价承诺。
- 不新增管理端 SKU 新增、编辑、上下架、批量维护或上传配置能力。
- 不新增店主 Web 展示端 SKU 详情页。
- 不实现完整品牌馆、品牌详情页、证书聚合页或榜单独立页，除非已有能力可安全跳转。
- 不允许小程序端直连未授权 MinIO/object key。

## Decisions

### D1. 独立 capability 承载 SKU 详情页

新增 `miniapp-sku-detail-page`，而不是继续扩展 `miniapp-home` 的基础商品详情段。原因是 SKU 详情页已经包含独立页面、媒体浏览、收藏、分享、推荐、异常状态、API 和安全边界，具备独立验收闭环。`miniapp-home` 继续负责入口和首页承接，详情页行为由本 capability 约束。

备选方案：把所有详情页要求 MODIFIED 到 `miniapp-home`。该方案会让首页 spec 过大，并让后续详情页变更与首页优化耦合，不采用。

### D2. 详情接口优先聚合首屏数据

详情页应优先使用 `GET /api/v1/miniapp/skus/{skuId}` 或等价版本化路径返回 SKU 主体、媒体、品牌、收藏状态和推荐数据。实现可内部拆分 repository/service，但小程序首屏不应串行请求多个接口再拼装核心页面。

备选方案：小程序分别请求 SKU、媒体、品牌、推荐和收藏状态。该方案增加首屏耗时和失败组合复杂度，不符合 4G 下 2.5 秒首屏目标。

### D3. 收藏作为 SKU 粒度能力

REQ-0044 明确收藏状态需与收藏页一致，因此本 Change 允许新增收藏/取消收藏接口和持久化能力。收藏接口必须幂等，请求失败回滚，未登录或授权失败不得误展示已收藏事实。

备选方案：继续沿用首页心形的非持久化视觉反馈。该方案与本需求验收 AC-009/AC-010 冲突，不采用。

### D4. 媒体 URL 由后端安全输出

详情页需要图片、视频和分享图，但小程序不得直连未授权对象存储。后端应返回公开安全 URL、签名 URL 或经既有媒体适配层生成的可访问 URL；响应不得包含 raw object key 作为小程序展示地址。

备选方案：小程序根据 object key 拼接 MinIO URL。该方案违反对象存储与安全规则，不采用。

### D5. 使用行为事件进入 `product-usage-logging`

SKU 详情页事件纳入统一 usage event 字典：详情浏览、媒体切换、图片预览、视频播放、收藏、取消收藏、分享点击、品牌点击、推荐点击、加载失败。埋点失败不得阻断详情页主流程。

备选方案：小程序本地自行记录或临时日志字段。该方案缺少统一脱敏和查询口径，不采用。

## Risks / Trade-offs

- [Risk] Sprint fix 缓冲已降至 23.33%，详情页再扩大到购物、询价、库存会挤压缺陷修复空间 → Mitigation：spec 和 acceptance 明确不做项，tasks 中单独验收范围外能力未出现。
- [Risk] API/DB 变更面可能扩大 → Mitigation：优先复用现有 SKU、品牌、类目、规格、媒体表；只有收藏、公开状态或推荐所需字段缺失时才新增迁移，并同步 docs/tests。
- [Risk] 图片/视频预览在小程序端受平台 API 限制 → Mitigation：实现阶段优先使用微信小程序原生媒体能力；HTML 原型只作为视觉/交互参考，不直接照搬浏览器 API。
- [Risk] 收藏未登录授权流程影响体验 → Mitigation：授权失败保持未收藏，按钮状态回滚，Toast 提示，主浏览流程不中断。
- [Risk] 分享图裁切和安全 URL 生成不稳定 → Mitigation：优先后台分享图，其次主图安全 URL；失败时可降级到默认品牌图，不阻断页面展示。

## Migration Plan

1. 确认现有 SKU、品牌、类目、规格、图片/视频数据能支撑详情页公开字段。
2. 如需新增收藏或推荐数据结构，先补 SQLite/MySQL schema、迁移和数据库文档。
3. 实现或调整小程序 SKU 详情、收藏和 usage event 接口，同步 OpenAPI、Orval、API 文档和错误码。
4. 实现小程序详情页、媒体预览、收藏/分享、品牌/推荐跳转和异常状态。
5. 补充后端、小程序静态/行为测试和原型/截图验收证据。
6. 若接口或数据变更不可兼容，回滚到只展示基础公开字段和安全媒体 URL，并隐藏收藏或推荐模块。

## Open Questions

- 收藏是否需要匿名设备态、微信 openid 态，还是仅登录/授权用户态，需在实现前确认。
- 品牌主页、分类页、搜索页和收藏页的现有路由可用性需在 apply 阶段实测；不可用时必须安全降级。
- 分享图后台字段是否已存在；若不存在，使用主图裁切还是默认品牌图作为首期策略需实现阶段定稿。
