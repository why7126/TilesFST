## Why

[BUG-0010-tile-sku-modal-subtitle-inconsistency](issues/bugs/archive/BUG-0010-tile-sku-modal-subtitle-inconsistency/) 已评审通过。SKU 新增/编辑弹窗副标题曾使用无样式定义的 `modal-subtitle`，与品牌弹窗 `brand-modal-desc` 的 Typography 不一致，破坏管理端弹窗标题区视觉统一性。

## What Changes

- 在 `user-management.css` 抽取共享 `.modal-desc`（12px、`var(--admin-weak)`）。
- `TileSkuFormModal` / `BrandFormModal` 统一使用 `modal-desc`；移除 `brand-modal-desc`。
- SKU / 品牌弹窗 `.modal-head` 改为自适应高度（`min-height: 64px`）。
- SKU 副标题文案对齐品牌句式，保留 REQ-0006 AC-023「弹窗内不提供状态选择」。
- 补充 `TileSkuFormModal` Vitest 断言。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | SKU + 品牌弹窗标题区 |
| API / DB / Orval | 不变 |

## Rollback Plan

回滚 TSX 与 CSS 中 `.modal-desc` 相关改动；恢复 `brand-modal-desc` 与 `modal-subtitle`。
