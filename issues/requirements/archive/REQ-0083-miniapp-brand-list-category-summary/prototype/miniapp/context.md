---
requirement_id: REQ-0083-miniapp-brand-list-category-summary
status: approved
created_at: 2026-07-30 22:36:58
updated_at: 2026-07-30 22:52:24
owner: product
source: requirement.md
---

# 原型上下文

## 目标

本原型用于表达微信小程序品牌列表页下半部的单行品牌信息布局。后续实现时，以 `requirement.md` 与 `acceptance.md` 为验收事实源；顶部轮播图仅作为保持不变的页面上下文示意，不表达轮播改造。

## 页面结构

```text
BrandListPage
├── CustomNavigation / PageTitle
├── BrandHeroSwiper          # 保持既有能力
├── BrandList
│   └── BrandSummaryRow
│       ├── Left: Logo + BrandName + ProductCount
│       └── Right: LeafCategoryNames
├── Loading / Empty / Error states
└── TabBar / SafeArea
```

## 关键设计点

- 顶部品牌轮播保持与现有品牌列表页一致，不调整视觉、数据或跳转。
- 下半部每行只展示一个品牌，横向分成左侧品牌基础信息和右侧末级类目汇总。
- 左侧优先保证品牌 Logo、品牌名称和商品数量可读。
- 右侧类目汇总适合使用短标签；类目过多时应限行、省略或展示“等 N 类”。
- 品牌行整体可点击，沿用现有品牌详情页/主页跳转规则。
- 页面需要避让自定义导航、状态栏、微信原生胶囊和底部 TabBar。
- 320、375、430 pt 视口均需检查品牌行左右区域、类目标签折行和底部安全区。

## 原型文件

- `prototype/miniapp/prototype.html`
- `prototype/miniapp/prototype.png`：待后续从 HTML 导出，缺 PNG 不阻塞评审。

## 非目标

- 不表达顶部轮播图改造。
- 不表达完整品牌详情页。
- 不表达管理端品牌维护、商品类目绑定或类目管理流程。
- 不表达品牌搜索、筛选、收藏、询价或下单流程。
