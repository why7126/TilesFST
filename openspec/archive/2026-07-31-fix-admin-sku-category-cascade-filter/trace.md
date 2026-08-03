---
change_id: fix-admin-sku-category-cascade-filter
type: fix
status: proposed
source_bug: BUG-0096-admin-sku-category-filter-only-top-level
related_requirement: REQ-0006-tile-sku-management
created_at: 2026-07-31 15:17:04
updated_at: 2026-07-31 21:25:00
iteration: sprint-015
---

# Trace

```yaml
change_id: fix-admin-sku-category-cascade-filter
type: fix
status: proposed
source_bug: BUG-0096-admin-sku-category-filter-only-top-level
related_requirement: REQ-0006-tile-sku-management
iteration: sprint-015
```

## 来源

- BUG：`BUG-0096-admin-sku-category-filter-only-top-level`
- 父需求：`REQ-0006-tile-sku-management`
- 能力：`tile-sku-management`

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 21:25:00 | `/opsx-modify BUG-0096` | 验收返修：统一品牌、类目、状态筛选下拉的触发框、菜单位置、选项样式和选中态；补充前端一致性测试。 |
| 2026-07-31 21:15:20 | `/opsx-modify BUG-0096` | 验收返修：移除类目筛选下方「当前：xxx」文案；修复类目下拉层层级和位置，确保下拉位于筛选控件下方且不被 SKU 列表遮挡。 |
| 2026-07-31 20:53:08 | `/opsx-modify BUG-0096` | 验收返修：类目筛选 UI 改为单个级联下拉框，点击有下级类目时在右侧展开下级类目面板；同步前端测试与行为文档。 |
| 2026-07-31 15:36:25 | `/sprint-propose sprint-015` | 纳入 sprint-015 正式范围。 |
| 2026-07-31 15:17:04 | `/bug-opsx BUG-0096` | 创建修复 Change，状态为 proposed。 |
