---
change_id: fix-admin-category-tree-count
type: fix
status: applied
source_bug: BUG-0095-admin-category-tree-count-shows-product-count
related_requirement: REQ-0005-tile-category-management
created_at: 2026-07-31 15:13:20
updated_at: 2026-07-31 17:29:59
---

# Trace

```yaml
change_id: fix-admin-category-tree-count
type: fix
status: applied
source_bug: BUG-0095-admin-category-tree-count-shows-product-count
related_requirement: REQ-0005-tile-category-management
iteration: sprint-015
```

## 来源

- BUG：`BUG-0095-admin-category-tree-count-shows-product-count`
- 父需求：`REQ-0005-tile-category-management`
- 能力：`tile-category-management`、`web-client`

## Bug Analysis Report

- 现象：管理端类目树右侧数值显示为商品数量，而非下一层级类目数量。
- 复现：打开管理端类目树，查看一级类目右侧数字并与直接子类目数量对比。
- 影响：后台运营可能误判类目层级结构，影响类目维护和数据排查。
- 根因分类：`ui-contract / data-mapping / count-semantics`。
- 严重等级：`medium`。
- 关联需求：`REQ-0005-tile-category-management`。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 17:29:59 | `/opsx-modify` | 验收返修：移除“全部类目”文字负向偏移和左侧占位，改为完整整行按钮，确保选中态边框完整包住入口文字和右侧数值。 |
| 2026-07-31 17:24:07 | `/opsx-modify` | 验收返修：保留“全部类目”右侧数值位置不变，仅将“全部类目”文字左移到与类目树标题文字左对齐；补充组件样式契约测试。 |
| 2026-07-31 17:18:45 | `/opsx-modify` | 验收返修：将“全部类目”入口与一级类目节点复用同一行布局和左侧占位，使右侧数值位置对齐；补充组件测试、design 与 web-client delta spec。 |
| 2026-07-31 15:31:48 | `/opsx-apply` | Change apply 完成，状态同步为 applied，待人工验收与 archive。 |
| 2026-07-31 15:20:06 | `/sprint-propose sprint-015` | 纳入 Sprint 015 正式范围。 |
| 2026-07-31 15:13:20 | `/bug-opsx BUG-0095` | 创建修复 Change，状态为 proposed。 |
