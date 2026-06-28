## Why

[BUG-0014-tile-sku-publish-action-missing](issues/bugs/archive/BUG-0014-tile-sku-publish-action-missing/) 已评审通过。瓷砖 SKU 列表页（`/admin/tile-skus`）对 **已下架**（`status=DISABLED`）行错误隐藏「上架/恢复」操作，运营下架后无法从 UI 恢复上架。后端 `POST /api/v1/admin/tile-skus/{id}/publish` 已实现；缺陷为 `TileSkuManagementPage.tsx` 操作列对 `DISABLED` 显式渲染 `null`（`item.status !== 'DISABLED' ? 上架 : null`）。

`add-tile-sku-management` 尚未归档；REQ-0006 **AC-018**（操作列）、**AC-037**（上下架/恢复）因此项未达标。根据项目规则，验收后发现的功能缺失 MUST 使用新的 `fix-*` change 修复。

## What Changes

- 修改 `TileSkuManagementPage.tsx` 操作列：非 `PUBLISHED` 行（含 `DISABLED`）MUST 展示 publish 操作；`DISABLED` 文案为「恢复」，其余为「上架」；与 delete 独立渲染（对齐 BUG-0001 / 类目管理修复模式）。
- 补充 `TileSkuManagementPage` Vitest：mock `DISABLED` 行含「恢复」；`PUBLISHED` 行含「下架」。
- 更新 change `trace.md` 与 BUG acceptance 验收记录。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `web-client`：MODIFIED「管理端瓷砖 SKU 管理页」— 列表行上下架/恢复操作列渲染规则。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `/admin/tile-skus` 列表页操作列 |
| REQ-0006 | 满足 AC-018、AC-037、FR-007；不修改 CRUD/筛选/弹窗业务逻辑 |
| API | 不变 |
| 数据库 | 不变 |
| Orval | 不需要 |
| 测试 | vitest（SKU 列表操作列） |
| Docker | web 镜像重建（页面逻辑） |
| 关联 | `add-tile-sku-management`；参考 `fix-tile-category-enable-action` |

## Rollback Plan

若修复引起操作列异常，可回滚本 change 的 TSX/测试改动：

1. 恢复 `TileSkuManagementPage.tsx` 操作列条件渲染至修复前 commit。
2. 移除新增 Vitest（若有）。
3. 临时规避：admin 调用 `POST .../publish`（见 BUG workaround.md）。

回滚不涉及 API、数据库或对象存储。
