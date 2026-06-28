---
bug_id: BUG-0030-banner-list-ui-inconsistency
status: pending_review
created_at: 2026-06-28 16:16:51
updated_at: 2026-06-28 16:16:51
related_requirement: REQ-0016-banner-management
---

# 回归验收标准

> 修复本缺陷 MUST 满足管理端列表一致性基准（用户管理页），且不得回归 Banner 列表 CRUD、筛选、上下线与删除规则。REQ-0016 AC-021 左侧 `1-10 / 32` 式范围由本 BUG acceptance **覆盖**（同 BUG-0027 模式）。

## AC-001 Banner 列表 MUST NOT 展示多余 section 标题

**Given** 管理员已登录 Web 管理端  
**When** 访问 `/admin/banners` Banner 管理列表页  
**Then** 表格区域上方 MUST NOT 出现「Banner 列表」section 标题  
**And** MUST NOT 出现「共 N 个 Banner」副标题行（`section-head` 移除）

## AC-002 Banner 列表 MUST NOT 展示 table-toolbar 范围统计行

**Given** 管理员在 Banner 列表页  
**When** 观察表格上方区域  
**Then** MUST NOT 出现「当前显示 X-Y / N」统计行（`table-toolbar` / `table-count` 移除）  
**And** `status=ONLINE` 时删除按钮 MUST 仍通过 `title` 提示「已上线 Banner 需先下线后删除」

## AC-003 Banner 分页 MUST 与用户管理页结构一致

**Given** 管理员已登录 Web 管理端  
**When** 分别访问「Banner 管理」与「用户管理」列表页  
**Then** 两个页面底部分页区域 MUST 使用相同 DOM 结构：`pagination` + `page-summary` + `page-right` + `page-buttons` + `page-size-wrap`  
**And** 布局、按钮尺寸、边框、圆角、字号、激活态和每页显示控件 MUST 视觉一致

## AC-004 Banner 分页 MUST NOT 使用 banner-pagination 结构

**Given** Banner 列表存在分页数据  
**When** 用户查看列表底部分页  
**Then** MUST NOT 出现 `banner-pagination`、`banner-page-left`、`table-toolbar` 类名/结构  
**And** 当前页 MUST 以 `.page-btn.active` 高亮按钮展示，而非连续 1–5 页码条  
**And** 每页条数下拉 MUST 含「每页显示」标签，选项格式为「10 条 / 20 条 / 50 条」  
**And** 左侧摘要 MUST 为「共 N 个 Banner」（或 loading 时「…」），而非「X-Y / N」范围

## AC-005 分页功能 MUST 保持可用

**Given** Banner 列表有多页数据  
**When** 用户切换页码或修改每页条数（10 / 20 / 50）  
**Then** 列表 MUST 正确刷新，total 与当前筛选结果一致  
**And** 切换每页条数后 page=1，keyword / display_client / status / time_status 筛选 MUST 保留

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

**Given** 进入 `fix-banner-admin-ui`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** SHOULD 补充 `BannerManagementPage` 相关 Vitest（分页 DOM 结构、无 section-head / banner-pagination）  
**And** MUST 在 Change `trace.md` 记录与用户管理页分页并排验收结论

## AC-009 REQ-0016 AC-021 delta 对齐

**Given** BUG-0030 修复完成  
**When** 对照 REQ-0016 `acceptance.md` AC-021  
**Then** 分页左侧 MUST 采用「共 N 个 Banner」摘要 + 右侧页码与每页条数（覆盖原 AC-021 左侧 `1-10 / 32` 式范围要求）  
**And** `/bug-opsx` delta spec MUST 以 MODIFIED 记录该变更
