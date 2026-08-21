---
change_id: fix-miniapp-sku-detail-carousel-original-image-height
status: implemented
created_at: 2026-08-21 13:43:10
updated_at: 2026-08-21 13:52:48
source_bug: BUG-0131-miniapp-sku-detail-carousel-original-image-height
sprint: sprint-024
---

# 修复小程序商品详情页轮播图清晰度和高度

## 背景

`BUG-0131-miniapp-sku-detail-carousel-original-image-height` 记录了小程序商品详情页顶部轮播首屏使用 `.thumb` 缩略图导致大图区域清晰度不足的问题。用户截图中的 SKU `M612X07` 在详情页首屏中瓷砖纹理、边缘和展板文字发糊，无法满足瓷砖详情页查看花色、纹理和规格细节的核心场景。

当前详情页媒体高度固定为 `680rpx`，用户反馈高度不够。截图也显示商品名称和价格仍在首屏露出，因此修复需要在“更高、更清晰的媒体区”和“首屏商品关键信息可见”之间保持平衡。

## 变更内容

- 调整 SKU 详情页图片媒体展示语义：详情页首屏轮播图片不再优先使用小尺寸 `.thumb`，改用原图或详情级高清展示图。
- 保持图片预览使用原图或等价高清 URL。
- 商品列表、商品卡片、推荐位和 Banner 继续保留 `.thumb` 或等价轻量图片策略，避免列表性能回退。
- 调整小程序商品详情页轮播高度，覆盖 320 到 430px 逻辑宽度，并保证首屏仍露出商品名称或关键商品信息。
- 同步更新 OpenSpec、测试断言、媒体四联验收和小程序 render evidence 要求。

## 回滚计划

- 若详情页直接使用原图导致首屏加载明显变慢，可回滚到详情级高清展示图策略，而不是让列表/卡片回退原图。
- 若高度调整导致商品名称完全被挤出首屏，可回滚媒体区高度公式或上限，保留清晰图展示 URL 语义。
- 回滚不涉及数据库结构；若接口字段语义变更影响兼容，可临时让小程序端优先读取 `preview_url` 作为详情展示源，并保持后端字段兼容。

## 关联

- BUG：`issues/bugs/archive/BUG-0131-miniapp-sku-detail-carousel-original-image-height/`
- Sprint：`iterations/archive/sprint-024/`
- 相关能力：`miniapp-sku-detail-page`、`miniapp-product-list-page`、`media-acceptance-template`
