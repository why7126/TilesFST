---
requirement_id: REQ-0043-miniapp-home-style-optimization
title: 微信小程序首页样式与信息架构优化 - 原型策略
status: pending_review
created_at: 2026-07-18 12:51:59
updated_at: 2026-07-18 12:57:29
---

# 原型策略

## 1. 视觉来源

本需求以用户提供的附件原型为视觉事实源：

- 附件 `prototype.png`：高保真视觉参考。
- `prototype.html`：已纳入本需求目录，作为布局、字号、色彩和模块结构参考。
- 附件 `context.md`：交互、信息架构和负面约束参考。
- 附件 `requirement.md`：功能范围和验收要点参考。

附件中的外部版本号不写入本项目需求事实；本项目事实以 `REQ-0043` 文档、后续 OpenSpec 和验收结论为准。

## 2. 实现优先级

```text
prototype.png / prototype.html
  > requirement.md / acceptance.md
  > rules/ui-design.md 小程序适配约束
  > 当前 src/miniapp 实现现状
```

## 3. 页面结构参考

```text
StoreHeader
SearchBar
HeroBanner
QuickEntryGrid（选瓷砖 / 品牌馆 / 新品榜 / 热销榜）
NewProductSection
HotProductSection
AllProductWaterfall
BottomTabBar（首页 / 分类 / 找砖 / 收藏 / 证书）
```

## 4. PNG 导出状态

当前已有用户附件 PNG 可作为 Golden Reference。若后续进入 OpenSpec 实现阶段，建议将附件原型复制到本目录作为 `prototype.png`，或在 Change 中记录可追溯来源。

## 5. 已纳入文件

| 文件 | 用途 |
|---|---|
| `prototype.html` | 首页原型 HTML，后续 UI 实现与视觉验收优先参考 |
