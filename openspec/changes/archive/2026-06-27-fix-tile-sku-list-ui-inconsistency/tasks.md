## 1. 准备与定位

- [x] 1.1 阅读 `BUG-0009-tile-sku-list-ui-inconsistency` 的 bug.md、root-cause.md、acceptance.md、review.md
- [x] 1.2 对照 `UserManagementPage.tsx` 与 `BrandManagementPage.tsx`（BUG-0002 修复后）分页 DOM
- [x] 1.3 检查 `TileSkuManagementPage.tsx` 当前分页与 `table-head` 结构
- [x] 1.4 确认不涉及 API、数据库、Orval、MinIO 变更

## 2. 列表页 UI 修复

- [x] 2.1 将底部分页 DOM 改为 `page-summary` + `page-right` + `page-buttons` + `page-size-wrap`
- [x] 2.2 移除 `table-card` 内 `table-head` / `table-title` / `table-note` 区块
- [x] 2.3 保持分页功能：翻页、每页 10/20/50/100、筛选条件保留、切换 page_size 重置 page=1
- [x] 2.4 复用 `user-management.css` 既有分页类名；MUST NOT 新增裸 Hex

## 3. 测试

- [x] 3.1 新增或更新 `TileSkuManagementPage.test.tsx`：分页 DOM 对齐、无 table-head（参考 `BrandManagementPage.test.tsx`）
- [x] 3.2 运行 `cd src/web && npx vitest run src/pages/admin/TileSkuManagementPage`（或等价路径）
- [x] 3.3 运行 `cd src/web && npm run build`

## 4. 并排验收与追溯

- [x] 4.1 1440×1024 下 `/admin/tile-skus` 与 `/admin/users` 分页并排对比
- [x] 4.2 对照 `tile-sku-management-list.html` 与 BUG acceptance AC-001～AC-009，记录于本 change `trace.md`
- [x] 4.3 更新 `BUG-0009-tile-sku-list-ui-inconsistency/trace.md` 中 `openspec_changes` 状态
- [x] 4.4 评估是否需 `docs/knowledge-base/incidents/` 沉淀（本缺陷为 UI 一致性，通常不需要）
