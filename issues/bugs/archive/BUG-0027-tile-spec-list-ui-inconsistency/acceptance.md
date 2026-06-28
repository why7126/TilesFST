---
bug_id: BUG-0027-tile-spec-list-ui-inconsistency
status: pending_review
created_at: 2026-06-28 13:20:08
updated_at: 2026-06-28 13:20:08
related_requirement: REQ-0009-tile-spec-management
---

# 回归验收标准

> 修复本缺陷 MUST 满足 REQ-0009 **AC-024**（分页语义）、**AC-042**（分页模式复用）、**AC-045**（列表原型并排），且不得回归规格列表 CRUD、启停与筛选功能。

## AC-001 规格列表分页 MUST 与用户管理页结构一致

**Given** 管理员已登录 Web 管理端  
**When** 分别访问「瓷砖规格」与「用户管理」列表页  
**Then** 两个页面底部分页区域 MUST 使用相同 DOM 结构：`pagination` + `page-summary` + `page-right` + `page-buttons` + `page-size-wrap`  
**And** 布局、按钮尺寸、边框、圆角、字号、激活态和每页显示控件 MUST 视觉一致

## AC-002 规格分页 MUST NOT 使用非标准 pagination-bar 结构

**Given** 规格列表存在分页数据  
**When** 用户查看列表底部分页  
**Then** MUST NOT 出现 `pagination-bar`、`pagination-left`、`page-indicator` 类名/结构  
**And** 当前页 MUST 以 `.page-btn.active` 高亮按钮展示，而非 `{page} / {totalPages}` 文本  
**And** 每页条数下拉 MUST 含「每页显示」标签，选项格式为「20 条 / 50 条 / 100 条」

## AC-003 尺寸名称列字号 MUST 与同表其他列协调

**Given** 规格列表存在至少一条数据  
**When** 观察「尺寸名称」列与宽度/长度/厚度等相邻列  
**Then** 尺寸名称列 MUST NOT 明显大于同表标准数据列（12px 体系）  
**And** 视觉层级 MUST 与用户管理列表主列（`.user-main`）或同表数值列保持一致，不得单独放大破坏表格 rhythm

## AC-004 分页功能 MUST 保持可用

**Given** 规格列表有多页数据  
**When** 用户切换页码或修改每页条数（20 / 50 / 100）  
**Then** 列表 MUST 正确刷新，total 与当前筛选结果一致（REQ-0009 AC-024）  
**And** 切换每页条数后 page=1，keyword / status 筛选 MUST 保留

## AC-005 修复 MUST 对齐 REQ-0009 列表原型分页语义

**Given** 修复完成  
**When** 与 `prototype/web/tile-size-management.html` 并排对比（1440×1024）  
**Then** 分页左侧「共 N 条」、右侧页码与每页条数布局 MUST 与原型语义一致  
**And** 实现 DOM MUST 同时满足 AC-001 管理端标准分页模式（原型 HTML 局部类名不得 override 已验收模式）

## AC-006 修复范围 MUST 为纯前端 UI

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API 路径、请求/响应结构、SQLite schema  
**And** MUST NOT 引入新的后端逻辑

## AC-007 Design System 约束 MUST 满足

**Given** 修复完成  
**When** 检查 Web UI 修改  
**Then** MUST 复用 `user-management.css` 既有分页类名与 semantic Token  
**And** MUST NOT 新增裸 Hex 或与 `rules/ui-design.md` 冲突的局部样式

## AC-008 测试与记录 MUST 补齐

**Given** 进入 `fix-tile-spec-list-ui-inconsistency`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** SHOULD 补充 `TileSpecManagementPage` 相关 Vitest（分页 DOM 结构、无 pagination-bar）  
**And** MUST 在 Change `trace.md` 记录与用户管理页分页并排验收结论

## AC-009 REQ-0009 AC-042 对齐确认

**Given** BUG-0027 修复完成  
**When** 对照 `issues/requirements/archive/REQ-0009-tile-spec-management/acceptance.md` AC-042  
**Then** 「复用 AdminLayout、品牌页启停确认与**分页模式**」MUST 全部满足
