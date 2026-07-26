## Why

[BUG-0017-user-reset-password-confirm-ui-inconsistency](issues/bugs/archive/BUG-0017-user-reset-password-confirm-ui-inconsistency/) 已评审通过（REV-BUG-0017-001，sprint-002）。`/admin/users` 行内「重置密码」在调用 API 前使用浏览器原生 `window.confirm`，与同页冻结/删除 confirm modal 及 `TileCategoryManagementPage` 启停确认 DS modal 不一致，破坏管理端 Confirm Dialog 统一性。

`fix-admin-list-status-action-confirm`（BUG-0016）**有意排除**重置密码 confirm；本 change **仅**修复重置**前**确认步骤。`ResetPasswordDialog`（展示一次性随机密码）**不在 scope**。

## What Changes

- **重置密码 confirm**：`UserManagementPage` 增加 `resetPasswordConfirmTarget` + DS confirm modal；MUST NOT 使用 `window.confirm`。
- **确认前不调 API**：点击「重置密码」→ 打开 modal；仅「确认重置」后调用 `POST .../reset-password`。
- **成功后行为不变**：API 成功 → Toast「密码已重置」→ 打开既有 `ResetPasswordDialog`。
- **结构对齐**：`modal-backdrop` + `modal-card` + head/body/footer；参考同页 `statusConfirmTarget` 与类目启停 confirm。
- **测试**：`UserManagementPage.test.tsx` 新增 confirm 门禁；`window.confirm` spy 断言未调用；回归冻结/删除用例。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `web-client`：**ADDED**「用户重置密码二次确认」—— `/admin/users` 重置密码须 DS modal 确认；禁止 `window.confirm`；确认前不得调 reset-password API。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 无变更 |
| 前端 Web 管理端 | `UserManagementPage.tsx` |
| API / Orval | 无 |
| 数据库 | 无 |
| Design System | 无新 Token；复用既有 `modal-*` 与 `user-management.css` / `brand-management.css` |
| 测试 | Vitest 新增/更新 |
| Docker | web 镜像重建（可选） |
| 依赖 | `add-user-management` 基线；`fix-admin-list-status-action-confirm` 已归档（同页 freeze/delete modal 参考） |
| 关联 BUG | BUG-0016 职责独立；MUST NOT 混 scope |

## Rollback Plan

1. 回滚 `UserManagementPage` 中 `resetPasswordConfirmTarget` modal 与 handler 接线。
2. 恢复 `handleResetPassword` 内 `window.confirm`（仅作紧急回滚，不推荐）。
3. 回滚 Vitest 新增用例。
4. 若已 archive，从 `openspec/specs/web-client/spec.md` 移除 ADDED requirement。
5. 重新标记 `BUG-0017` 为未修复并保留验收失败记录。
