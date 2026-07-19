---
req_id: REQ-0042-custom-navigation-bar
status: done
created_at: 2026-07-17 08:52:22
updated_at: 2026-07-19 11:02:05
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0041-miniapp-home
captured_via: capture
classification_rationale: 用户明确选择“自定义导航栏方案”，属于小程序首页/壳层体验的新增实现方案与交互能力补充，并非既有已交付能力偏差，因此判定为 REQ。
---

# 一句话

把当前小程序首页搜索框上方模块中的品牌展示部分作为自定义导航栏；“门店信息”入口不纳入自定义导航栏，搜索框保持在导航栏下方。

# 原始描述

走自定义导航栏方案。

# 背景与关联

- 父需求：`REQ-0041-miniapp-home`
- 基准需求：`REQ-0043-miniapp-home-style-optimization`
- 涉及端：微信小程序
- 业务价值：明确首页顶部品牌导航栏的内容边界，避免“门店信息”入口与品牌导航混在一起，同时保持 REQ-0043 深色首页、搜索、四入口、瀑布流和 TabBar 目标不变。
- 预期后续：后续 OpenSpec 需将当前 `brand-header` 中 `store-logo`、`store-name`、`store-subtitle` 或等价元素定义为自定义导航栏，并排除 `store-link` / “门店信息”入口与默认 `openStoreInfo` 跳转。

# 待澄清

- [x] 自定义导航栏仅定义当前小程序首页搜索框上方的品牌展示区域。
- [x] 导航栏包含品牌 Logo、店名和品牌副文案；不包含“门店信息”入口。
- [x] 搜索框保持在自定义导航栏下方，不并入导航栏。
- [ ] 若后续仍保留门店信息入口，需要另行确认其页面位置和交互方式。
- [ ] 若后续启用 `navigationStyle: custom`，需要补充状态栏和胶囊按钮安全区验收。

# 探索结论

- 已按 `REQ-0043-miniapp-home-style-optimization` 重新对齐：REQ-0043 是首页样式与信息架构基准。
- REQ-0042 明确当前首页搜索框上方的品牌展示部分为自定义导航栏。
- 当前实现中的“门店信息”入口不纳入自定义导航栏，导航栏整体不得默认绑定门店信息跳转。
- 搜索框保持在自定义导航栏下方，不作为导航栏内部元素。
- 页面不得模拟微信系统状态栏、分享按钮、关闭按钮或胶囊控件。
- REQ-0042 不得改变 REQ-0043 的深色视觉、四入口、全部产品瀑布流和底部 TabBar 目标。

# 分类说明（/capture）

该条目描述小程序首页采用自定义导航栏的实现选择和体验方案，当前没有独立交付基线，因此判定为 REQ，并作为 `REQ-0041-miniapp-home` 的补充需求记录。
