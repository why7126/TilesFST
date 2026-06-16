# REQ-0005 用户管理列表页 v2（UI 优化）— 原型上下文

## 1. 原型目标

本文件指导 **列表页 UI 优化**（`REQ-0005-user-management-list-refine`）的前端还原。优先级：

1. `user-management-list.html`（本目录 v2）
2. `user-management-list.png`（待重新导出）
3. 本 context 文件
4. `requirement.md`
5. `REQ-0005-user-management` 弹窗原型（modal 不变）

## 2. v2 相对 v1 变更摘要

| # | 变更 |
|---|------|
| 1 | 删除「搜索」按钮 |
| 2 | 关键词 placeholder：「搜索用户名/昵称」 |
| 3 | 删除「用户列表」标题行 |
| 4 | 删除 table-toolbar（含「仅后台管理员可编辑用户」） |
| 5 | 用户列：用户名、昵称 **两行** 纵向排列 |
| 6 | 分页：左「共 x 个用户」；右页码 +「每页显示 x 条」 |

## 3. 页面画布

与 v1 相同：1440×1024、Sidebar 264px、内容 max-width 1080px。

## 4. 搜索筛选区

- 字段：关键词、角色、状态、登录情况、**重置**（无搜索按钮）。
- 关键词 placeholder：**搜索用户名/昵称**。
- 网格列（桌面）：`1.5fr 1fr 1fr 1.1fr auto`。
- 交互：输入防抖/回车/筛选项变更触发查询（实现层）；重置清空全部条件。

## 5. 用户列表

- 指标卡下方 **直接** 接 `table-card`，无 section-head。
- 无 table-toolbar。
- 表头列不变。
- 用户单元格：`.user-meta` 纵向两行 — `.user-main`（用户名）、`.user-sub`（昵称或「未设置昵称」）。

## 6. 分页

```text
.pagination
├─ .page-summary     「共 126 个用户」
└─ .page-right
   ├─ .page-buttons  ‹ 1 2 3 … ›
   └─ .page-size-wrap 「每页显示」+ select
```

禁止展示：`1-10 / 126`、`当前显示`、孤立「每页」前缀（无「显示」）。

## 7. 一致性检查清单

- [ ] 无「搜索」按钮
- [ ] placeholder 为「搜索用户名/昵称」
- [ ] 无「用户列表」标题行
- [ ] 无 toolbar 提示行
- [ ] 用户名列两行
- [ ] 分页左「共 x 个用户」、右页码 + 每页条数
- [ ] 弹窗仍引用 REQ-0005 modal 原型，本 HTML 不含弹窗
