## Why

[BUG-0016-admin-list-status-action-confirm-missing](issues/bugs/archive/BUG-0016-admin-list-status-action-confirm-missing/) 已评审通过（REV-BUG-0016-001，sprint-002）。管理端 **用户管理** 与 **瓷砖 SKU** 列表页部分状态变更行内操作（冻结/解冻、删除、上架/下架/恢复）点击后直接调用 API，或仍使用 `window.confirm`，与已归档 REQ-0007/REQ-0008 及 `BrandManagementPage` / `TileCategoryManagementPage` 的 DS modal 二次确认模式不一致，存在误触风险。

品牌启停/删除已在 `fix-brand-status-confirm` 闭环，**不在本 change scope**。重置密码 confirm UI 统一归 **BUG-0017**，本 change **MUST NOT** 修改重置密码交互。

## What Changes

- **用户冻结/解冻**：`UserManagementPage` 增加独立 `statusConfirmTarget` + confirm modal；确认前 MUST NOT 调用 `updateUserStatus`。
- **用户删除**：移除 `window.confirm`；复用 `deleteTarget` + modal 结构（对齐类目/品牌删除）。
- **SKU 上架/下架/恢复**：`TileSkuManagementPage` 增加 `statusConfirmTarget`（或 action 枚举）；确认前 MUST NOT 调用 `publishTileSku` / `unpublishTileSku`。
- **文案与结构**：modal MUST 使用 `modal-backdrop` + `modal-card` + head/body/footer；参考 `brand-status-confirm-context.md` / `tile-category-status-confirm-context.md`。
- **测试**：更新 `UserManagementPage.test.tsx`、`TileSkuManagementPage.test.tsx`；确认前 mock API MUST NOT 被调用。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `web-client`：**ADDED**「用户列表状态变更二次确认」与「SKU 列表上下架二次确认」—— `/admin/users` 冻结/解冻/删除与 `/admin/tile-skus` 上架/下架/恢复须 DS modal 确认；确认前不得调 API。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 无变更 |
| 前端 Web 管理端 | `UserManagementPage.tsx`、`TileSkuManagementPage.tsx` |
| API / Orval | 无 |
| 数据库 | 无 |
| Design System | 无新 Token；复用既有 `modal-*` 与 `user-management.css` / `tile-sku-management.css` |
| 测试 | Vitest 更新/新增 |
| Docker | web 镜像重建（可选） |
| 依赖 | `add-user-management`、`add-tile-sku-management` 基线；参考 `fix-brand-status-confirm`、`fix-tile-category-management-refine`（已 archive） |
| 关联 BUG | BUG-0017（重置密码 UI）职责独立 |

## Rollback Plan

1. 回滚 `UserManagementPage` / `TileSkuManagementPage` 中 confirm modal state 与 JSX。
2. 恢复用户删除 `window.confirm` 与用户冻结直调 API 行为（仅作紧急回滚，不推荐）。
3. 回滚 Vitest 至修复前断言。
4. 若已 archive，从 `openspec/specs/web-client/spec.md` 移除 ADDED requirement 条目。
5. 重新标记 `BUG-0016` 为未修复并保留验收失败记录。
