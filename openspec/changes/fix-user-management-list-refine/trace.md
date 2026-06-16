---
title: Change 追溯
purpose: fix-user-management-list-refine 与 REQ、原型、验收映射
---

# fix-user-management-list-refine 追溯

## 1. 关联需求

| 字段 | 值 |
|---|---|
| requirement_id | REQ-0005-user-management-list-refine |
| parent_requirement | REQ-0005-user-management |
| parent_change | add-user-management |
| change_type | fix |
| strategy | css-port（增量 port v2 HTML） |
| iteration | sprint-002 |

## 2. 原型优先级

1. `issues/requirements/REQ-0005-user-management-list-refine/prototype/web/user-management-list.html`（v2）
2. `issues/requirements/REQ-0005-user-management-list-refine/prototype/web/user-management-list.png`
3. `user-management-list-context.md`
4. `acceptance.md`
5. `rules/ui-design.md`

Modal 冻结：`REQ-0005-user-management/prototype/web/user-management-modal.*`

## 3. 优化项映射

| # | 优化项 | 验收 AC |
|---|--------|---------|
| O-01 | 删除搜索按钮 | AC-001, AC-004 |
| O-02 | placeholder + keyword 范围 | AC-003, AC-005, AC-006 |
| O-03 | 删除 section-head | AC-007 |
| O-04 | 删除 table-toolbar | AC-008–AC-010 |
| O-05 | 用户列两行 | AC-012–AC-015 |
| O-06 | 分页精简 | AC-016–AC-019 |

## 4. PNG 视觉 Checklist（1280×1024）

| # | 检查项 | Pass |
|---|--------|------|
| 1 | Admin Shell：264px Sidebar + 右侧滚动 | [ ] |
| 2 | Logo TILESFST；「用户管理」菜单 active | [ ] |
| 3 | 页面标题「用户管理」+ 添加用户品牌金按钮 | [ ] |
| 4 | 筛选区 5 列网格（无搜索按钮） | [ ] |
| 5 | placeholder「搜索用户名/昵称」 | [ ] |
| 6 | 重置按钮存在且样式一致 | [ ] |
| 7 | 4 指标卡布局与 v2 一致 | [ ] |
| 8 | 指标卡与表格之间无「用户列表」标题行 | [ ] |
| 9 | 表格内无 toolbar 提示行 | [ ] |
| 10 | 表头六列：用户、角色、状态、最后登录、创建时间、操作 | [ ] |
| 11 | 用户列：头像 + 用户名/昵称两行纵向 | [ ] |
| 12 | 空昵称显示「未设置昵称」；无邮箱副标题 | [ ] |
| 13 | 分页左「共 x 个用户」 | [ ] |
| 14 | 分页右：页码 +「每页显示」条数 | [ ] |
| 15 | 无「1-10 / N」「当前显示」文案 | [ ] |
| 16 | 角色/状态 badge 颜色与 v2 一致 | [ ] |
| 17 | 行操作链接样式（编辑/重置/冻结/删除）无回归 | [ ] |

## 5. 验证命令

```bash
cd src/backend && uv run pytest tests/test_admin_users.py -q
cd src/web && pnpm exec vitest run src/pages/admin/UserManagementPage
cd src/web && pnpm run build
```

## 6. 已知可接受偏差

- 视口 1280 vs 原型画布 1440：内容区 max-width 1080px 等比验收。
- placeholder 空格：「搜索用户名/昵称」与「搜索用户名 / 昵称」二选一，以 v2 HTML 为准。

## 7. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-16 | `/requirement-to-opsx` | 创建 change 与 artifacts |
