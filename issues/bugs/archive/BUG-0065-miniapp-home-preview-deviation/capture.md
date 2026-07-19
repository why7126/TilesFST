---
bug_id: BUG-0065-miniapp-home-preview-deviation
title: 微信小程序首页预览效果与 REQ-0041 原型和验收差异明显
status: done
severity: high
source: 用户微信开发者工具预览截图反馈
captured_via: capture
classification_rationale: 已有 REQ-0041 与 add-miniapp-home 实现后，实际小程序预览在整体色彩、布局、内容加载和模块完整性上明显偏离原型与验收标准，属于已交付能力的验收偏差而非新需求。
related_requirement: REQ-0041-miniapp-home
related_change: null
source_change: add-miniapp-home
created_at: 2026-07-16 11:33:39
updated_at: 2026-07-19 15:32:13
---

# BUG-0065 微信小程序首页预览效果与 REQ-0041 原型和验收差异明显

## 原始反馈

用户在微信小程序内预览当前实现后反馈：

> 这是在微信小程序里面预览的效果，与原型差异特别大，不论是整体色彩，布局，还是内容（都没加载出来）

截图证据：

- `screenshots/miniapp-preview-deviation.png`

## 现象摘要

- 首页整体视觉与 REQ-0041 原型差异明显：色彩、页面层级、模块密度和品牌质感不足。
- 页面内容未按预期加载：截图中未展示 Banner、快捷找砖入口、新品推荐、热销推荐和完整品牌服务卡片。
- 当前只看到顶部标题、门店信息入口、搜索框、空商品提示、品牌服务标题和底部 TabBar。
- 空态占据大面积首屏区域，导致首页首屏没有形成“品牌数字展厅”的核心视觉和内容闭环。

## 初步影响

| 影响面 | 说明 |
|---|---|
| 小程序首页 UI | 与 `prototype/miniapp/prototype.html` / `prototype.png` 的布局和视觉气质不一致 |
| 内容加载 | Banner、快捷入口、新品/热销、服务区内容未正常展示或缺少可用兜底 |
| 验收 | 可能不满足 REQ-0041 的 AC-002、AC-006、AC-007、AC-008、AC-009、AC-UI-001、AC-STATE-003 |
| 交付信心 | 当前预览难以作为终端客户数字展厅首屏验收 |

## 待补充

- 对比原型截图，逐项确认模块顺序、色彩、间距、圆角、Banner 视觉和服务区卡片差异。
- 确认内容没加载出来的根因：后端未启动、接口地址不可访问、测试数据缺失、接口筛选条件过严，或小程序请求失败。
- 确认是否需要提供小程序预览 seed/demo 数据，保证无真实后台数据时也能展示符合原型的演示内容。
- 后续 `/bug-complete` 时补齐 root cause、workaround、acceptance 和 trace。
