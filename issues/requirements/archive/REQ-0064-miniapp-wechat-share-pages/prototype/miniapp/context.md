---
requirement_id: REQ-0064-miniapp-wechat-share-pages
title: 小程序多页面微信分享 prototype context
status: approved
created_at: 2026-07-21 09:45:04
updated_at: 2026-07-21 10:11:23
---

# Prototype Context

## 1. 原型策略

本需求不新增自绘分享按钮、分享面板、海报页或后台配置页，核心体验依赖微信小程序原生分享入口。因此本阶段不生成 HTML / PNG 视觉稿，使用本 context 作为 prototype 策略说明。

后续实现验收以真实小程序页面、微信开发者工具或真机 evidence 为准。

## 2. 页面状态矩阵

| 页面 | 正常进入 | 微信朋友直达 | 朋友圈直达 | 异常参数 |
|---|---|---|---|---|
| 首页 | 展示品牌首页 | 进入首页 | 进入首页 | 使用首页兜底内容 |
| 商品详情页 | 展示 SKU | 进入指定 SKU | 进入指定 SKU | 商品暂不可查看 |
| 商品列表页 | 展示当前列表 | 恢复列表上下文 | 恢复列表上下文 | 降级为可浏览列表 |
| 品牌详情页 | 展示品牌主页 | 进入指定品牌 | 进入指定品牌 | 品牌暂不可查看 |

## 3. 交互约束

- 使用微信原生右上角分享入口。
- 商品详情页如保留底部“分享”按钮，应与页面级分享配置一致。
- 不自绘微信分享、关闭或系统胶囊。
- 分享直达状态下返回兜底到首页。
- 分享直达状态下首屏内容不得被自定义导航栏遮挡。
- 页面标题、分享标题和列表标题必须保持语义一致。

## 4. Evidence 建议

```yaml
target: REQ-0064-miniapp-wechat-share-pages
pages:
  - pages/index/index
  - pages/tile-detail/index?skuId=<sample>&source=share
  - pages/product-list/index?keyword=<sample>&sourcePage=share
  - pages/brand-detail/index?brandId=<sample>&source=share
viewports:
  - 320pt
  - 375pt
  - 430pt
checks:
  - share_friend_config
  - share_timeline_config
  - query_retention
  - native_capsule_reserve
  - back_fallback
  - content_offset
  - no_blank_screen
```

## 5. PNG / HTML

- PNG：N/A，本需求无新增自绘界面。
- HTML：N/A，小程序原生分享能力无法由静态 HTML 准确表达。
- 后续若产品要求分享海报或自定义分享面板，必须另行 capture 或扩展 Change。
