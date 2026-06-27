---
bug_id: BUG-0010-tile-sku-modal-subtitle-inconsistency
title: SKU弹窗副标题与品牌弹窗样式不一致
severity: medium
status: draft
owner: product
discovered_at: 2026-06-27 08:56:54
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_change: null
---

# 缺陷说明

瓷砖 SKU 新增/编辑弹窗标题区副标题与「新增品牌」弹窗不一致：SKU 使用未定义样式的 `modal-subtitle`，品牌使用 `brand-modal-desc`（12px、`var(--admin-weak)`）；SKU 弹窗头部固定 64px 导致副标题排版与品牌弹窗视觉层级不一致。

# 复现步骤

1. admin 登录，打开 `/admin/tile-skus` 新增/编辑 SKU 弹窗。
2. 打开 `/admin/brands` 新增品牌弹窗。
3. 对比标题下方副标题的字号、颜色、行高、与标题间距。

# 期望结果

- SKU 与品牌弹窗副标题 MUST 共用同一 semantic 样式（`.modal-desc`）。
- 弹窗头部 MUST 支持标题 + 副标题自适应高度（`min-height: 64px`）。
- SKU 副标题文案结构与管理端弹窗一致（「维护…、…与…。」），并保留 REQ-0006 AC-023「弹窗内不提供状态选择」语义。

# 实际结果（修复前）

- SKU 使用 `modal-subtitle`，无 CSS 定义，呈现浏览器默认样式。
- 品牌使用 `brand-modal-desc`，样式正确但类名未共享。
- 两弹窗副标题视觉不一致。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 | SKU 弹窗、品牌弹窗标题区（统一 `.modal-desc`） |
| API / DB | 无 |
| REQ-0006 | AC-023 副标题语义保留 |

# 严重等级说明

`medium` — 不阻断功能，但破坏管理端弹窗视觉一致性与 Design System 验收。

# 代码线索

| 线索 | 路径 |
|---|---|
| SKU 弹窗 | `TileSkuFormModal.tsx` |
| 品牌弹窗 | `BrandFormModal.tsx` |
| 共享样式 | `user-management.css` `.modal-desc` |
| SKU 头部布局 | `tile-sku-management.css` |
| 品牌头部布局 | `brand-management.css` |
