---
change_id: fix-miniapp-sku-detail-brand-logo-thumbnail-url
status: proposed
created_at: 2026-08-22 21:23:53
updated_at: 2026-08-22 21:23:53
source_bug: BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url
---

# 设计

## 根因摘要

BUG-0133 的根因状态为 `probable`。品牌列表、品牌详情和通用品牌卡组件已有 `brand_logo_thumbnail_url` 消费能力，但商品详情页品牌对象仍存在字段缺口，导致 `brand-card` 在商品详情页无法稳定取得缩略图 URL，进而回退到 `brand_logo_url` 原图。

后续实现阶段需要通过接口响应样本和小程序 Network evidence 把根因升级为 `confirmed`，并把证据回填到 BUG acceptance。

## 修复方案

1. 后端 SKU 详情响应补齐品牌 Logo 缩略图字段：
   - 在 SKU 详情品牌 Schema 中新增 `brand_logo_thumbnail_url`。
   - 服务层按品牌 Logo object key 推导或读取同目录缩略图 URL。
   - 保留 `brand_logo_url` 兼容字段，但普通卡片展示不得依赖它作为首选。

2. 小程序商品详情页补齐端侧契约：
   - `SkuDetail.brand` 类型增加 `brand_logo_thumbnail_url`。
   - 详情页向 `brand-card` 传递完整 `product.brand`。
   - 保持 `brand-card` 缩略图优先、Logo 缺失或失败时稳定占位。

3. 测试与验收补齐：
   - 后端测试断言 `/api/v1/miniapp/skus/{id}` 返回 `brand.brand_logo_thumbnail_url`。
   - 小程序静态测试断言商品详情页类型或绑定保留 `brand_logo_thumbnail_url`。
   - BUG acceptance 记录 key、object、URL、render 四联证据。

## API 与兼容性

- 请求：`GET /api/v1/miniapp/skus/{sku_id}`。
- 响应新增字段：`data.brand.brand_logo_thumbnail_url: string | null`。
- `brand_logo_url` 保持兼容，继续表达品牌 Logo 原图或原始展示引用。
- 错误码不新增。
- 因响应 Schema 增加字段，后续实现需要同步 OpenAPI、Orval 和 API 文档。

## 数据与对象存储

- 不新增数据库字段。
- 不新增 Bucket 或对象存储前缀。
- 品牌 Logo 缩略图应沿用已有同目录缩略图命名策略和受控 `/media` URL。
- 若历史品牌 Logo 缩略图对象缺失，需在验收中记录 blocked、follow-up 或历史回填摘要，不得把原图 fallback 视为性能通过。

## 测试策略

- 后端：补充或更新 `tests/test_miniapp_home.py` 中 SKU 详情接口品牌字段断言。
- 小程序：补充或更新 `tests/test_miniapp_static.py` 中商品详情页品牌字段消费断言。
- 媒体：按 `docs/standards/media-bug-four-point-acceptance-template.md` 回填四联验收。
- 回归：确认品牌列表、品牌详情、商品详情的品牌 Logo 缩略图优先策略一致。
