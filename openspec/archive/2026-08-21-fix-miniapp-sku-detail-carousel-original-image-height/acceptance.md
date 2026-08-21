---
change_id: fix-miniapp-sku-detail-carousel-original-image-height
status: implemented
created_at: 2026-08-21 13:43:10
updated_at: 2026-08-21 13:52:48
source_bug: BUG-0131-miniapp-sku-detail-carousel-original-image-height
---

# 验收计划

## 回归验收

- 商品详情页轮播首屏图片不再优先使用小尺寸 `.thumb` 作为大图展示资源。
- 图片点击预览仍使用原图或等价高清 URL。
- 商品列表、商品卡片、推荐位和 Banner 仍使用 `.thumb` 或等价轻量图片 URL。
- 轮播高度比固定 `680rpx` 更适合瓷砖详情展示，并覆盖 320、375、430px 逻辑宽度。
- 首屏仍能露出商品名称或关键商品信息。
- 规格、测试断言和媒体四联验收同步更新。

## 媒体四联验收

模板：`docs/standards/media-bug-four-point-acceptance-template.md`

| 维度 | 要求 |
|---|---|
| key | 记录脱敏 SKU 图片原图 key 与 `.thumb` key 关系，确认不向小程序公开原始 object key。 |
| object | 记录示例 SKU 原图与 `.thumb` 的 MIME、像素尺寸、bytes 和缩略图收益对比。 |
| URL | 确认详情页展示 URL 使用原图或详情级高清图，预览 URL 仍高清，列表/卡片 URL 仍为 `.thumb`。 |
| render | 使用小程序 DevTools、真机或体验版补充修复前后清晰度、轮播高度和首屏商品信息露出 evidence。 |

## 验收结果回填

| 时间 | 结果 | 证据 | 说明 |
|---|---|---|---|
| 2026-08-21 13:52:48 | pass_with_pending_render_evidence | `uv run pytest tests/test_miniapp_home.py::test_miniapp_sku_detail_returns_public_media_recommendations_and_share tests/test_miniapp_home.py::test_miniapp_products_return_has_more_for_waterfall tests/test_miniapp_home.py::test_miniapp_product_list_brand_default_sort_uses_published_at_and_id tests/test_miniapp_home.py::test_miniapp_product_list_category_and_keyword_default_sort_uses_public_order`：4 passed；`uv run pytest tests/test_miniapp_static.py::test_miniapp_sku_detail_page_covers_media_favorite_share_and_empty_states tests/test_miniapp_media_assertions.py`：5 passed。 | 后端接口断言详情页图片 `media[].url` 使用原图、`preview_url` 保持原图，列表/卡片仍 `.thumb`；小程序静态断言详情页图片/预览绑定和 `720rpx` 到 `820rpx` 视口约束媒体区。当前环境未连接小程序 DevTools/真机，render evidence 需发布前补充。 |
