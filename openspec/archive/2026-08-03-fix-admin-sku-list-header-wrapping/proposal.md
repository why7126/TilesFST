---
change_id: fix-admin-sku-list-header-wrapping
type: fix
status: proposed
created_at: 2026-08-03 08:32:48
updated_at: 2026-08-03 08:32:48
related_bug: BUG-0104-admin-sku-list-headers-wrap
related_requirement: REQ-0006-tile-sku-management
capability: tile-sku-management
---

# 修复管理后台 SKU 列表表头字段换行

## Why

BUG-0104 记录管理后台 SKU 列表部分表头字段在常用桌面宽度下发生换行，破坏表格扫描体验并影响表头与正文列的对应判断。该问题不阻断 SKU 数据维护，但属于既有管理端列表展示缺陷，已评审通过并确认需要修复。

## What

- 约束管理后台 SKU 列表表头字段单行显示。
- 明确表头、列宽与横向滚动容器的布局契约。
- 保持排序、筛选、分页、操作列和正文列可读性不回归。
- 补充前端回归测试或等价验收，覆盖表头单行与关键交互不受影响。

## Out Of Scope

- 不新增或修改后端 API。
- 不调整数据库结构。
- 不修改 SKU 排序、筛选、分页或鉴权业务逻辑。
- 不重构 SKU 列表整体信息架构。

## Rollback Plan

若修复导致列表内容重叠、横向滚动失效或操作列不可用，回滚本 Change 中的 SKU 列表样式/组件调整与对应测试，恢复现有列表渲染；由于不涉及 API、数据库或数据迁移，回滚不需要数据修复。
