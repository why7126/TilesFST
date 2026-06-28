## Context

- **缺陷**：[BUG-0017-user-reset-password-confirm-ui-inconsistency](issues/bugs/archive/BUG-0017-user-reset-password-confirm-ui-inconsistency/)
- **现状**：
  - `UserManagementPage.tsx`：`handleResetPassword` 首行 `window.confirm` 后直调 `resetUserPassword`。
  - 同页 `statusConfirmTarget` / `deleteTarget` 已 DS modal 化（BUG-0016 / `fix-admin-list-status-action-confirm` archived）。
  - `ResetPasswordDialog` 已是 DS modal（结果弹窗，非本 change）。
- **父需求/参考**：REQ-0005-user-management、REQ-0007（类目启停 modal）、REQ-0008（品牌启停先例）
- **Golden Reference**：
  1. 同页 `statusConfirmTarget` modal（`UserManagementPage.tsx`）
  2. `TileCategoryManagementPage.tsx` 启停 confirm（L423–466）
  3. `issues/bugs/archive/BUG-0017-user-reset-password-confirm-ui-inconsistency/acceptance.md`

## Conflict Resolution

| 检查项 | BUG-0017 / Golden Reference | 当前实现 | 决议 |
|--------|----------------------------|---------|------|
| 重置前 confirm | DS modal，确认后 API | `window.confirm` | **ADDED** 以 BUG-0017 为准 |
| 重置后展示密码 | `ResetPasswordDialog` | 已实现 | **冻结** 不修改结果弹窗逻辑 |
| 冻结/删除 confirm | BUG-0016 已交付 | DS modal | **冻结** 仅回归验收 |
| 类目/品牌启停 | 已 archive | DS modal | **冻结** 仅回归验收 |

## Goals / Non-Goals

**Goals:**

- `/admin/users` 重置密码 confirm 符合 BUG-0017 acceptance AC-001～AC-010。
- modal 结构、取消行为、Vitest 门禁对齐类目启停 / 同页冻结 confirm。
- 成功后 `ResetPasswordDialog` 与 Toast **不回归**。

**Non-Goals:**

- 后端 API、Orval、SQLite 变更。
- 修改 `ResetPasswordDialog` 业务逻辑（除非最小接线）。
- 抽取共享 `AdminConfirmDialog`（可选后续）。
- 用户冻结/解冻/删除、SKU/品牌/类目 confirm（独立 scope）。

## Decisions

### D1：页面内联 modal（非新组件）

- 与 `fix-admin-list-status-action-confirm` / `fix-brand-status-confirm` 一致：inline JSX，不新增 shared 组件。

### D2：State 机

- `resetPasswordConfirmTarget: UserAdminItem | null`
- 行内「重置密码」→ `setResetPasswordConfirmTarget(user)`（**不** `void handleResetPassword` 直调 API）
- modal 主按钮 → `handleResetPasswordConfirm` → `resetUserPassword` → `setResetPassword(password)` + `setNotice('密码已重置')` → 关闭 confirm modal
- 与 `statusConfirmTarget` / `deleteTarget` **分离** state

### D3：文案（初稿）

| 操作 | 标题 | 正文 | 主按钮 |
|------|------|------|--------|
| 重置密码 | 重置密码 | 确认为用户「{username}」重置密码？重置后将生成新随机密码。 | 确认重置 |

### D4：无障碍

- `role="dialog"`、`aria-modal="true"`、`aria-labelledby` 指向标题 id；正文 `page-desc`。

### D5：API / 权限冻结

- 不修改 OpenAPI、权限、Orval。

## 验收 Gate

- **视口**：1280×1024（可选并排类目启停 confirm）。
- **Checklist**：见 `trace.md`（≥8 项）。
- **回归**：`UserManagementPage.test.tsx` 冻结/删除用例；`BrandManagementPage` / `TileCategoryManagementPage` 启停用例 MUST pass。
- **来源**：`issues/bugs/archive/BUG-0017-user-reset-password-confirm-ui-inconsistency/acceptance.md`。
