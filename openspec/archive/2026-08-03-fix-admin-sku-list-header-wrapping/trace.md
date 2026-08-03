---
change_id: fix-admin-sku-list-header-wrapping
type: fix
status: applied
created_at: 2026-08-03 08:32:48
updated_at: 2026-08-03 09:02:03
related_bug: BUG-0104-admin-sku-list-headers-wrap
related_requirement: REQ-0006-tile-sku-management
iteration: sprint-018
---

# Change Trace

```yaml
change_id: fix-admin-sku-list-header-wrapping
type: fix
status: applied
related_bug: BUG-0104-admin-sku-list-headers-wrap
related_requirement: REQ-0006-tile-sku-management
iteration: sprint-018
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-03 09:02:03 | `/opsx-apply BUG-0104` | 修复 SKU 列表表头换行，补充单行表头、最小表格宽度、横向滚动和前端回归测试；无需 API/DB/Orval/Docker 变更。 |
| 2026-08-03 08:39:44 | `/sprint-propose sprint-018` | 纳入 sprint-018 正式范围。 |
| 2026-08-03 08:32:48 | `/bug-opsx BUG-0104` | 基于已评审 BUG 创建 OpenSpec 修复 Change。 |
