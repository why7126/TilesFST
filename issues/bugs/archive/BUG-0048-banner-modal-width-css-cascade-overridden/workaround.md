---
bug_id: BUG-0048-banner-modal-width-css-cascade-overridden
status: pending_review
created_at: 2026-06-28 18:42:00
updated_at: 2026-06-28 18:42:00
---

# 临时规避方案

## 1. 可用性规避

该缺陷不阻断 Banner 新增/编辑、保存或取消：

1. 约 **520px** 弹窗内仍可完成全部字段填写与提交（纵向滚动由 BUG-0033 保障）。
2. 将浏览器窗口最大化或提高视口高度，可改善纵向可视区域（**横向仍约 520px**，无法通过窗口大小消除）。
3. 浏览器缩放（Zoom out）可间接增加可视横向空间（非正式方案，影响全页可读性）。

## 2. 开发/验收规避

正式修复前：

- **不可**以「源 CSS 含 880px」或 Vitest regex 作为 BUG-0040 宽度验收 pass 条件。
- 验收 **MUST** 使用 DevTools Computed `width` 或并排 SKU 弹窗对比。
- `fix-banner-list-and-modal-ui` **SHOULD NOT archive**，直至本 BUG 闭环。

## 3. 运营规避

字段较多时（SKU 详情跳转、双列 grid + 图片区）：

1. 利用 `.modal-body` 纵向滚动查看全部字段。
2. 分步填写后滚动至底部保存。

## 4. 风险说明

上述规避 **不能**消除：

- Banner 弹窗实际宽度约 520px，明显窄于 SKU 880px。
- 双列 grid、图片上传区、Combobox 横向偏紧。
- BUG-0040 修复意图未在运行时达成。

须进入 `/bug-review BUG-0048 --approve`，通过 `fix-banner-modal-width-css-cascade`（或补修 `fix-banner-list-and-modal-ui`）正式修复。
