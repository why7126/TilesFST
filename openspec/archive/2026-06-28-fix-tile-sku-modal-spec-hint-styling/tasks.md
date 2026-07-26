## 1. 准备

- [x] 1.1 阅读 BUG-0038 bug.md、root-cause.md、acceptance.md
- [x] 1.2 对照 `UserFormModal` / `BrandFormModal` 的 `form-help` 用法与 `user-management.css` 定义

## 2. 实现

- [x] 2.1 `TileSkuFormModal.tsx`：提示元素 `form-hint` → `form-help`
- [x] 2.2 确认 MUST NOT 新增 CSS 或修改提示文案/显隐条件

## 3. 测试

- [x] 3.1 `TileSkuFormModal.test.tsx`：补充 `spec_id: null` 编辑模式断言提示与 `form-help` 类名
- [x] 3.2 运行 `cd src/web && npx vitest run TileSkuFormModal.test.tsx`

## 4. 追溯与验收

- [x] 4.1 更新 BUG-0038 trace.md `openspec_changes` 与 change `trace.md`
- [x] 4.2 按 acceptance.md AC-001～AC-006 与 screenshots/tile-sku-modal-spec-hint-styling.png 并排验收（Vitest 覆盖 AC-001/003/004/006；AC-002 依赖 `form-help` + `user-management.css`）
- [x] 4.3 评估 `docs/knowledge-base/incidents/` 沉淀（不需要 — 纯 UI 类名修复）

## 5. 归档

- [x] 5.1 `/opsx-archive fix-tile-sku-modal-spec-hint-styling`
