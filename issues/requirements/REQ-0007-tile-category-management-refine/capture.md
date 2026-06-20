---
req_id: REQ-0007-tile-category-management-refine
status: captured
recorded_at: 2026-06-20
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement: REQ-0005-tile-category-management
---

# 一句话

瓷砖类目管理页：启停操作增加二次确认；去掉检索区/列表区 section 标题；底部分页文案与布局对齐用户管理页 v2。

# 原始描述

瓷砖类目页，优化点：

1. 启用/停用 需要二次确认
2. 类目检索标题、类目列表标题不需要
3. 列表底部的分页文案与布局，与用户管理页一致

# 分类结论（需求 vs 缺陷）

| 优化点 | 归类 | 理由 |
|--------|------|------|
| 1. 启停二次确认 | **需求** | 父需求 AC-015 / business-flow 为直接启停；删除才有确认弹窗；属新增交互策略 |
| 2. 去掉检索/列表 section 标题 | **需求** | 当前与 HTML 原型一致（含「类目检索」「类目列表」）；属相对原型的 UI 精简 |
| 3. 分页对齐用户管理页 | **需求** | 类目页现按 AC-020「当前显示 x-y / N 条」实现；用户管理 v2（REQ-0005-user-management-list-refine）为「共 N 个类目」+ 新布局；属跨页一致性优化 |

**非 BUG**：无功能缺失或错误实现；与已归档 `add-tile-category-management` / BUG-0001 修复无冲突。

# 参考实现

- 分页参考：`src/web/src/pages/admin/UserManagementPage.tsx`（`.pagination` / `.page-summary` / `.page-right`）
- 当前类目页：`src/web/src/pages/admin/TileCategoryManagementPage.tsx`（`.cat-pager`、「当前显示 …」）
- 类似子需求：`REQ-0005-user-management-list-refine` → `fix-user-management-list-refine`

# 待澄清

- [ ] 启停确认弹窗文案（如「确认停用类目「{name}」？」/「确认启用…」）是否与删除确认风格一致
- [ ] 去掉 section 标题后，是否同时去掉副标题 `section-note`（如「按名称、状态与层级筛选」）
- [ ] 列表工具栏内「当前树节点名称 + 记录数」是否保留（仅去掉外层「类目列表」标题）
- [ ] 分页 summary 文案：「共 N 个类目」还是「共 N 条类目」
- [ ] 变更类型：`fix-tile-category-management-refine` vs `update-*`（建议 fix-*，对齐 user-management-list-refine）

# 探索结论

（/req-explore 后人工确认写入）
