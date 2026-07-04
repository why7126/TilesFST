---
bug_id: BUG-0054-admin-content-padding-too-large
title: 管理端全局右侧内容区域内边距过大 - 临时规避方案
severity: medium
status: pending_review
owner: product
created_at: 2026-07-03 18:24:49
updated_at: 2026-07-03 18:24:49
related_requirement: REQ-0013-admin-shell-padding-refine
---

# 临时规避方案

## 是否存在可接受规避

暂无产品级可接受规避方案。

该问题来自管理端全局 Shell padding 与内容宽度策略，终端用户无法通过页面内设置消除右侧内容区域留白。浏览器缩放、手动拖宽窗口或折叠侧栏只能部分改善可视面积，不能解决 `content-inner` 宽度上限和页面级 max-width 分裂。

## 临时操作建议

在正式修复前，可采用以下临时方式降低影响：

1. 宽屏办公时可折叠侧栏，释放一部分横向空间。
2. 列表页可优先使用筛选和分页减少横向阅读压力。
3. 日志审计、SKU 等宽表格页面可在较大视口下使用，避免窄窗口进一步压缩内容。

## 风险

- 浏览器缩放会影响文字可读性，不建议作为正式方案。
- 针对单页临时 CSS override 会继续扩大页面级布局分裂，不建议在正式修复前采用。
- 若只修复日志审计页，会遗漏 SKU、系统设置等同源问题。

## 正式修复建议

通过 `fix-admin-content-padding-too-large` 类 OpenSpec Change 统一调整管理端 Shell 与页面级内容宽度策略，并完成多视口、多页面回归验收。
