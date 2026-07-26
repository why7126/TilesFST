## Why

微信小程序首页、商品详情页、商品列表页和品牌详情页已经形成主要浏览链路，但分享能力目前分散在各页面内，朋友圈分享、商品列表上下文保留、分享直达兜底和设备 evidence 尚未形成统一契约。REQ-0064 已评审通过，需要通过 OpenSpec Change 将页面级微信分享能力纳入正式可实现范围。

## What Changes

- 为首页、商品详情页、商品列表页、品牌详情页补齐微信朋友分享和朋友圈分享要求。
- 明确分享标题、分享路径、关键 query 参数、分享图兜底和异常参数降级规则。
- 要求商品列表页分享保留搜索、分类、品牌和榜单上下文。
- 要求分享直达场景继续遵守小程序自定义导航、原生胶囊避让、返回兜底和页面 offset 规则。
- 要求分享埋点失败不阻断分享，并禁止在分享路径、埋点和 evidence 中泄露敏感信息。
- 不新增分享海报、后台分享配置、裂变活动、短链系统、API 或数据库持久化。

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `miniapp-home`: 首页支持微信朋友分享与朋友圈分享，分享标题、路径、来源标识和埋点非阻断规则进入规格。
- `miniapp-sku-detail-page`: SKU 详情页补齐朋友圈分享、`skuId` 参数保留、分享图兜底和分享直达异常态。
- `miniapp-product-list-page`: 商品列表页新增微信朋友分享与朋友圈分享，并保留搜索、分类、品牌和榜单上下文。
- `miniapp-brand-detail-home-page`: 品牌详情页补齐微信朋友分享与朋友圈分享，并保留 `brandId` 与分享直达兜底。
- `miniapp-global-custom-navigation-bar`: 分享直达页面继续遵守原生胶囊避让、返回兜底和内容 offset。
- `miniapp-device-evidence-template`: 分享、返回、胶囊和直达场景的 DevTools / 真机 evidence 边界进入验收要求。

## Impact

- 小程序：预计影响 `src/miniapp/pages/index`、`src/miniapp/pages/tile-detail`、`src/miniapp/pages/product-list`、`src/miniapp/pages/brand-detail` 的页面级分享配置、路径构建和埋点。
- API：默认不新增或调整接口；若实现阶段新增后台分享配置或分享图字段，必须另行同步 OpenAPI、Orval、docs 和测试。
- 数据库：默认不新增表或字段。
- 对象存储 / 媒体：仅使用现有公开安全 URL 或本地兜底资源，不放宽 MinIO 权限。
- 测试：需要补充小程序静态测试或等价验收，覆盖 `onShareAppMessage`、`onShareTimeline`、query 参数保留、运行 `.js` 与 `.ts` 一致性和分享直达 evidence。
