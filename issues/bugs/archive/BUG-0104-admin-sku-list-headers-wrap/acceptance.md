---
bug_id: BUG-0104-admin-sku-list-headers-wrap
title: 管理后台 SKU 列表表头字段换行验收标准
acceptance_status: passed
created_at: 2026-08-03 08:22:05
updated_at: 2026-08-03 20:52:16
---

# 验收标准

## 回归验收项

- [x] AC-001：在管理后台进入 SKU 列表页面后，所有表头字段在常用桌面宽度下均保持单行显示。
- [x] AC-002：表头字段与正文列内容保持对齐，不出现表头和数据列错位。
- [x] AC-003：当列数较多或窗口宽度不足时，表格可通过既有横向滚动或布局策略完整查看全部列。
- [x] AC-004：修复后排序、筛选、分页和操作列仍可正常使用。
- [x] AC-005：修复不得通过过度压缩列宽造成正文内容重叠、按钮不可点击或操作列不可见。

## 复现与验证入口

1. 登录管理后台。
2. 进入 SKU 列表页面。
3. 使用常用桌面宽度查看所有表头字段。
4. 调整窗口宽度，确认表头保持单行且表格布局可用。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-03 20:52:16
accepted_by: workflow-sync
source_change: fix-admin-sku-list-header-wrapping
source_sprint: sprint-018
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

