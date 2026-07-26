## Context

- **缺陷**：[BUG-0037-tile-spec-status-confirm-ui-inconsistency](issues/bugs/archive/BUG-0037-tile-spec-status-confirm-ui-inconsistency/)
- **现状**：
  - `TileSpecManagementPage.tsx` L329–382：启停/删除 confirm 使用 `<section className="modal-card confirm-card">`，无 `modal-close`，主按钮「确认」，删除用 `btn primary danger`。
  - `confirm-card` 全仓库 CSS 无定义。
  - `TileCategoryManagementPage.tsx` / `BrandManagementPage.tsx` 已 DS modal 化（Golden Reference）。
- **父需求/参考**：REQ-0009-tile-spec-management、REQ-0008-brand-status-confirm、REQ-0005 类目页
- **Golden Reference**：
  1. `TileCategoryManagementPage.tsx` 启停/删除 confirm（L423–505）
  2. `BrandManagementPage.tsx` 启停/删除 confirm（L355–437）
  3. `issues/bugs/archive/BUG-0037-tile-spec-status-confirm-ui-inconsistency/acceptance.md`

## Conflict Resolution

| 检查项 | BUG-0037 / Golden Reference | 当前实现 | 决议 |
|--------|----------------------------|---------|------|
| 启停 confirm 结构 | DS modal + × + page-desc | 简化 confirm-card | **MODIFIED** 以 BUG-0037 为准 |
| 启停主按钮 | 确认启用/确认停用 | 泛化「确认」 | **MODIFIED** |
| 停用后果说明 | 含前台不再展示 | 无 | **MODIFIED** |
| 删除 confirm | 「删除规格」+ btn primary | 「删除」+ danger | **MODIFIED** |
| 分页/表单/刷新 | fix-tile-spec-admin-ui 已交付 | 已对齐 | **冻结** 仅回归验收 |
| 类目/品牌 confirm | 已 archive | DS modal | **冻结** 仅回归验收 |

## Goals / Non-Goals

**Goals:**

- `/admin/tile-specs` 启停/删除 confirm 符合 BUG-0037 acceptance AC-001～AC-010。
- modal 结构、取消行为、Vitest 门禁对齐 `TileCategoryManagementPage`。
- 启停/删除 API 调用与 Toast **不回归**。

**Non-Goals:**

- 后端 API、Orval、SQLite 变更。
- 抽取共享 `AdminConfirmDialog`（可选后续）。
- 分页、表单弹窗、列表刷新（BUG-0027/28/29 scope）。
- 修改类目/品牌/用户 confirm。

## Decisions

### D1：页面内联 modal（非新组件）

- 与 `fix-user-reset-password-confirm-ui` / `fix-brand-status-confirm` 一致：inline JSX，复制类目页结构。

### D2：State 机（不变）

- 沿用 `statusConfirmTarget` / `deleteTarget`；仅替换 confirm JSX markup 与按钮 handler 文案。

### D3：文案

| 操作 | 标题 | 正文 | 主按钮 |
|------|------|------|--------|
| 启用 | 启用规格 | 确认启用规格「{display_name}」？ | 确认启用 |
| 停用 | 停用规格 | 确认停用规格「{display_name}」？停用后前台将不再展示该规格。 | 确认停用 |
| 删除 | 删除规格 | 确认删除规格「{display_name}」？此操作不可恢复。 | 删除规格 |

### D4：无障碍

- `role="dialog"`、`aria-modal="true"`、`aria-labelledby` 指向标题 id；正文 `page-desc`；标题区 `modal-close`。

### D5：API / 权限冻结

- 不修改 OpenAPI、权限、Orval。

## 验收 Gate

- **视口**：1440×1024（并排类目停用 confirm，可选 PNG）。
- **Checklist**：见 `trace.md`（≥8 项）。
- **回归**：`TileSpecManagementPage.test.tsx` 既有用例；`TileCategoryManagementPage.test.tsx` / `BrandManagementPage.test.tsx` confirm 用例 MUST pass。
- **来源**：`issues/bugs/archive/BUG-0037-tile-spec-status-confirm-ui-inconsistency/acceptance.md`。

## Risks / Trade-offs

- **[Risk] 复制 markup 遗漏 id 冲突** → 启停/删除 dialog 使用独立 `aria-labelledby` id（如 `status-spec-title`、`delete-spec-title`）。
- **[Risk] 与 fix-tile-spec-admin-ui 合并 touch 冲突** → 本 change 职责独立，仅改 confirm JSX 块。
