## 1. 准备

- [x] 1.1 阅读 BUG-0010 bug.md、root-cause.md、acceptance.md
- [x] 1.2 对照 BrandFormModal 与 TileSkuFormModal 标题区 DOM/CSS

## 2. 共享样式与组件

- [x] 2.1 在 `user-management.css` 新增 `.modal-desc`
- [x] 2.2 `TileSkuFormModal` 改用 `modal-desc`；更新副标题文案
- [x] 2.3 `BrandFormModal` 改用 `modal-desc`；移除 `brand-modal-desc`
- [x] 2.4 `tile-sku-management.css` / `brand-management.css` 调整 modal-head 自适应布局

## 3. 测试

- [x] 3.1 `TileSkuFormModal.test.tsx` 断言 `.modal-desc` 与文案
- [x] 3.2 运行 `npx vitest run TileSkuFormModal.test.tsx`

## 4. 追溯

- [x] 4.1 更新 BUG-0010 trace.md `openspec_changes`
- [x] 4.2 记录验收于 change `trace.md`
- [x] 4.3 评估 incidents 沉淀（不需要）

## 5. 归档

- [ ] 5.1 `/opsx-archive fix-tile-sku-modal-subtitle-inconsistency`
