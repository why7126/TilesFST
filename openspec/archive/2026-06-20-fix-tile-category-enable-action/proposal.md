## Why

**BUG-0001-tile-category-enable-missing**（`issues/bugs/archive/BUG-0001-tile-category-enable-missing/`）：瓷砖类目管理页对 **停用且 SKU=0** 的行错误隐藏「启用」按钮，运营无法通过 UI 重新启用类目。后端 `POST /api/v1/admin/tile-categories/{id}/enable` 已实现；缺陷为 `TileCategoryManagementPage.tsx` 将 `canDeleteCategory` 与启停按钮展示错误绑定（`deletable ? null : 启用`）。本 change 为 **fix-*** 回归修复，对齐 `REQ-0005-tile-category-management` AC-015 与 `BrandManagementPage` 模式。

## What Changes

- **列表操作列**：停用行 **始终** 展示「启用」；启用行展示「停用」；「删除」独立按 `canDeleteCategory` 控制（与品牌管理一致）。
- **测试**：新增/扩展 vitest，覆盖停用+SKU=0 行同时含「启用」「删除」；启用行无「删除」。
- **追溯**：修复后更新 BUG trace → `done`；可选沉淀 incidents 条目。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `web-client`：MODIFIED「管理端瓷砖类目管理页」— 列表行启停/删除操作列渲染规则。

## Impact

| 影响面 | 说明 |
|---|---|
| 前端 Web 管理端 | `TileCategoryManagementPage.tsx` |
| 后端 / API / Orval | 无 |
| 数据库 | 无 |
| 测试 | vitest（类目页操作列） |
| Docker | web 镜像重建（页面逻辑） |
| 关联 | `add-tile-category-management`；父 REQ-0005 |

## Rollback Plan

1. 回滚 `TileCategoryManagementPage.tsx`（及 vitest）至修复前 commit。
2. 重新 `npm run build` / 部署 web 镜像。
3. 临时规避：admin 调用 `POST .../enable`（见 BUG workaround.md）。
