---
bug_id: BUG-0030-banner-list-ui-inconsistency
title: Banner列表分页与用户管理页不一致且表头上方多余标题行
severity: medium
status: draft
owner: product
discovered_at: 2026-06-28 16:04:18
environment: local|docker
related_requirement: REQ-0016-banner-management
related_change: null
---

# 缺陷说明

Web 管理端「Banner 管理」列表页（`/admin/banners`）存在三处 UI 一致性问题，未对齐管理端列表黄金参考页「用户管理」：

1. **多余区块标题**：表格上方存在 `section-head` 区块，含「Banner 列表」标题及「共 N 个 Banner」副文案；用户管理页直接在 `table-card` 内展示表格，无此类 section 标题。
2. **多余统计行**：`table-toolbar` 内展示「当前显示 X-Y / N」范围文案；用户管理页无 `table-toolbar`，总数摘要仅在底部分页栏左侧以「共 N 条」形式出现。
3. **分页 DOM 不一致**：使用自定义 `banner-pagination` + `banner-page-left`（左侧每页条数 + 范围 + 右侧多页码按钮），而非用户管理页已验收的 `.pagination` + `page-summary` + `page-right` + `page-buttons`（单页码激活）+ `page-size-wrap`（「每页显示」）结构。

根因类型为 **design / frontend-ui**：`add-banner-management` 实现时按 REQ-0016 原型 HTML port 了 section-head、table-toolbar 与原型分页布局，未复用 `admin-list-page-consistency.md` 规定的用户管理页基准模式（同类问题见 BUG-0009、BUG-0027）。

# 复现步骤

1. 以 admin 或 employee 登录 Web 管理端（local `5173` 或 Docker `3000`）。
2. 进入「Banner 管理」列表页（侧栏 OPERATIONS → Banner 管理，或 `/admin/banners`）。
3. 观察表格上方是否存在「Banner 列表」标题及「当前显示 … / …」行。
4. 观察底部分页区域：左侧每页条数 + 范围文案、右侧多页码按钮布局。
5. 打开「用户管理」列表页（`/admin/users`），并排对比表格上方结构及底部分页 DOM/样式。
6. 可选：对照截图 `screenshots/banner-list-ui-inconsistency.png` 与 `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-list.html`。

# 期望结果

- 表格区域 **无**「Banner 列表」section 标题及「共 N 个 Banner」副标题行。
- 表格上方 **无**「当前显示 X-Y / N」统计行（`table-toolbar` / `table-count` 移除或精简；「已上线 Banner 需先下线后删除」提示 MAY 保留于删除按钮 `title` tooltip，与用户管理页 disabled 操作提示模式一致）。
- 底部分页与用户管理页一致：
  - 使用 `pagination` + `page-summary`（「共 N 个 Banner」）+ `page-right` + `page-buttons` + `page-size-wrap` 结构。
  - 当前页以 `.page-btn.active` 高亮展示（非连续 1–5 页码条）。
  - 每页条数下拉含「每页显示」标签，选项格式为「10 条 / 20 条 / 50 条」。
  - 样式复用 `user-management.css` 中已定义的分页规则（`BannerManagementPage` 已 import 该 CSS）。

# 实际结果

- `BannerManagementPage.tsx` 在 `table-card` 外包裹 `section-head`（「Banner 列表」+「共 N 个 Banner」）。
- `table-toolbar` 展示「当前显示 {rangeStart}-{rangeEnd} / {total}」及删除规则提示。
- 分页使用 `banner-pagination` / `banner-page-left` / `banner-page-size`，与用户管理页 `.pagination` 结构不同；`banner-management.css` 单独定义 `.banner-pagination` 样式。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / Banner 列表 | 分页样式、表格上方信息层级与用户管理页不一致 |
| Design System / 列表一致性 | 违反 `admin-list-page-consistency.md` 基准页要求 |
| 关联需求 | REQ-0016-banner-management（`add-banner-management` 列表页实现） |
| 原型/验收冲突 | REQ-0016 AC-021 要求左侧 `1-10 / 32` 式范围；修复时 BUG acceptance 优先于原型（同 BUG-0027 模式），需在 `/bug-complete` 或 `/bug-opsx` 中 MODIFIED delta spec |

不影响 API、数据库、权限边界、Banner 业务逻辑或小程序/店主端。

# 严重等级说明

严重程度为 `medium`。

理由：

- 不阻断 Banner 列表的查询、分页、新增、编辑、上下线、删除等核心功能。
- 分页逻辑（翻页、修改 pageSize）仍可用，主要为视觉与 DOM 结构一致性问题。
- 属于可见管理端 UI 缺陷，影响 REQ-0016 验收及与 BUG-0009、BUG-0027 同类问题的 Design System 一致性；应在 `fix-banner-admin-ui` 或等价 fix change 中与其他 Banner 弹窗 BUG（0031–0036）一并修复。

# 代码线索

| 线索 | 路径 |
|---|---|
| Banner 列表页（section-head / toolbar / 分页） | `src/web/src/pages/admin/BannerManagementPage.tsx` |
| 用户管理分页参考 | `src/web/src/pages/admin/UserManagementPage.tsx` |
| 通用分页样式 | `src/web/src/features/admin/styles/user-management.css` |
| Banner 分页补充样式 | `src/web/src/features/admin/styles/banner-management.css` |
| 列表原型 | `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-list.html` |
| 列表一致性最佳实践 | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` |
| 同类已修复 BUG | `issues/bugs/archive/BUG-0027-tile-spec-list-ui-inconsistency/` |
| 父 Change | `openspec/changes/add-banner-management` |
