---
bug_id: BUG-0009-tile-sku-list-ui-inconsistency
title: SKU列表分页与用户管理页不一致且表头上方多余标题行
severity: medium
status: draft
owner: product
discovered_at: 2026-06-27 08:56:54
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_change: null
---

# 缺陷说明

瓷砖 SKU 列表页存在两处 UI 一致性问题：

1. 列表底部分页控件与用户管理页分页样式、布局不一致，与整体 Design System 及管理端既有列表页规范不符。
2. 列表表格表头上方存在多余的标题行（`table-head` / `table-title`「SKU 列表」），与 REQ-0006 原型及用户管理页等管理端列表结构不一致——页面级 `page-hero` 标题区已存在，表格卡片内不应再重复标题行。

# 复现步骤

1. 以 admin 用户登录 Web 管理端（local 或 Docker 均可）。
2. 进入「瓷砖 SKU」列表页（`/admin/tile-skus`），观察列表底部分页区域（总数、页码、每页条数等）。
3. 打开「用户管理」列表页，对比底部分页控件的尺寸、边框、圆角、文字、激活态与布局。
4. 观察 SKU 列表表格区域：确认表头上方是否出现额外标题行（「SKU 列表」及「默认按更新时间倒序」），并与用户管理页 `table-card` 内直接呈现表头的结构对比。
5. 对照 `issues/requirements/REQ-0006-tile-sku-management/prototype/web/tile-sku-management-list.html` 与 `prototype/images/tile-sku-management-list.png`（如有）。

# 期望结果

- SKU 列表底部分页应与用户管理页分页保持一致的结构和视觉语言：
  - 使用 `page-summary` + `page-right` + `page-buttons` + `page-size-wrap` 布局，而非 `page-left` + `brand-pagination-right`。
  - 统一高度、内边距、边框、字号、按钮尺寸和激活态。
  - 统一「总数摘要 + 翻页按钮 + 每页显示」层级与文案格式。
- 表格卡片内直接呈现筛选/表格/分页，表头上方**无**重复标题行，与 REQ-0006 列表原型及 Design System 管理端列表模板（`UserManagementPage`）一致。

# 实际结果

- SKU 列表分页使用 `page-left`（含总数与翻页按钮混排）+ `brand-pagination-right`，与用户管理页的 `page-summary` + `page-right` 结构不一致；该模式与 BUG-0002 修复前的品牌管理页相同，未对齐已验收的用户管理分页实现。
- 表格卡片内存在 `table-head` 区块，含 `table-title`「SKU 列表」与 `table-note`，在已有 `page-hero` 页面标题下形成重复层级，破坏页面信息架构与整体设计方案一致性。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / 瓷砖 SKU 列表 | 分页样式与用户管理页不一致 |
| Web 管理端 / SKU 列表表格卡片 | 表头上方多余标题行，与原型及既有列表页结构不符 |
| Design System 验收 | 管理端列表页组件复用与视觉一致性不达标 |
| 关联需求 | REQ-0006-tile-sku-management（`add-tile-sku-management` 实现范围） |

# 严重等级说明

严重程度为 `medium`。

理由：

- 不阻断 SKU 列表的查询、分页、新增、编辑等核心功能。
- 不影响 API、数据库或权限边界。
- 但属于可见管理端 UI 缺陷，影响视觉一致性、REQ-0006 原型验收及长期组件复用；同类问题已在 BUG-0002（品牌管理分页）中修复，SKU 页应同样对齐。

# 代码线索

| 线索 | 路径 |
|---|---|
| SKU 列表页（分页 + 表格标题行） | `src/web/src/pages/admin/TileSkuManagementPage.tsx` |
| 用户管理分页参考 | `src/web/src/pages/admin/UserManagementPage.tsx` |
| 通用分页样式 | `src/web/src/features/admin/styles/user-management.css` |
| SKU 页补充样式 | `src/web/src/features/admin/styles/tile-sku-management.css` |
| 列表原型 | `issues/requirements/REQ-0006-tile-sku-management/prototype/web/tile-sku-management-list.html` |
| UI 规范 | `rules/ui-design.md` |
