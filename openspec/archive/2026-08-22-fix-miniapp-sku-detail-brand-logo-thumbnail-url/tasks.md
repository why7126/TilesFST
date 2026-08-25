---
change_id: fix-miniapp-sku-detail-brand-logo-thumbnail-url
status: applied
created_at: 2026-08-22 21:23:53
updated_at: 2026-08-22 21:37:04
source_bug: BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url
---

# 任务

- [x] 1. 后端 SKU 详情接口补齐品牌 Logo 缩略图字段
  - [x] 在 SKU 详情品牌响应 Schema 中增加 `brand_logo_thumbnail_url`。
  - [x] 服务层返回品牌 Logo 缩略图受控 URL，并保留 `brand_logo_url` 兼容字段。
  - [x] 避免把不存在或不可读的缩略图 URL 当作已验证轻量资源。

- [x] 2. 小程序商品详情页保留并传递缩略图字段
  - [x] `SkuDetail.brand` 类型增加 `brand_logo_thumbnail_url`。
  - [x] 确认 `product.brand` 传入 `brand-card` 时不丢失缩略图字段。
  - [x] 确认品牌卡 Logo 普通展示优先使用缩略图，缺缩略图时展示占位或受控降级。

- [x] 3. 补充回归测试
  - [x] 后端测试覆盖 `/api/v1/miniapp/skus/{sku_id}` 返回 `data.brand.brand_logo_thumbnail_url`。
  - [x] 小程序静态测试覆盖商品详情页品牌对象声明或消费 `brand_logo_thumbnail_url`。
  - [x] 回归品牌列表、品牌详情和商品详情入口的品牌 Logo 字段一致性。

- [x] 4. 补充文档与生成物
  - [x] 若 OpenAPI 发生变化，运行 `./scripts/generate-openapi-client.sh` 并同步 Orval 生成物。
  - [x] 更新 `docs/03-api-index.md` 中 SKU 详情品牌字段说明。
  - [x] 更新 BUG-0133 acceptance 的 key、object、URL、render 四联验收证据。

- [x] 5. 归档前检查
  - [x] 运行聚焦后端测试和小程序静态测试。
  - [x] 运行 `python scripts/validate-openspec-language.py`。
  - [x] 运行 `python scripts/validate-directory-structure.py`。
  - [x] 判断是否需要在 `docs/knowledge-base/incidents/` 沉淀品牌 Logo 缩略图消费偏差经验；本次为单字段消费偏差，现有媒体四联验收实践已覆盖，暂不新增 incident。
