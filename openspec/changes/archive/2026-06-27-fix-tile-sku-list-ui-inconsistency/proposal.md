## Why

[BUG-0009-tile-sku-list-ui-inconsistency](issues/bugs/BUG-0009-tile-sku-list-ui-inconsistency/) 已评审通过并纳入 `sprint-002`。瓷砖 SKU 列表页（`/admin/tile-skus`）底部分页 DOM 使用废弃的 `page-left` / `brand-pagination-right` 结构，与用户管理页及 BUG-0002 修复后的品牌管理页不一致；`table-card` 内存在多余的「SKU 列表」标题行，与 `page-hero` 及 REQ-0006 列表原型信息架构重复。

`add-tile-sku-management` 尚未归档；REQ-0006 **AC-051**（分页与表格模式复用）与 **AC-054**（列表原型并排）因此项未达标。根据项目规则，验收后发现的 UI 一致性缺陷 MUST 使用新的 `fix-*` change 修复。

## What Changes

- 将 `TileSkuManagementPage.tsx` 底部分页 DOM 对齐 `UserManagementPage.tsx`（`page-summary` + `page-right` + `page-buttons` + `page-size-wrap`）。
- 移除 `table-card` 内 `table-head` / `table-title` / `table-note` 重复标题行。
- 补充 `TileSkuManagementPage` Vitest：断言分页结构与无 `table-head`（参考 `BrandManagementPage.test.tsx`）。
- 更新 change `trace.md` 与用户管理页分页并排验收记录。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `/admin/tile-skus` 列表页分页与表格卡片结构 |
| REQ-0006 | 满足 AC-019～AC-021 视觉结构、AC-051、AC-054；不修改 CRUD/筛选业务逻辑 |
| API | 不变 |
| 数据库 | 不变 |
| Orval | 不需要 |
| MinIO | 不变 |

## Rollback Plan

若修复引起列表布局异常，可回滚本 change 的 TSX/测试改动：

1. 恢复 `TileSkuManagementPage.tsx` 分页与 table-card DOM。
2. 移除新增 Vitest（若有）。
3. 保留 BUG 与 OpenSpec 记录，重新评估替代方案。

回滚不涉及 API、数据库或对象存储。
