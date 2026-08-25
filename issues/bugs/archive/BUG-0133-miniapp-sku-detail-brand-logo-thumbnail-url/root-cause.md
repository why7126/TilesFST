---
bug_id: BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url
root_cause_status: probable
category: design
created_at: 2026-08-22 21:05:41
updated_at: 2026-08-22 21:05:41
---

# Root Cause

## 根因状态

`probable`

已有代码定位显示，品牌列表和品牌详情链路已经具备 `brand_logo_thumbnail_url` 字段与缩略图优先消费逻辑；商品详情页品牌卡通过 `product.brand` 渲染通用 `brand-card`，但商品详情页的 `SkuDetail.brand` 类型附近仍只声明 `brand_logo_url`。这说明商品详情页品牌数据在接口响应、端侧类型或归一化链路上存在字段缺口，导致品牌卡无法稳定拿到缩略图字段。

当前仍缺少修复前真实接口响应样本与微信小程序 Network 截图闭环，因此根因状态暂定为 `probable`，后续实现和验收阶段需补齐 evidence 后再升级为 `confirmed`。

## 直接原因

商品详情页品牌卡展示依赖 `product.brand`，而该品牌对象缺少稳定的 `brand_logo_thumbnail_url` 字段。即使通用 `brand-card` 组件支持 `brand_logo_thumbnail_url || brand_logo_url` 的优先级，只要商品详情接口或端侧详情类型未传入缩略图 URL，品牌卡就会回退到 `brand_logo_url` 原图。

## 根本原因

媒体多规格图片能力已覆盖品牌列表和品牌详情等入口，但商品详情页品牌卡的数据契约没有同步补齐品牌 Logo 缩略图字段。该页面复用了品牌卡组件，却没有把同一套缩略图字段从后端详情响应贯通到小程序详情类型与渲染数据。

## 触发条件

1. 商品绑定的品牌配置了 Logo 原图。
2. 该品牌 Logo 有缩略图派生资源，或按媒体多规格策略应具备缩略图消费入口。
3. 用户打开微信小程序商品详情页。
4. 商品详情接口返回的 `brand` 数据缺少 `brand_logo_thumbnail_url`，或端侧详情类型/归一化链路没有保留该字段。
5. `brand-card` 组件无法取得缩略图字段，回退使用 `brand_logo_url`。

## 证据链

| 证据入口 | 类型 | 摘要 | 结论 |
|---|---|---|---|
| `src/miniapp/components/brand-card/index.ts` | 代码定位 | 组件内品牌 Logo 选择逻辑优先使用 `brand_logo_thumbnail_url || brand_logo_url` | 通用品牌卡组件具备缩略图优先消费能力 |
| `src/miniapp/pages/brand-list/index.ts`、`src/miniapp/pages/brand-detail/index.wxml` | 代码定位 | 品牌列表和品牌详情均存在 `brand_logo_thumbnail_url` 字段或绑定 | 其他品牌入口已接入缩略图字段 |
| `src/miniapp/pages/tile-detail/index.ts` | 代码定位 | `SkuDetail.brand` 类型只声明 `brand_logo_url`，未声明 `brand_logo_thumbnail_url` | 商品详情页品牌数据契约存在字段缺口 |
| `src/miniapp/pages/tile-detail/index.wxml` | 代码定位 | 商品详情页将 `product.brand` 传给 `<brand-card>` | 缺口会直接影响商品详情页品牌卡展示 |
| `tests/test_miniapp_home.py::test_miniapp_sku_detail_returns_public_media_recommendations_and_share` | 测试定位 | 当前测试断言商品详情接口品牌数据包含 `brand_logo_url`，未覆盖 `brand_logo_thumbnail_url` | 回归测试缺少商品详情品牌 Logo 缩略图断言 |

## 人工补证步骤

1. 在本地或测试环境请求 `/api/v1/miniapp/skus/{id}`，选择一个带品牌 Logo 且缩略图对象存在的商品，记录脱敏后的 `brand` 字段摘要。
2. 在微信小程序开发者工具打开同一商品详情页，禁用缓存后记录 Network 中品牌 Logo 请求 URL、Size、Time、是否命中缓存。
3. 对比品牌 Logo 原图 URL 与缩略图 URL，确认品牌卡普通展示是否请求缩略图。
4. 修复后把同一入口的接口响应、Network 摘要和页面渲染截图回填到 `acceptance.md`。

## 验证方式

- 修复前：商品详情接口或端侧商品详情数据缺少 `brand.brand_logo_thumbnail_url`，品牌卡 Network 请求命中原图 URL。
- 修复后：商品详情接口返回 `brand.brand_logo_thumbnail_url`，小程序商品详情页品牌卡优先请求缩略图 URL；缺缩略图时使用占位或受控降级，不直接拉取大体积原图。
