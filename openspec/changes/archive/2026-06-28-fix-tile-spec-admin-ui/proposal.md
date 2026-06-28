## Why

[BUG-0027-tile-spec-list-ui-inconsistency](issues/bugs/archive/BUG-0027-tile-spec-list-ui-inconsistency/)、[BUG-0028-tile-spec-modal-form-layout](issues/bugs/archive/BUG-0028-tile-spec-modal-form-layout/) 与 [BUG-0029-tile-spec-list-not-refresh-after-create](issues/bugs/archive/BUG-0029-tile-spec-list-not-refresh-after-create/) 已评审通过，同属 REQ-0009 瓷砖规格管理页交付后的前端缺口：

1. **BUG-0027**：列表分页使用未定义 `pagination-bar` DOM，未复用用户管理/品牌页标准分页；尺寸名称列 `.size-name` 字号偏离。
2. **BUG-0028**：弹窗字段顺序与 REQ-0009 AC-019 不一致；备注 `textarea` 未 port 整行宽度与固定高度。
3. **BUG-0029**：表单保存成功后 `onSuccess` 仅 Toast，未调用 `loadSpecs()`，列表与 summary stale。

根据项目规则，已交付能力上的缺陷 MUST 使用 `fix-*` change；三 BUG 共享 `TileSpecManagementPage` / `TileSpecFormModal` / `tile-spec-management.css`，合并于本 change。

## What Changes

- **BUG-0027**：`TileSpecManagementPage.tsx` 分页 DOM 对齐 `UserManagementPage`；调整 `.size-name` 视觉 rhythm。
- **BUG-0028**：`TileSpecFormModal.tsx` 字段重排（宽/长 → 只读尺寸名称 → 厚度/排序 → 备注）；`tile-spec-management.css` port `.input`/`.textarea` 宽度与备注固定高度。
- **BUG-0029**：`onSuccess` 回调同时 `setNotice` + `void loadSpecs()`，对齐品牌/SKU 页模式。
- 补充 Vitest（分页 DOM、弹窗字段顺序、保存后 refresh）。
- **不** 变更 API、SQLite、`buildDisplayName()` 语义（保留 `{w}×{l}mm`）、Orval、Docker。

## Capabilities

### New Capabilities

（无。）

### Modified Capabilities

- `web-client`：MODIFIED「管理端瓷砖规格管理页」— 分页 MUST 复用管理端标准模式；弹窗字段顺序与备注整行；保存后 MUST 刷新列表与 summary。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `TileSpecManagementPage.tsx`、`TileSpecFormModal.tsx`、`tile-spec-management.css`、可选 vitest |
| 店主端 / 小程序 / 后端 / DB / Orval | 无 |
| 父需求 | REQ-0009-tile-spec-management |
| 关联 BUG | BUG-0027、BUG-0028、BUG-0029 |
| 前置 Change | `add-tile-spec-management`（功能基线） |

## Rollback Plan

若 UI 修复导致回归，可回滚本 change 的前端改动：

1. 恢复 `TileSpecManagementPage.tsx`、`TileSpecFormModal.tsx`、`tile-spec-management.css` 及新增测试至 fix 前版本。
2. 运行 `cd src/web && pnpm vitest run src/pages/admin/TileSpecManagementPage src/features/admin/components/TileSpecFormModal && pnpm build` 确认通过。

回滚不涉及 API、数据库或部署配置。
