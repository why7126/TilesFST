---
requirement_id: REQ-0042-custom-navigation-bar
title: 微信小程序首页品牌自定义导航栏原型上下文
status: approved
created_at: 2026-07-18 12:55:02
updated_at: 2026-07-19 09:30:12
---

# REQ-0042 原型上下文

## 1. 原型策略

本需求不再提供独立于 `REQ-0043` 的完整首页视觉原型。后续 UI 实现必须以 `REQ-0043-miniapp-home-style-optimization` 的附件 `prototype.png` / `prototype.html` 为视觉事实源。

本目录 `prototype.html` 仅用于表达局部边界：当前首页搜索框上方的品牌展示部分是自定义导航栏；右侧“门店信息”入口不属于自定义导航栏；右侧分享和关闭来自小程序原生能力；搜索框保持在导航栏下方。

## 2. 参考优先级

```text
当前 src/miniapp/pages/index/index.wxml 的 brand-header 结构
  > REQ-0043 prototype.png / prototype.html
  > REQ-0043 requirement.md / acceptance.md
  > REQ-0042 acceptance.md 导航栏边界
```

## 3. 与 REQ-0043 的关系

- 不恢复 `REQ-0041` 暖白首页主背景。
- 不手绘模拟微信系统状态栏、分享按钮、关闭按钮或胶囊控件；分享和关闭必须直接使用小程序原生能力。
- 不额外叠加与 `REQ-0043` 原型冲突的标题条。
- 自定义导航栏包含品牌 Logo、店名和副文案。
- 自定义导航栏右侧保留原生分享和关闭按钮避让区。
- “门店信息”入口不属于自定义导航栏。
- 搜索框不属于自定义导航栏，保持在其下方。

## 4. 待导出项

- PNG Golden Reference：使用 `REQ-0043` 附件 PNG，不为 REQ-0042 单独导出完整首页 PNG。
- 真机截图：待后续实现阶段补充顶部品牌导航栏与搜索框的实际截图。

## 5. 不做项提醒

- 不做全小程序统一 custom navigation 壳层。
- 不做后台配置导航栏。
- 不做多门店切换。
- 不把“门店信息”入口纳入自定义导航栏。
- 不手绘模拟分享 / 关闭按钮，必须使用小程序原生能力。
- 不做收藏持久化、证书聚合页、品牌馆独立页。
- 不因导航方案新增 API / DB。
