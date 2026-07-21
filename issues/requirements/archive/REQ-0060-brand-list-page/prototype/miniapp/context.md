---
requirement_id: REQ-0060-brand-list-page
status: pending_review
created_at: 2026-07-19 23:28:20
updated_at: 2026-07-19 23:28:20
owner: product
source: requirement.md
---

# 原型上下文

## 目标

本原型用于表达微信小程序品牌列表页的信息架构和视觉方向，后续实现时以 `requirement.md` 与 `acceptance.md` 为验收事实源。

## 页面结构

```text
BrandListPage
├── CustomNavigation / PageTitle
├── BrandHeroSwiper
├── BrandSummaryStrip
├── BrandGrid
│   └── BrandCard x 2 columns
├── Loading / Empty / Error states
└── TabBar / SafeArea
```

## 关键设计点

- 顶部品牌轮播对齐小程序首页轮播：暗色材质、品牌金指示点、标题和副标题叠加。
- 品牌列表一行 2 个卡片，卡片稳定尺寸，Logo 居中展示。
- 品牌卡片点击进入品牌详情页/主页；未交付时可降级品牌商品列表。
- 页面需要避让自定义导航、状态栏、微信原生胶囊和底部 TabBar。
- 320、375、430 pt 视口均需检查双列卡片、标题截断和轮播不遮挡。

## 原型文件

- `prototype/miniapp/prototype.html`
- `prototype/miniapp/prototype.png`：待后续从 HTML 导出，缺 PNG 不阻塞评审。

## 非目标

- 不表达管理端品牌维护页。
- 不表达完整品牌详情页。
- 不表达品牌收藏、预约、询价或下单流程。
