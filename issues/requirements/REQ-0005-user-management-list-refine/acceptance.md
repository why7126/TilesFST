---
title: 需求验收标准
purpose: REQ-0005 用户管理列表页 UI 优化验收标准
content: 基于 requirement.md 与 prototype/web/user-management-list.html
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
note: REQ-0005-user-management-list-refine
---

# 验收标准

## 1. 筛选区（O-01、O-02）

- [ ] **AC-001** 筛选区不展示「搜索」按钮。
- [ ] **AC-002** 筛选区展示「重置」按钮；点击后清空关键词、角色、状态、登录情况并 reload，page=1。
- [ ] **AC-003** 关键词 placeholder 为「搜索用户名/昵称」（或与原型 HTML 完全一致）。
- [ ] **AC-004** 关键词回车或防抖后触发查询；变更任一下拉筛选项后自动查询，page 重置为 1。
- [ ] **AC-005** 界面无任何「邮箱」「手机号」搜索提示文案。
- [ ] **AC-006** 后端：keyword 仅匹配 `username`、`display_name`；含 email/phone 的数据不会被 keyword 误命中（集成测试或手工用例）。

## 2. 列表标题与 toolbar（O-03、O-04）

- [ ] **AC-007** 指标卡与表格之间无「用户列表」标题行。
- [ ] **AC-008** 表格内无 `table-toolbar` 行。
- [ ] **AC-009** 页面不展示「当前显示 x-y / N」文案。
- [ ] **AC-010** 页面不展示「仅后台管理员可编辑用户」文案。
- [ ] **AC-011** 表头列仍为：用户、角色、状态、最后登录、创建时间、操作。

## 3. 用户列（O-05）

- [ ] **AC-012** 用户名列第一行仅显示 `username`。
- [ ] **AC-013** 第二行显示昵称；空昵称显示「未设置昵称」。
- [ ] **AC-014** 第二行不显示邮箱。
- [ ] **AC-015** 用户名与昵称视觉上为两行（非同一行连续文本）；窄屏下亦保持纵向排列。

## 4. 分页区（O-06）

- [ ] **AC-016** 分页左侧文案为「共 {total} 个用户」，total 与当前筛选结果总数一致。
- [ ] **AC-017** 分页右侧包含页码控件（上一页、当前页、下一页）与每页条数选择。
- [ ] **AC-018** 每页条数标签/选项含「每页显示」语义（如「每页显示 10 条」）。
- [ ] **AC-019** 分页区不展示「1-10 / N」「每页」（孤立词）、「当前显示」等旧文案。
- [ ] **AC-020** 切换 10/20/50 条后列表与 total 展示正确。

## 5. 回归与不回归

- [ ] **AC-021** 4 指标卡、添加用户按钮、行操作、弹窗行为与 REQ-0005 一致（无回归）。
- [ ] **AC-022** `employee` 仍不可见用户管理菜单；API 仍 admin-only。
- [ ] **AC-023** `npm run build` 与相关 vitest 通过。
- [ ] **AC-024** 1280×1024 与更新后的 `user-management-list.png` 并排验收（PNG 须随原型更新）。

## 6. 技术验收

- [ ] **AC-025** 变更经 OpenSpec `fix-user-management-list-refine`（或等价 fix-* change）进入开发。
- [ ] **AC-026** 样式使用 semantic token / CSS Port，TSX 无裸 Hex。
- [ ] **AC-027** 若修改 repository 搜索逻辑，补充或更新 pytest 覆盖 keyword 范围。
