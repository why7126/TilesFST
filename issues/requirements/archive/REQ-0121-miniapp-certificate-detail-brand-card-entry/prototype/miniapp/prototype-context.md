---
requirement_id: REQ-0121-miniapp-certificate-detail-brand-card-entry
title: 小程序证书详情页品牌入口复用 brand-card 原型上下文
status: in_sprint
owner: product
source: acceptance.md
created_at: 2026-08-24 15:26:47
updated_at: 2026-08-24 16:36:37
---

# 原型上下文

## 1. 目标

本 prototype context 用于约束证书详情页所属品牌入口的局部视觉和交互验收。该需求不重做证书详情页整体原型，只要求在既有证书详情页 `BrandEntry` 区域复用 `brand-card` 组件，并保持品牌 Logo、跳转、埋点和异常状态一致。

## 2. 页面落点

```text
CertificateDetailPage
├── MediaHero
├── CertificateSummary
├── BrandEntry
│   └── brand-card
│       ├── brand-logo: brand_logo_thumbnail_url / fallback
│       ├── brand-name
│       ├── brand-hint
│       └── entry affordance
├── CertificateInfoPanel
└── BottomActionBar
```

## 3. 状态覆盖

| 状态 | 说明 | 验收重点 |
|---|---|---|
| normal | 有品牌名称、缩略图和品牌入口 | 展示一致、点击进入品牌页、上报 `brand_card_click`。 |
| thumbnail-missing | 无 `brand_logo_thumbnail_url` | 使用统一占位，不 fallback 到原图。 |
| image-failed | 缩略图 URL 加载失败 | 不破图、不跳高、证书正文仍可读。 |
| long-name | 品牌名称较长 | 320px 小屏不溢出，不遮挡入口提示。 |
| unavailable | 品牌不可公开或入口不可用 | 禁用或提示一致，阻止无效跳转。 |

## 4. 视觉约束

- 继续沿用 `brand-card` 的深色卡片、品牌金强调和近直角视觉。
- Logo 容器固定尺寸，图片加载前后不改变卡片高度。
- 卡片点击热区覆盖整张品牌入口，触控高度不小于 44px。
- 品牌入口与证书详情页上下模块间距保持一致，不新增独立页面级视觉语言。

## 5. 验收证据

- 320 / 375 / 430px 逻辑宽度截图或等价截图摘要。
- `brand_logo_thumbnail_url` Network evidence。
- `brand_card_click` 埋点事件名和参数摘要。
- 证书详情页与商品详情页 brand-card 回归对比摘要。
