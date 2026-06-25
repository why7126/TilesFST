## Context

- **现状**：`TileCategoryManagementPage.tsx` 启停直接 `handleToggleStatus` → API；检索/列表有 `section-head`；分页用 `cat-pager` +「当前显示 x-y / N 条」。
- **父 change**：`add-tile-category-management`（archived）；`fix-tile-category-enable-action`（archived，启停按钮可见性已修复）。
- **原型来源**（优先级）：
  1. `issues/requirements/REQ-0007-tile-category-management-refine/prototype/web/tile-category-management-list-refine-context.md`
  2. `issues/requirements/REQ-0007-tile-category-management-refine/prototype/web/tile-category-status-confirm-context.md`
  3. `issues/requirements/REQ-0007-tile-category-management-refine/acceptance.md`
  4. `issues/requirements/REQ-0005-tile-category-management/prototype/web/tile-category-management.html`（v1 基线，按 context diff）
  5. `issues/requirements/REQ-0005-user-management-list-refine` 分页区（并排参考）
  6. `openspec/specs/web-client/spec.md`「管理端瓷砖类目管理页」（基线）

## Conflict Resolution

| 检查项 | v2 context | v1 HTML/实现 | add spec / acceptance | 决议 |
|--------|------------|--------------|----------------------|------|
| 启停点击 | 二次确认后 API | 直接 API | AC-015 直接启停 | **MODIFIED** 以 REQ-0007 为准 |
| 检索 section-head | 无 | 有「类目检索」 | v1 HTML 有 | **MODIFIED** 删除外层标题 |
| 列表 section-head | 无 | 有「类目列表」 | v1 HTML 有 | **MODIFIED** 删除外层标题 |
| cat-table-toolbar | 保留 | 保留 | AC-012 工具栏 | **冻结** |
| 分页左侧 | 「共 N 个类目」 | 「当前显示 x-y / N 条」 | AC-020 v1 文案 | **MODIFIED** 对齐用户管理 v2 |
| 分页 select | 「10 条」 | 「10 条/页」 | — | **MODIFIED** |
| 删除/弹窗/树/API | 不变 | 不变 | REQ-0005 | **冻结** |
| BUG-0001 启停按钮 | 停用行必有「启用」 | 已修复 | — | **冻结**，回归 AC-024 |

## Goals / Non-Goals

**Goals:**

- `/admin/tile-categories` 符合 REQ-0007 acceptance 与 v2 context（1280×1024 并排）。
- 启停确认弹窗复用删除 modal 样式类。
- 分页 DOM/文案与 `UserManagementPage` v2 一致。
- BUG-0001、删除规则、CategoryFormModal 零回归。

**Non-Goals:**

- 后端 API、Orval、SQLite 变更。
- 新增/编辑弹窗、指标卡、类目树、筛选逻辑变更。
- 移除「查询」按钮或改为自动搜索（非本期）。
- v2 完整 HTML 文件强制提交（context diff 足够 gate）。

## Decisions

### D1：CSS Port 增量（延续 add-tile-category-management）

- 在 `tile-category-management.css` 上调整间距（去 section-head 后）；分页复用 `user-management.css` 的 `.pagination` / `.page-summary` / `.page-right` 或 port 等价规则。

### D2：启停确认状态机

- 新增 `statusConfirmTarget: TileCategoryAdminItem | null` + `statusConfirmAction: 'enable' | 'disable' | null`（或等价）。
- 行内按钮 → 打开确认弹窗；footer 主按钮 → 调用现有 `enableCategory` / `disableCategory` → Toast + `refreshAll()`。

### D3：分页结构对齐

- 替换 `cat-pager` 为与 `UserManagementPage` 相同的 JSX 结构；summary 文案「共 {total} 个类目」。

### D4：API / 弹窗冻结

- 不修改 OpenAPI、Orval、CategoryFormModal、删除确认逻辑。

## 验收 Gate

- **视口**：1280×1024。
- **Golden Reference**：`tile-category-management-list-refine.png`（待导出，非阻塞）。
- **Checklist**：见 `trace.md`（≥12 项）。
- **回归**：`TileCategoryManagementPage.test.tsx`（BUG-0001 用例）+ 本 change 新增用例。
