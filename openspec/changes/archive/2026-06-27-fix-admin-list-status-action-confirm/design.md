## Context

- **缺陷**：[BUG-0016-admin-list-status-action-confirm-missing](issues/bugs/BUG-0016-admin-list-status-action-confirm-missing/)
- **现状**：
  - `UserManagementPage.tsx`：`handleFreeze` 直调 `updateUserStatus`；`handleDelete` 使用 `window.confirm`。
  - `TileSkuManagementPage.tsx`：`handlePublish` / `handleUnpublish` 直调 API；同页删除已有 `deleteTarget` modal。
  - `BrandManagementPage` / `TileCategoryManagementPage`：启停/删除 confirm 已交付（Golden Reference）。
- **父需求/参考**：REQ-0008、REQ-0007、REQ-0005-user-management、REQ-0006-tile-sku-management
- **原型/context**：
  1. `issues/requirements/REQ-0008-brand-status-confirm/prototype/web/brand-status-confirm-context.md`
  2. `issues/requirements/REQ-0007-tile-category-management-refine/prototype/web/tile-category-status-confirm-context.md`
  3. `issues/bugs/BUG-0016-admin-list-status-action-confirm-missing/acceptance.md`

## Conflict Resolution

| 检查项 | BUG-0016 / Golden Reference | 当前实现 | 决议 |
|--------|----------------------------|---------|------|
| 用户冻结/解冻 | modal 确认后 API | 直调 API | **ADDED** 以 BUG-0016 为准 |
| 用户删除 | DS modal | `window.confirm` | **ADDED** modal 化 |
| SKU 上下架 | modal 确认后 API | 直调 API | **ADDED** 以 BUG-0016 为准 |
| 重置密码 confirm | BUG-0017 独立 | `window.confirm` | **冻结** 本 change 不修改 |
| 品牌/类目 confirm | 已 archive | 已实现 | **冻结** 仅回归验收 |

## Goals / Non-Goals

**Goals:**

- `/admin/users` 冻结/解冻/删除符合 BUG-0016 acceptance AC-001～AC-004。
- `/admin/tile-skus` 上架/下架/恢复符合 AC-005～AC-007。
- modal 结构、取消行为、Vitest 门禁对齐品牌/类目先例。
- 品牌/类目/SKU 删除既有 confirm **不回归**。

**Non-Goals:**

- 后端 API、Orval、SQLite 变更。
- 抽取共享 `AdminConfirmDialog` 组件（可选后续优化，非阻塞）。
- 重置密码 confirm UI（→ BUG-0017）。
- 品牌列表启停/删除（已满足 REQ-0008）。

## Decisions

### D1：复用页面内联 modal 模式（非新组件）

- 与 `fix-brand-status-confirm` 一致：在页面内复制 `modal-backdrop` JSX，不引入新 shared 组件（降低 scope）。
- 样式复用 `user-management.css` / 类目页 modal 类名；SKU 页可沿用同页删除 modal 样式。

### D2：用户页 state 机

- `statusConfirmTarget: UserAdminItem | null` — 冻结/解冻共用；由 `user.status` 推导 enable/disable 文案。
- `deleteTarget: UserAdminItem | null` — 替换 `window.confirm` 路径；与 status confirm **分离** state。
- 行内按钮 → 设置 target → 打开 modal → 主按钮 → API → Toast + `loadUsers()`。

### D3：SKU 页 state 机

- `statusConfirmTarget: TileSkuAdminItem | null` + `statusConfirmAction: 'publish' | 'unpublish' | null`（或等价）。
- 上架/恢复共用 publish API；下架用 unpublish API。
- 与 `deleteTarget` **分离**。

### D4：文案（初稿，apply 时可微调）

| 操作 | 标题 | 正文要点 |
|------|------|---------|
| 冻结用户 | 冻结用户 | 确认冻结用户「{username}」？冻结后该用户将无法登录。 |
| 解冻用户 | 解冻用户 | 确认解冻用户「{username}」？ |
| 删除用户 | 删除用户 | 确认删除用户「{username}」？此操作不可恢复。 |
| 下架 SKU | 下架 SKU | 确认下架 SKU「{name}」？下架后前台将不再展示该商品。 |
| 上架/恢复 SKU | 上架 SKU | 确认上架 SKU「{name}」？ |

### D5：无障碍

- 弹窗 `role="dialog"`、`aria-modal="true"`、`aria-labelledby` 指向标题 id（对齐品牌/类目）。

### D6：API / 权限冻结

- 不修改 OpenAPI、权限边界、Orval。

## 验收 Gate

- **视口**：1280×1024（可选并排类目/品牌 confirm 参考）。
- **Checklist**：见 `trace.md`（≥8 项）。
- **回归**：`BrandManagementPage.test.tsx`、`TileCategoryManagementPage.test.tsx` 启停/删除用例 MUST 保持通过。
- **来源**：`issues/bugs/BUG-0016-admin-list-status-action-confirm-missing/acceptance.md` AC-001～AC-015。
