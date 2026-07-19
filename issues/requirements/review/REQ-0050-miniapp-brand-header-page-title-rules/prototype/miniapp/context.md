---
requirement_id: REQ-0050-miniapp-brand-header-page-title-rules
title: 小程序 brand-header 页面标题规则原型上下文
status: pending_review
created_at: 2026-07-19 14:26:30
updated_at: 2026-07-19 14:26:30
---

# Miniapp Prototype Context

## 目标

展示 `brand-header` 在首页与非首页的文案差异：

- 首页：两行品牌文案。
- 非首页：一行页面标题 + 左侧返回按钮。
- 两种形态均避让顶部状态栏和微信右侧原生胶囊。
- 不自绘分享 / 关闭按钮；原型仅用虚线区域标注“原生胶囊避让区”。

## 页面状态

| 状态 | 原型说明 |
|---|---|
| 首页 | 顶部展示 `菲尚特瓷砖馆` 与 `质感空间，由砖而生`，无返回按钮。 |
| 搜索 | 顶部展示返回按钮与 `搜索`，无第二行 subtitle。 |
| 商品详情 | 顶部展示返回按钮与 `商品详情`，SKU 信息留在内容区。 |
| 收藏 / 证书 | 顶部展示返回按钮与单行页面标题，内容区为占位状态。 |

## 验收优先级

```text
acceptance.md
  > prototype/miniapp/brand-header-title-rules.html
  > prototype/miniapp/context.md
  > rules/ui-design.md
```

## 待导出

- PNG Golden Reference：待后续实现或视觉验收时从 HTML 原型导出。
