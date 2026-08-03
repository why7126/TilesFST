---
change_id: fix-admin-sku-material-main-image-tag
type: fix
status: applied
source_bug: BUG-0097-admin-sku-material-main-image-tag-redundant
related_requirement: REQ-0006-tile-sku-management
created_at: 2026-07-31 15:16:00
updated_at: 2026-07-31 15:40:28
iteration: sprint-015
---

# Trace

```yaml
change_id: fix-admin-sku-material-main-image-tag
type: fix
status: applied
source_bug: BUG-0097-admin-sku-material-main-image-tag-redundant
related_requirement: REQ-0006-tile-sku-management
iteration: sprint-015
```

## 来源

- BUG：`BUG-0097-admin-sku-material-main-image-tag-redundant`
- 父需求：`REQ-0006-tile-sku-management`
- 能力：`tile-sku-management`

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 15:36:22 | `/opsx-modify BUG-0097` | 验收返修：删除素材完整度条件筛选，列表请求不再提交 `material_completeness`；同步测试与文档。 |
| 2026-07-31 15:28:34 | `/opsx-modify BUG-0097` | 验收返修：素材列只显示图片/视频数量，移除「缺主图」等素材状态标签；同步测试与文档。 |
| 2026-07-31 15:22:52 | `/opsx-apply fix-admin-sku-material-main-image-tag` | 实现完成，tasks 9/9，状态为 applied。 |
| 2026-07-31 15:16:00 | `/bug-opsx BUG-0097` | 创建修复 Change，状态为 proposed。 |
| 2026-07-31 15:17:00 | `/sprint-propose sprint-015` | 纳入 sprint-015 正式范围。 |
