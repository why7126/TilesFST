---
requirement_id: REQ-0086-miniapp-brand-list-ui-interaction-optimization
status: pending_review
created_at: 2026-07-31 15:13:01
updated_at: 2026-07-31 15:13:01
owner: product
source: prototype.html
---

# 原型上下文

## 目标

本原型用于表达微信小程序品牌列表页新版 UI 与交互体验。后续实现时，以 `requirement.md` 与 `acceptance.md` 为验收事实源；附件截图和 `prototype.html` 作为视觉层级、间距、品牌卡片结构与交互分区参考。

## 页面结构

```text
BrandListPage
├── CustomNavigation
│   ├── StatusBar
│   ├── BackButton
│   ├── PageTitle("品牌")
│   └── NativeCapsuleReserve
├── BrandHero
│   ├── Eyebrow("BRAND GALLERY")
│   ├── MainTitle("全球严选瓷砖品牌")
│   └── SupportingCopy
├── BrandMatrixHeader
│   ├── Title("品牌矩阵")
│   └── Hint("按类目快速识别")
├── BrandList
│   └── BrandSummaryCard[]
│       ├── BrandEntry → BrandDetail
│       └── CategoryTag[] → BrandCategoryProductList
├── Loading / Empty / Error states
└── TabBar / SafeArea
```

## 关键设计点

- 页面整体延续暗色旗舰风，以品牌金作为返回按钮、Logo 占位、卡片边框和底部品牌 Tab 选中态强调。
- 顶部标题为“品牌”，右侧保留微信原生胶囊 reserve，标题不得被胶囊挤压。
- Hero 区作为品牌氛围入口，优先保持附件视觉稿中的大圆角、金色边框和主标题层级。
- “品牌矩阵”标题区用于承接下方列表，右侧提示文案解释类目标签的浏览价值。
- 每张品牌卡片只承载一个品牌，上行是品牌详情入口，下行是类目商品入口。
- 品牌 Logo 缺失时可使用品牌首字母或缩写的圆形占位，避免破图。
- 类目标签独立点击，点击后携带 `brandId` 与 `categoryId` 进入商品列表页；实现时需阻止事件冒泡。
- 类目标签完整展示并自动换行，卡片高度自然增长，不使用“等 N 类”隐藏类目。
- 页面需避让自定义导航、状态栏、微信原生胶囊、底部 TabBar 和 Safe Area。
- DevTools 需检查 320、375、390、430 pt 视口；真机不可用时标记 `blocked` 或 `follow_up`。

## 原型文件

- `prototype.html`
- `prototype.png`：待后续从 HTML 或设计稿导出，不阻塞本次 req-complete。

## 非目标

- 不表达管理端品牌维护、Logo 上传、排序配置或权限流程。
- 不表达品牌详情页内部结构改造。
- 不表达商品列表页完整视觉重构。
- 不表达类目管理、商品绑定类目、搜索筛选、收藏、询价或下单流程。

## 附件来源

- 用户提供的新版品牌列表页截图。
- 用户提供的 `MoonBox-REQ-0083-brand-list-v1.0.2-patch/prototype.html`。
- 用户提供的 `MoonBox-REQ-0083-brand-list-v1.0.2-patch/prototype-context.md`。
- 用户提供的 `MoonBox-REQ-0083-brand-list-v1.0.2-patch/requirement.md`。
