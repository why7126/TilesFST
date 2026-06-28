---
bug_id: BUG-0027-tile-spec-list-ui-inconsistency
title: 瓷砖规格列表分页与尺寸名称列字号与用户管理页不一致
severity: medium
status: draft
owner: product
discovered_at: 2026-06-28 13:13:16
environment: local|docker
related_requirement: REQ-0009-tile-spec-management
related_change: null
---

# 缺陷说明

Web 管理端「瓷砖规格」列表页（`/admin/tile-specs`）存在两处 UI 一致性问题：

1. **分页交互与样式**：底部分页控件未复用用户管理页 / 品牌管理页已验收的分页 DOM 与样式，使用项目内唯一的 `pagination-bar` / `page-indicator` 结构，缺少标准 `.pagination` 容器、当前页高亮按钮、「每页显示 N 条」文案等，视觉与交互与用户管理页不一致。
2. **表格主列字号**：「尺寸名称」列通过 `.size-name` 设为 13px + 高对比文字色，而同表其他数据列为 12px + 次要色，在无 avatar 的主列场景下视觉权重明显偏高，与管理端列表统一观感不符。

# 复现步骤

1. 以 admin 用户登录 Web 管理端（local `5173` 或 Docker `3000` 均可）。
2. 进入「瓷砖规格」列表页（侧栏 OPERATIONS → 瓷砖规格，或 `/admin/tile-specs`）。
3. 观察列表底部分页区域：总数摘要、页码展示形式、每页条数下拉样式与文案。
4. 打开「用户管理」列表页，并排对比底部分页控件的高度、背景、边框、按钮激活态与「每页显示」层级。
5. 观察规格列表「尺寸名称」列（如 `600x1200mm`）与同表宽度/长度/厚度等列的字号与字色对比。
6. 可选：对照 `issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management.html` 与截图 `screenshots/tile-spec-list-pagination-font-inconsistency.png`。

# 期望结果

- 列表底部分页应与用户管理页（及 BUG-0002 修复后的品牌管理页、BUG-0009 修复后的 SKU 列表页）保持一致：
  - 使用 `pagination` + `page-summary` + `page-right` + `page-buttons` + `page-size-wrap` 结构。
  - 当前页以 `.page-btn.active` 高亮展示，而非 `1 / N` 文本指示器。
  - 每页条数下拉含「每页显示」标签，选项格式为「20 条 / 50 条 / 100 条」。
  - 统一分页栏高度、顶部分割线、背景与按钮尺寸（见 `user-management.css`）。
- 表格「尺寸名称」列字号、字色与同表其他列及用户管理列表主列视觉层级协调，符合 REQ-0009 AC-042 管理端列表模式复用要求。

# 实际结果

- `TileSpecManagementPage.tsx` 使用 `pagination-bar` / `pagination-left` / `pagination-right` / `page-indicator` 类名，上述类名在 `user-management.css` 中无定义，分页区域未接入已验收的标准分页样式。
- 页码以 `{page} / {totalPages}` 文本展示，缺少金色激活页码按钮；每页条数下拉为裸数字选项，无「每页显示」文案。
- `tile-spec-management.css` 中 `.size-name` 为 13px + `--admin-text`，而同表 `td` 默认为 12px + `--admin-muted`，尺寸名称列视觉明显偏大。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / 瓷砖规格列表 | 分页样式与用户管理页不一致 |
| Web 管理端 / 规格列表表格 | 尺寸名称列字号与同表其他列不协调 |
| Design System 验收 | REQ-0009 AC-024、AC-042 列表模式复用未达标 |
| 关联需求 | REQ-0009-tile-spec-management（`add-tile-spec-management` 实现范围） |

不影响 API、数据库、权限边界或小程序/店主端。

# 严重等级说明

严重程度为 `medium`。

理由：

- 不阻断规格列表的查询、分页、新增、编辑、启停、删除等核心功能。
- 分页逻辑（翻页、修改 pageSize）仍可用，主要为视觉与交互一致性问题。
- 但属于可见管理端 UI 缺陷，影响 REQ-0009 验收及与 BUG-0009 同类问题的 Design System 一致性；同类根因已在 SKU 列表修复，规格页应同样对齐。

# 代码线索

| 线索 | 路径 |
|---|---|
| 规格列表页（分页 + 尺寸名称列） | `src/web/src/pages/admin/TileSpecManagementPage.tsx` |
| 用户管理分页参考 | `src/web/src/pages/admin/UserManagementPage.tsx` |
| 品牌管理分页参考 | `src/web/src/pages/admin/BrandManagementPage.tsx` |
| 通用分页样式 | `src/web/src/features/admin/styles/user-management.css` |
| 规格页补充样式（`.size-name`） | `src/web/src/features/admin/styles/tile-spec-management.css` |
| 列表原型 | `issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management.html` |
| 同类已修复 BUG | `issues/bugs/archive/BUG-0009-tile-sku-list-ui-inconsistency/` |
| UI 规范 | `rules/ui-design.md` |
