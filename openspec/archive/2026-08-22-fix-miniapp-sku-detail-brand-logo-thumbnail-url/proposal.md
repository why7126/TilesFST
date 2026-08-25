---
change_id: fix-miniapp-sku-detail-brand-logo-thumbnail-url
type: fix
status: proposed
created_at: 2026-08-22 21:23:53
updated_at: 2026-08-22 21:23:53
source_bug: BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url
source_sprint: sprint-025
---

# 修复小程序商品详情页品牌 Logo 缩略图字段缺口

## 背景

BUG-0133 记录了小程序商品详情页品牌卡缺少 `brand_logo_thumbnail_url`，导致品牌 Logo 在普通卡片展示场景中可能直接回退加载原图的问题。该问题出现在已交付的商品详情页和通用品牌卡组件衔接处，与媒体多规格图片能力中“列表、卡片和轻量展示优先使用缩略图”的约束不一致。

已有代码线索显示，品牌列表和品牌详情入口已经具备 `brand_logo_thumbnail_url`，通用 `brand-card` 组件也支持缩略图优先；但商品详情页品牌数据契约仍存在字段缺口，需要在接口响应、端侧类型和回归测试中补齐。

关联 BUG：`issues/bugs/archive/BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url/`

## 变更范围

- 补齐小程序 SKU 详情接口 `data.brand.brand_logo_thumbnail_url` 字段。
- 补齐小程序商品详情页品牌数据类型与归一化链路，确保 `brand-card` 可收到缩略图 URL。
- 明确商品详情页品牌卡普通展示不得把原图作为性能通过 fallback。
- 增加后端接口测试、小程序静态测试和媒体四联验收记录。

## 非目标

- 不新增通用媒体多规格图片平台能力。
- 不新增品牌 Logo 上传入口或管理端表单能力。
- 不改变品牌详情页、品牌列表页已有交互语义，除非为保持字段一致性做兼容性回归。
- 不引入视频转码、多清晰度视频或 CDN 正式接入。

## 回滚计划

- 若接口字段补充导致兼容性问题，可保留 `brand_logo_url` 原字段不变，并临时停止端侧消费新增 `brand_logo_thumbnail_url`。
- 若缩略图 URL 在部分历史数据中不可用，端侧回滚为占位图或既有安全 fallback，不恢复普通卡片展示直接拉取大体积原图的行为。
- 回滚后必须保留 BUG-0133 验收记录中的失败证据，并重新评估是否需要历史品牌 Logo 缩略图回填。

## 验证计划

- 运行后端聚焦测试，确认 SKU 详情接口返回 `brand.brand_logo_thumbnail_url`。
- 运行小程序静态测试，确认商品详情页品牌类型和品牌卡传参保留缩略图字段。
- 补充微信小程序 DevTools Network evidence，确认品牌卡普通展示优先请求缩略图或安全占位。
- 按媒体类 BUG 四联模板回填 key、object、URL、render 四个维度。
