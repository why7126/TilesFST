## Context

- **现状**：`BrandManagementPage.tsx` 中 `handleToggleStatus` 直接调用 `enableBrand` / `disableBrand`；删除使用 `deleteTarget` + 独立确认弹窗。
- **父需求**：REQ-0005-brand-management；子需求 REQ-0008-brand-status-confirm（approved，sprint-002）。
- **原型来源**（优先级）：
  1. `issues/requirements/REQ-0008-brand-status-confirm/prototype/web/brand-status-confirm-context.md`
  2. `issues/requirements/REQ-0008-brand-status-confirm/acceptance.md`
  3. `issues/requirements/REQ-0005-brand-management/prototype/web/brand-management.html`（v1 基线，启停仍为直接 API）
  4. `issues/requirements/REQ-0007-tile-category-management-refine/prototype/web/tile-category-status-confirm-context.md`（交互参考）
  5. 已实现 `BrandManagementPage` 删除确认弹窗（modal 结构参考）
  6. `openspec/specs/web-client/spec.md`（基线 fix 能力）

## Conflict Resolution

| 检查项 | REQ-0008 context | v1 HTML / 当前实现 | REQ-0005 acceptance | 决议 |
|--------|------------------|-------------------|---------------------|------|
| 启停点击 | 二次确认后 API | 直接 API | 直接启停 | **ADDED** 以 REQ-0008 为准 |
| 停用正文 | 含「停用后前台将不再展示该品牌。」 | 无弹窗 | — | **ADDED** |
| 启用正文 | 仅确认意图 | 无弹窗 | — | **ADDED** |
| 删除确认 | 独立弹窗 | 独立弹窗 | 删除规则不变 | **冻结** |
| 弹窗/筛选/分页/API | 不变 | 不变 | REQ-0005 | **冻结** |

## Goals / Non-Goals

**Goals:**

- `/admin/brands` 符合 REQ-0008 acceptance（AC-001～AC-023）。
- 启停确认弹窗复用删除 modal 样式类（`modal-backdrop`、`modal-card` 等）。
- 删除确认、BrandFormModal、分页、筛选零回归。

**Non-Goals:**

- 后端 API、Orval、SQLite 变更。
- 新增/编辑弹窗、指标卡、删除规则变更。
- 批量启停、导出。
- PNG Golden Reference 强制提交（context gate 先行）。

## Decisions

### D1：CSS Port 增量（延续 brand-management）

- 不新增页面级 CSS；复用删除确认弹窗已有 `modal-*` class，必要时在 `brand-management.css` 做零增量或沿用全局 modal 样式。

### D2：启停确认状态机

- 新增 `statusConfirmTarget: BrandAdminItem | null` + `statusConfirmAction: 'enable' | 'disable' | null`（或等价）。
- 行内「启用/停用」→ 设置 target + action → 打开确认弹窗。
- footer 主按钮 → 调用现有 `enableBrand` / `disableBrand` → Toast + `loadBrands()`。
- **MUST NOT** 与 `deleteTarget` 共用同一 state。

### D3：无障碍

- 弹窗 `role="dialog"`、`aria-modal="true"`、`aria-labelledby` 指向标题 id（对齐删除弹窗）。

### D4：API / 弹窗冻结

- 不修改 OpenAPI、Orval、BrandFormModal、删除确认逻辑。

## 验收 Gate

- **视口**：1280×1024。
- **Golden Reference**：启停确认 PNG 可选待导出（非阻塞）。
- **Checklist**：见 `trace.md`（≥8 项）。
- **回归**：`BrandManagementPage.test.tsx` + 本 change 新增用例。
