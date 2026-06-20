# REQ-0007 瓷砖类目管理列表页 v2（UI 优化）— 原型上下文

## 1. 原型目标

本文件指导 **列表页 UI 优化**（`REQ-0007-tile-category-management-refine`）的前端还原。优先级：

1. 本 context 文件 + 父需求 `REQ-0005-tile-category-management/prototype/web/tile-category-management.html`（v1 基线，按下列 diff 修改）
2. `tile-category-management-list-refine.png`（待重新导出）
3. `requirement.md` / `acceptance.md`
4. `REQ-0005-user-management-list-refine` 分页区（并排参考）
5. 父需求弹窗原型 `tile-category-management-add.html`（不变）

## 2. v2 相对 v1 变更摘要

| # | 变更 |
|---|------|
| 1 | 启用/停用：点击后弹出确认框，确认后再请求 API |
| 2 | 删除「类目检索」section-head（含副标题） |
| 3 | 删除「类目列表」section-head（含副标题） |
| 4 | 保留 `cat-table-toolbar`（树上下文 + 共 N 条记录 + 调整排序） |
| 5 | 分页：左「共 x 个类目」；右页码 +「每页显示 x 条」；删除「当前显示 x-y / N 条」 |

## 3. 页面画布

与 v1 相同：1440×1024、Sidebar 264px、内容 max-width 1080px、work-grid 280px 树 + 列表。

## 4. 检索区

- 指标卡下方 **直接** 接 `filter-card`，无 `section-head`。
- 字段不变：类目名称/编码、状态、层级、查询、重置。

## 5. 列表区

- 无外层「类目列表」标题。
- `cat-work-grid` 内：左侧树 + 右侧 `table-card`。
- `cat-table-toolbar` **保留**：
  - 左：如「全部类目」+「共 36 条记录」
  - 右：「调整排序」

## 6. 启停确认弹窗（新增）

结构对齐删除确认弹窗：

```text
.modal-backdrop
└─ .modal-card
   ├─ .modal-head   标题「停用类目」或「启用类目」+ 关闭
   ├─ .modal-body   确认文案（含 {name}）
   └─ .modal-footer 「取消」+「确认停用」/「确认启用」
```

停用正文示例：**确认停用类目「按空间」？停用后前台将不再展示该类目。**

## 7. 分页

```text
.pagination
├─ .page-summary     「共 36 个类目」
└─ .page-right
   ├─ .page-buttons  ‹ 1 ›
   └─ .page-size-wrap 「每页显示」+ select（10 条 / 20 条 / 50 条）
```

禁止展示：`当前显示 1-10 / 36`、`10 条/页`（斜杠格式）。

## 8. 一致性检查清单

- [ ] 启停须二次确认
- [ ] 无「类目检索」「类目列表」section 标题
- [ ] 工具栏树上下文 + 记录数保留
- [ ] 分页左「共 x 个类目」、右页码 + 每页条数
- [ ] 删除仍独立确认弹窗
- [ ] 新增/编辑弹窗仍引用父需求 add.html
