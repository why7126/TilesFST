## 1. 准备与定位

- [x] 1.1 阅读 `BUG-0011-tile-sku-modal-content-overflow` 的 bug.md、root-cause.md、acceptance.md、review.md
- [x] 1.2 检查 `TileSkuFormModal.tsx` 与 `tile-sku-management.css` 当前弹窗 DOM/CSS
- [x] 1.3 确认不涉及 API、数据库、Orval、MinIO 变更

## 2. 弹窗滚动布局修复

- [x] 2.1 为 `.sku-modal-card .modal-body` 增加 `flex: 1; min-height: 0; overflow-y: auto`（或等价 scroll wrapper）
- [x] 2.2 确保 `.modal-head`、`.modal-footer` 不参与滚动（`flex-shrink: 0`）
- [x] 2.3 保持 `.sku-modal-card` 的 `max-height: calc(100vh - 64px)` 与 `overflow: hidden`
- [x] 2.4 验证新增/编辑两种 mode 均正常

## 3. 测试

- [x] 3.1 补充或更新 `TileSkuFormModal` Vitest：断言 modal-body 滚动布局
- [x] 3.2 运行 `cd src/web && npx vitest run src/features/admin/components/TileSkuFormModal`（或等价路径）
- [x] 3.3 运行 `cd src/web && npm run build`

## 4. 矮视口验收与追溯

- [x] 4.1 在 1440×900、1280×720、1920×1080 非全屏下验收滚动至底部字段与 footer
- [x] 4.2 对照 REQ-0006 AC-022 与 BUG acceptance AC-001～AC-008，记录于本 change `trace.md`
- [x] 4.3 更新 `BUG-0011-tile-sku-modal-content-overflow/trace.md` 中 `openspec_changes` 状态
- [x] 4.4 评估是否需 `docs/knowledge-base/incidents/` 沉淀（本缺陷为 UI 布局，通常不需要）
