---
bug_id: BUG-0039-banner-list-display-position-column
status: pending_review
created_at: 2026-06-28 17:43:07
updated_at: 2026-06-28 17:43:07
related_requirement: REQ-0016-banner-management
---

# 回归验收标准

> 修复本缺陷 MUST 独立展示「展示位置」列，且不得回归 Banner 列表查询、分页、CRUD、上下线与删除规则。与 `banner-management-list.png` 第一列结构的差异由本 BUG acceptance **覆盖**（同 BUG-0030 模式）。

## AC-001 第一列 MUST 仅显示 Banner 标题

**Given** 管理员已登录 Web 管理端  
**When** 访问 `/admin/banners` 且列表有数据  
**Then** 第一列（表头「Banner」或「Banner 标题」）MUST 仅展示缩略图 + Banner 标题  
**And** MUST NOT 在同一单元格内以副标题形式展示展示位置（无 `.banner-sub` 或等价叠放）

## AC-002 MUST 新增独立「展示位置」列

**Given** 管理员在 Banner 列表页  
**When** 观察表头与数据行  
**Then** MUST 存在表头「展示位置」  
**And** 单元格 MUST 展示 `positionLabel(position)` 文案（如「首页顶部轮播」「首页中部运营位」）  
**And** 列顺序 SHOULD 为：Banner → 展示位置 → 展示端 → 跳转类型 → …（展示位置紧邻 Banner 或展示端，以实现为准且须在 trace 记录）

## AC-003 展示位置与展示端 MUST 语义区分

**Given** 列表中存在 Web 首页 + `HOME_TOP_CAROUSEL` 的 Banner  
**When** 查看该行  
**Then** 「展示端」列 MUST 显示「Web 首页」类 badge  
**And** 「展示位置」列 MUST 显示「首页顶部轮播」文案  
**And** 两列 MUST NOT 重复同一信息

## AC-004 空态与加载态 MUST 列数一致

**Given** 列表加载中或筛选结果为空  
**When** 观察表格  
**Then** 占位行 `colSpan` MUST 与表头列数一致（9 列）  
**And** MUST NOT 出现列错位或布局断裂

## AC-005 列表功能 MUST 无回归

**Given** 修复已合并  
**When** 执行筛选、分页、新增、编辑、上线、下线、删除  
**Then** 行为 MUST 与修复前一致  
**And** MUST NOT 变更 API 或请求参数

## AC-006 Design System 约束 MUST 满足

**Given** 修复完成  
**When** 检查 Web UI  
**Then** MUST 使用 semantic token / 既有表格样式  
**And** MUST NOT 新增裸 Hex

## AC-007 测试与记录 MUST 补齐

**Given** 进入 `fix-banner-list-display-position-column`（或合并 fix change）  
**When** 完成 `/opsx-apply`  
**Then** SHOULD 补充 `BannerManagementPage` Vitest（表头含「展示位置」、第一列无 position 副文案）  
**And** MUST 在 Change `trace.md` 记录与 list PNG 第一列 delta 验收结论

## AC-008 REQ-0016 列表原型 delta 对齐

**Given** BUG-0039 修复完成  
**When** 对照 `banner-management-list.html` / PNG  
**Then** 第一列仅标题 + 独立「展示位置」列 MUST 按本 acceptance 通过  
**And** `/bug-opsx` delta spec MUST MODIFIED 记录列表列结构变更
