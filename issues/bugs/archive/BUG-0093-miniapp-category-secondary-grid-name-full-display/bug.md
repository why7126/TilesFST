---
bug_id: BUG-0093-miniapp-category-secondary-grid-name-full-display
title: 小程序分类页二级类目卡片 3 列布局导致名称未完整显示
severity: medium
status: done
owner:
discovered_at: 2026-07-30 22:59:39
environment: miniapp
related_requirement: REQ-0045-category-list-page
related_change: fix-miniapp-category-secondary-grid-name-display
related_bug: BUG-0077-miniapp-category-secondary-name-truncated
created_at: 2026-07-30 23:02:53
updated_at: 2026-07-31 00:08:23
---

# 缺陷概述

微信小程序分类列表页右侧二级类目卡片当前一行显示 3 个，单个卡片宽度不足，导致较长二级类目名称无法完整显示，被省略号截断。用户无法在分类页直接识别完整类目名称，影响从分类入口选择商品列表的效率。

该问题与历史缺陷 `BUG-0077-miniapp-category-secondary-name-truncated` 相关。历史缺陷已归档，但本次截图显示二级类目卡片区域仍存在名称截断问题，因此按回归/验收残留缺陷记录。

# 复现步骤

1. 打开微信小程序。
2. 点击底部导航“分类”进入分类列表页。
3. 在左侧一级类目中选择包含较长二级类目名称的类目，例如“木纹砖产品”。
4. 查看右侧二级类目卡片列表。
5. 观察二级类目卡片是否为一行 3 个，以及名称是否被省略号截断。

# 期望结果

- 二级类目卡片在分类页右侧区域一行显示 2 个。
- 所有二级类目名称必须完整显示，不出现 `...` 或其他省略截断。
- 长名称允许换行展示，但不得遮挡卡片边框、相邻卡片、标题或“查看全部商品”入口。
- 点击二级类目后仍进入对应分类商品列表。

# 实际结果

- 二级类目卡片当前一行显示 3 个。
- 卡片宽度不足，导致较长类目名称被截断。
- 截图中可见 `600X1200 仿古精雕...`、`800X800 仿古精雕...`、`750X1500 仿古精雕...` 等名称未完整展示。

# 影响范围

- 终端：微信小程序。
- 页面：分类列表页。
- 区域：右侧二级类目卡片列表。
- 用户影响：用户无法直接从卡片文案辨识完整二级类目名称，可能误选或需要额外进入商品列表确认。
- 技术影响：预计主要涉及小程序分类页布局样式和文本展示规则；不应影响分类接口、类目数据结构和商品列表路由。

# 严重等级说明

严重等级为 `medium`。

理由：该缺陷影响分类页核心入口的可读性和选择效率，但未阻断用户点击类目进入商品列表，也未涉及数据丢失、权限、安全或接口不可用。由于历史同类缺陷已修复归档，本次应重点按回归问题处理，并在多端与长文本场景补足验收。

# 证据

- 用户截图：`screenshots/category-secondary-grid-truncated.png`
- 关联需求：`REQ-0045-category-list-page`
- 关联历史缺陷：`BUG-0077-miniapp-category-secondary-name-truncated`
