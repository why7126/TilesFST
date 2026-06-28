---
bug_id: BUG-0009-tile-sku-list-ui-inconsistency
status: pending_review
created_at: 2026-06-27 10:18:43
updated_at: 2026-06-27 10:18:43
related_requirement: REQ-0006-tile-sku-management
---

# 回归验收标准

> 修复本缺陷 MUST 满足 REQ-0006 **AC-019～AC-021**（分页语义）、**AC-051**（分页与表格模式复用）、**AC-054**（列表原型并排），且不得回归 SKU 列表 CRUD 与筛选功能。

## AC-001 SKU 列表分页 MUST 与用户管理页结构一致

**Given** 管理员已登录 Web 管理端  
**When** 分别访问「瓷砖 SKU」与「用户管理」列表页  
**Then** 两个页面底部分页区域 MUST 使用相同 DOM 结构：`page-summary` + `page-right` + `page-buttons` + `page-size-wrap`  
**And** 布局、按钮尺寸、边框、圆角、字号、激活态和每页显示控件 MUST 视觉一致

## AC-002 SKU 分页 MUST NOT 使用废弃的 brand 局部结构

**Given** SKU 列表存在分页数据  
**When** 用户查看列表底部分页  
**Then** MUST NOT 出现 `page-left` 或 `brand-pagination-right` 类名/结构  
**And** 总数摘要 MUST 独立于翻页按钮组（`page-summary`），不得与按钮混排在同一 flex 组

## AC-003 表格卡片内 MUST NOT 有重复标题行

**Given** 管理员访问 SKU 列表页  
**When** 查看 `table-card` 区域  
**Then** MUST NOT 渲染 `table-head`、`table-title`「SKU 列表」或等价卡片内二级标题  
**And** 页面级 `page-hero` 已提供「瓷砖 SKU」标题，表格 MUST 直接以 `<table>` 表头开始（与用户管理页一致）

## AC-004 分页功能 MUST 保持可用

**Given** SKU 列表有多页数据  
**When** 用户切换页码或修改每页条数（10 / 20 / 50 / 100）  
**Then** 列表 MUST 正确刷新，total 与当前筛选结果一致（REQ-0006 AC-019～AC-021）  
**And** 切换每页条数后 page=1，筛选条件 MUST 保留

## AC-005 修复 MUST 对齐 REQ-0006 列表原型

**Given** 修复完成  
**When** 与 `prototype/web/tile-sku-management-list.html` 并排对比（1440×1024）  
**Then** 分页左侧「共 N 条」、右侧页码与每页条数布局 MUST 与原型一致  
**And** 表格区域 MUST 无原型未定义的卡片内标题行

## AC-006 修复范围 MUST 为纯前端 UI

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API 路径、请求/响应结构、SQLite schema  
**And** MUST NOT 引入新的后端逻辑

## AC-007 Design System 约束 MUST 满足

**Given** 修复完成  
**When** 检查 Web UI 修改  
**Then** MUST 复用 `user-management.css` 既有分页类名与语义 Token  
**And** MUST NOT 新增裸 Hex 或与 `rules/ui-design.md` 冲突的局部样式

## AC-008 测试与记录 MUST 补齐

**Given** 进入 `fix-tile-sku-list-ui-inconsistency`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** SHOULD 补充 `TileSkuManagementPage` 相关 Vitest（分页 DOM 结构、无 table-head）  
**And** MUST 在 Change `trace.md` 记录与用户管理页分页并排验收结论

## AC-009 REQ-0006 AC-051 对齐确认

**Given** BUG-0009 修复完成  
**When** 对照 `issues/requirements/archive/REQ-0006-tile-sku-management/acceptance.md` AC-051  
**Then** 「复用 AdminLayout、AdminSidebar、**分页与表格模式**」MUST 全部满足
