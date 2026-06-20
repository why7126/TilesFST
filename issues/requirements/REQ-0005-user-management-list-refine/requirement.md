---
requirement_id: REQ-0005-user-management-list-refine
title: 管理后台用户管理列表页 UI 优化
terminal: web-admin
version: v1
status: in_sprint
owner: product
source: 基于 REQ-0005-user-management 已实现页面的产品优化反馈
parent_requirement: REQ-0005-user-management
---

# REQ-0005 用户管理列表页 UI 优化

## 1. 需求背景

`REQ-0005-user-management`（OpenSpec `add-user-management`）已落地用户管理列表页。产品方对 **列表页筛选区、表格标题区与用户列、分页区** 提出六项 UI/交互优化，以简化操作路径、收紧信息层级，并与实际搜索能力（用户名/昵称）保持一致。

本需求为 **REQ-0005 子需求**，仅变更列表页展示与关键词搜索范围；**不包含** 添加/编辑弹窗、权限模型、指标卡、行操作等业务逻辑变更。

## 2. 优化项总览

| # | 优化项 | 变更摘要 |
|---|--------|----------|
| O-01 | 删除「搜索」按钮 | 筛选区仅保留「重置」；查询由输入/筛选变更触发 |
| O-02 | 搜索框预置文案与范围 | placeholder「搜索用户名/昵称」；**不支持**邮箱、手机号搜索 |
| O-03 | 删除用户列表标题行 | 移除「用户列表」及同行「共 N 个用户」区块 |
| O-04 | 删除表格 toolbar 行 | 移除「当前显示 1-10 / N」与「仅后台管理员可编辑用户」整行 |
| O-05 | 用户列两行展示 | 第一行用户名，第二行昵称；禁止与用户名挤在同一行 |
| O-06 | 分页区文案精简 | 左侧「共 x 个用户」；右侧页码 +「每页显示 x 条」；删除其他分页文案 |

## 3. 目标用户

- **后台管理员**：日常浏览、筛选、维护用户列表。

## 4. 范围

### 4.1 本期包含

- 列表页筛选区 UI 与交互（O-01、O-02）
- 表格上方标题/toolbar 移除（O-03、O-04）
- 用户列单元格布局（O-05）
- 分页区布局与文案（O-06）
- 后端 `keyword` 查询范围收窄为 `username`、`display_name`（与 O-02 一致）
- 更新列表页 HTML 原型与 context 文档

### 4.2 本期不包含

- 添加/编辑用户弹窗（沿用 `REQ-0005` modal 原型）
- 4 指标卡内容与样式
- 角色/状态/登录情况筛选项定义
- 行操作（编辑、重置密码、冻结、删除）
- 新 API 端点或权限变更

## 5. 功能要求

### FR-001 删除「搜索」按钮

- 筛选区 MUST NOT 展示「搜索」主按钮。
- MUST 保留「重置」按钮；点击后清空关键词及全部筛选项并重新加载列表（page 重置为 1）。
- 关键词输入 MUST 在 **回车** 或 **失焦后防抖（建议 300ms）** 或 **筛选项变更** 时触发列表刷新（page 重置为 1）。
- 筛选区控件高度仍为 40px；桌面端网格列数由 6 列减为 5 列（关键词、角色、状态、登录情况、重置）。

### FR-002 搜索框预置文案与匹配范围

- 关键词输入框 placeholder MUST 为：**「搜索用户名/昵称」**（无空格分隔符亦可接受「搜索用户名 / 昵称」，以原型为准）。
- 前端 MUST NOT 在 placeholder 或帮助文案中提及邮箱、手机号。
- 后端 `GET /api/v1/admin/users?keyword=` MUST 仅对 `username`、`display_name` 做模糊匹配；MUST NOT 匹配 `email`、`phone`。
- 空关键词时不附加 keyword 条件。

### FR-003 删除用户列表标题行

- 表格区域上方 MUST NOT 展示 `section-head`（含「用户列表」标题及右侧「共 N 个用户」）。
- 表格卡片（`table-card`）在指标卡下方直接开始，保留表头行（用户、角色、状态、最后登录、创建时间、操作）。

### FR-004 删除表格 toolbar 行

- MUST NOT 展示 `table-toolbar` 整行。
- MUST NOT 展示「当前显示 x-y / N」。
- MUST NOT 展示「仅后台管理员可编辑用户」提示文案。

### FR-005 用户列两行展示

- 「用户」列 MUST 分两行展示文本信息（头像仍在左侧）：
  - **第一行**：用户名（`username`），主文字样式。
  - **第二行**：昵称（`display_name`）；若为空显示「未设置昵称」，弱文字样式。
- MUST NOT 将用户名与昵称拼接在同一行显示。
- 第二行 MUST NOT 回退展示邮箱；邮箱不属于列表展示字段。
- 实现 MUST 使用块级/纵向布局（如 `flex-direction: column`），确保两行始终换行显示。

### FR-006 分页区文案与布局

- 分页条位于表格底部，左右两端对齐：
  - **左侧**：固定文案 **「共 {total} 个用户」**，`total` 为当前筛选条件下的用户总数（与 API `summary.total` 或 `pagination.total` 一致）。
  - **右侧**：页码按钮组（上一页、页码、下一页）+ **「每页显示」** + 条数选择器（10 / 20 / 50）。
- MUST NOT 展示「每页」「x-y / N」「当前显示」等旧文案。
- 条数选择器标签推荐：**「每页显示 10 条」** 形式（select 选项或组合标签以原型为准）。

## 6. UI / UE 约束

- 继承 `AdminLayout` 与 `user-management.css` CSS Port 风格；禁止裸 Hex。
- 变更后须与 `prototype/web/user-management-list.html` 对齐，并更新 PNG Golden Reference（`user-management-list.png`）。
- 弹窗行为仍以 `REQ-0005-user-management/prototype/web/user-management-modal.*` 为准，本需求不修改。

## 7. 关联需求

| 需求 | 关系 |
|---|---|
| REQ-0005-user-management | 父需求；本需求 MODIFIED 列表页 §6.1、§6.3、§6.4 部分展示规则 |
| REQ-0004-admin-home | 布局壳层、Sidebar、指标卡样式 |
| add-user-management | 已实现基线；本优化建议新建 `fix-user-management-list-refine` change |

## 8. 状态

```yaml
requirement_id: REQ-0005-user-management-list-refine
priority: P1
status: in_sprint
owner: 产品负责人
iteration: sprint-002
openspec_change: fix-user-management-list-refine
```
