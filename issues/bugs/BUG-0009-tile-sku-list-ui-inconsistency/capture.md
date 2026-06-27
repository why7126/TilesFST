---
bug_id: BUG-0009-tile-sku-list-ui-inconsistency
status: captured
recorded_at: 2026-06-27 08:56:54
severity_hint: medium
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_change: null
---

# 现象

瓷砖 SKU 列表页存在两处 UI 一致性问题：

1. 列表底部分页控件与用户管理页分页样式、布局不一致，与整体 Design System 及管理端既有列表页规范不符。
2. 列表表格表头上方存在多余的标题行，与 REQ-0006 原型及用户管理页等管理端列表结构不一致（页面级标题区已存在，表格卡片内不应再重复标题行）。

# 复现步骤

1. 以 admin 登录管理端。
2. 进入「瓷砖SKU」列表页，观察列表底部分页区域（总数、页码、每页条数等）。
3. 打开「用户管理」列表页，对比底部分页控件的尺寸、边框、圆角、文字、激活态与布局。
4. 观察 SKU 列表表格区域：确认表头上方是否出现额外标题行（如「SKU 列表」等），并与用户管理页表格卡片结构对比。
5. 对照 `issues/requirements/REQ-0006-tile-sku-management/prototype/web/tile-sku-management-list.html` 与 `prototype/images/tile-sku-management-list.png`（如有）。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | SKU 列表底部分页应与用户管理页分页组件样式与交互一致；表格卡片内直接呈现筛选/表格/分页，表头上方无重复标题行，与原型及 Design System 管理端列表模板一致。 |
| **实际** | 分页视觉与用户管理页不一致；表头上方存在不应出现的标题行，破坏页面层级与整体设计方案一致性。 |

# 影响范围

- Web 管理端：瓷砖 SKU 列表页。
- 关联需求：REQ-0006-tile-sku-management（`add-tile-sku-management` 实现中）。
- 参考页面：用户管理页、品牌管理页（BUG-0002 已修复分页参考）。

# 初步分类（待 /bug-generate 确认）

| 判断 | 结论 |
|---|---|
| 缺陷类型 | UI 视觉/布局一致性缺陷 |
| 严重程度建议 | medium |
| 可能修复面 | SKU 列表页分页组件复用、表格卡片内标题行移除 |
| 设计约束 | 对齐 `rules/ui-design.md`、`UserManagementPage` 分页实现、REQ-0006 列表原型 |

# 附件

- 暂无截图。
- 参考原型：`issues/requirements/REQ-0006-tile-sku-management/prototype/web/tile-sku-management-list.html`
- 参考规范：`rules/ui-design.md` 分页器、Design System 管理端列表模板
