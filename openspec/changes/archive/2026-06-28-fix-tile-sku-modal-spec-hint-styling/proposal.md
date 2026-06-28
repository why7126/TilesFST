## Why

[BUG-0038-tile-sku-modal-spec-hint-styling](issues/bugs/archive/BUG-0038-tile-sku-modal-spec-hint-styling/) 已评审通过。SKU 编辑弹窗在 `spec_id` 为空（历史 SKU 迁移未匹配）时，规格字段下方提示「历史 SKU 未匹配规格，请手动选择后保存」使用了无 CSS 定义的 `form-hint` 类名，字号与颜色继承浏览器默认 `<p>` 样式，视觉层级高于管理端字段辅助说明规范（`form-help`），在暗色弹窗中过于抢眼。

## What Changes

- `TileSkuFormModal.tsx`：规格未匹配提示 `form-hint` → `form-help`（复用 `user-management.css` 既有样式）。
- `TileSkuFormModal.test.tsx`：补充 `spec_id: null` 编辑模式断言提示文案与 `form-help` 类名。
- **MUST NOT** 新增 `.form-hint` CSS、裸 Hex，或变更提示文案/显隐逻辑。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | 仅 SKU 编辑弹窗、`spec_id` 为空场景 |
| API / DB / Orval | 不变 |
| 小程序 / 店主端 | 不变 |

## Rollback Plan

回滚 `TileSkuFormModal.tsx` 中提示元素 className 改动及新增 Vitest 用例即可；无数据迁移或 API 变更。
