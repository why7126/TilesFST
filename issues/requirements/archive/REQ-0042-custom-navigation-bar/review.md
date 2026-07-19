---
review_id: REV-REQ-0042-custom-navigation-bar-001
requirement_id: REQ-0042-custom-navigation-bar
date: 2026-07-19
participants: []
result: approved
created_at: 2026-07-19 09:23:32
updated_at: 2026-07-19 09:30:12
---

# REQ-0042 需求评审

## 评审结论

通过。REQ-0042 已明确以 `REQ-0043-miniapp-home-style-optimization` 为当前首页视觉与信息架构基准，并将当前小程序首页搜索框上方 `brand-header` 中的品牌展示部分定义为自定义导航栏。

本次评审确认：自定义导航栏只包含品牌 Logo、门店名称和品牌副文案等品牌识别元素；右侧“门店信息”入口、门店详情跳转、多门店切换暗示和 `openStoreInfo` 默认点击行为均不纳入自定义导航栏。搜索框继续位于导航栏下方。

## 评审清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试。
- [x] 优先级与依赖合理。
- [x] UI 类原型和实现策略已决，以 `REQ-0043` 深色首页为基准。
- [x] 与现有 REQ 无未说明重复；本需求作为 `REQ-0043` 基准下的首页品牌导航边界细化。

## 条件通过项

- [x] 后续 OpenSpec Change 必须引用 `REQ-0043`，并保持深色首页、四入口、瀑布流和 TabBar 目标不被导航栏调整破坏。
- [x] 后续实现不得把“门店信息”入口放入自定义导航栏，也不得让导航栏整体默认点击进入门店信息页。
- [x] 搜索框保持在自定义导航栏下方，不并入导航栏内部。
- [x] 默认不新增 API、数据库字段或后台配置；若实现阶段发现 contract 缺口，必须在 OpenSpec Change 中明确并同步 API / DB / Orval / docs / tests。

## 后续动作

`/req-opsx REQ-0042-custom-navigation-bar`

## 评审后范围澄清

2026-07-19 09:30:12 补充：自定义导航栏右侧需要分享和关闭两个按钮，且必须直接使用微信小程序原生能力。该补充不恢复“门店信息”入口，也不允许页面内手绘模拟分享、关闭或胶囊控件。
