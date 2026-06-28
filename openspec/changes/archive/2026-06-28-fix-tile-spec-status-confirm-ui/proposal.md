## Why

[BUG-0037-tile-spec-status-confirm-ui-inconsistency](issues/bugs/archive/BUG-0037-tile-spec-status-confirm-ui-inconsistency/) 已评审通过（REV-BUG-0037-001）。`/admin/tile-specs` 行内「启用」「停用」「删除」虽已有二次确认，但使用简化内联 `confirm-card` 模板，与 `TileCategoryManagementPage` / `BrandManagementPage` DS confirm modal 在 DOM 结构、标题区 × 关闭、描述 Typography、语义化主按钮及停用后果说明等方面不一致，REQ-0009 AC-013 / AC-018 未满足。

`fix-tile-spec-admin-ui`（BUG-0027/28/29）**有意排除** confirm 弹窗对齐；本 change **仅**修复启停/删除 confirm UI/UE。

## What Changes

- **启停 confirm**：`TileSpecManagementPage` 启停 confirm markup 对齐类目/品牌页（`modal-close`、`page-desc`、「确认启用/确认停用」）；停用正文补「停用后前台将不再展示该规格。」
- **删除 confirm**：主按钮改为「删除规格」+ `btn primary`；移除 `danger` 变体与无效 `confirm-card` class。
- **确认前不调 API**：行为不变；取消/遮罩/× 关闭 MUST NOT 调用 API。
- **无障碍**：补 `aria-labelledby`；结构对齐 Golden Reference。
- **测试**：`TileSpecManagementPage.test.tsx` 新增停用 confirm 门禁；回归既有分页/刷新用例及类目/品牌 confirm 用例。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `web-client`：MODIFIED「管理端瓷砖规格管理页」— 启停/删除 confirm MUST 复用类目/品牌 modal 结构与文案规范；MUST NOT 使用简化 `confirm-card` 模板。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 无变更 |
| 前端 Web 管理端 | `TileSpecManagementPage.tsx`、可选 vitest |
| API / Orval | 无 |
| 数据库 | 无 |
| Design System | 无新 Token；复用既有 `modal-*` 与 `user-management.css` / `brand-management.css` |
| 测试 | Vitest 新增/更新 |
| Docker | web 镜像重建（可选） |
| 依赖 | `add-tile-spec-management`、`fix-tile-spec-admin-ui` 已 archived（分页/表单/刷新基线） |
| 关联 BUG | BUG-0027/28/29 职责独立；MUST NOT 混 scope |

## Rollback Plan

1. 回滚 `TileSpecManagementPage.tsx` 中启停/删除 confirm JSX 至 fix 前版本。
2. 回滚 Vitest 新增用例。
3. 若已 archive，从 `openspec/specs/web-client/spec.md` 恢复 MODIFIED requirement 前版本。
4. 重新标记 `BUG-0037` 为未修复并保留验收失败记录。
