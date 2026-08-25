---
bug_id: BUG-0137-miniapp-lightweight-image-variant-consumption
workaround_status: active
created_at: 2026-08-24 15:02:18
updated_at: 2026-08-24 15:02:18
---

# Workaround

## 临时规避

在正式修复前，可采用以下临时规避策略降低普通展示冷加载原图的风险：

1. 管理端维护 Banner、品牌 Logo、分享图素材时，优先使用已生成缩略图或展示图的图片对象。
2. 测试数据和演示数据避免只配置原图对象；缺少轻量图时优先使用本地占位图或下架相关 Banner。
3. 小程序验收时重点观察首页 Banner、品牌列表 Banner、品牌 Logo 和分享入口 Network 请求，发现原图请求即标记为失败或阻塞。
4. 对品牌 Logo 缺少 `brand_logo_thumbnail_url` 的数据，临时补齐缩略图对象或避免展示该 Logo 原图。

## 不可规避部分

- Banner schema 只有 `image_url` 的接口契约问题无法仅靠数据规避，需要后续修复字段契约。
- 端侧默认 fallback 到 `brand_logo_url`、`preview_url` 或 `url` 的代码路径无法靠运营配置彻底阻断。
- 缺少小程序 Network/render evidence 时，不能宣称媒体多规格消费验收通过。

## 风险提示

该规避方案只降低部分数据场景的冷加载风险，不替代正式修复。正式修复仍需统一字段优先级、禁止普通展示原图 fallback，并补齐小程序 DevTools、真机或体验版证据。
