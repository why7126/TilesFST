---
requirement_id: REQ-0007-tile-category-management-refine
title: 管理后台瓷砖类目管理页 UI 优化
terminal: web-admin
version: v1
status: in_sprint
iteration: sprint-002
owner: product
source: issues/requirements/archive/REQ-0007-tile-category-management-refine/capture.md
priority: P1
parent_requirement: REQ-0005-tile-category-management
---

# REQ-0007 瓷砖类目管理页 UI 优化

## 1. 需求背景

`REQ-0005-tile-category-management`（OpenSpec `add-tile-category-management`）已落地瓷砖类目管理页，含类目树、检索、列表、启停、条件删除与分页。产品方对 **启停交互、检索/列表区标题层级、分页区** 提出三项 UI/交互优化，以提升误操作防护，并与其他管理列表页（用户管理 v2）保持一致。

本需求为 **REQ-0005 子需求**，仅变更列表页展示与启停确认流程；**不包含** 类目 CRUD 业务规则、API、指标卡、类目树、弹窗字段、删除规则变更。

## 2. 优化项总览

| # | 优化项 | 变更摘要 |
|---|--------|----------|
| O-01 | 启停二次确认 | 点击「启用」「停用」须先确认，再调用 enable/disable API |
| O-02 | 去掉检索区 section 标题 | 移除「类目检索」标题及副标题；筛选表单直接展示 |
| O-03 | 去掉列表区 section 标题 | 移除「类目列表」标题及副标题；保留表格内工具栏（树节点名 + 记录数） |
| O-04 | 分页区对齐用户管理 v2 | 左侧「共 N 个类目」；右侧页码 +「每页显示」；移除「当前显示 x-y / N 条」 |

## 3. 目标用户

- **后台管理员 / 内部员工**：维护瓷砖类目启停与列表浏览。

## 4. 范围

### 4.1 本期包含

- 启用/停用确认弹窗（O-01）
- 检索区、列表区外层 `section-head` 移除（O-02、O-03）
- 列表底部分页文案与布局（O-04）
- 样式调整（`tile-category-management.css` 或复用 `user-management.css` 分页类名）
- vitest 覆盖启停确认与分页 DOM 断言

### 4.2 本期不包含

- 新增/编辑类目弹窗（沿用 `REQ-0005` modal 原型）
- 4 指标卡、类目树、筛选字段定义、查询/重置逻辑
- 删除确认弹窗（沿用现有「删除类目」流程）
- 删除/启停 API、OpenAPI、Orval 变更
- 「调整排序」占位实现
- HTML 原型文件强制改版（可选于 `/req-complete` 同步）

## 5. 功能要求

### FR-001 启用/停用二次确认

- 用户点击行内「启用」或「停用」时，MUST NOT 直接调用 API。
- MUST 弹出确认对话框，视觉与结构对齐现有「删除类目」确认框（`modal-backdrop` + `modal-card` + head/body/footer）。
- 弹窗标题：
  - 停用：**「停用类目」**
  - 启用：**「启用类目」**
- 弹窗正文 MUST 包含类目名称，推荐文案：
  - 停用：**「确认停用类目「{name}」？停用后前台将不再展示该类目。」**
  - 启用：**「确认启用类目「{name}」？」**
- 底部按钮：**「取消」**（关闭弹窗，不调用 API）、**「确认停用」** / **「确认启用」**（主按钮，调用对应 API）。
- 确认成功后 MUST 展示 Toast（沿用「类目已启用」「类目已停用」），并刷新类目树与列表。
- 取消或点击遮罩关闭时 MUST NOT 改变类目状态。
- 删除操作仍走独立删除确认弹窗，本 FR 不合并删除与启停。

### FR-002 去掉类目检索 section 标题

- 检索区上方 MUST NOT 展示 `section-head`（含 **「类目检索」** 标题及 **「按名称、状态与层级筛选」** 副标题）。
- 筛选区（`filter-card` + 关键词/状态/层级 + 查询/重置）MUST 保留，布局与交互不变。
- 指标卡与检索区之间的区块间距 MUST 保持与优化前视觉连贯（无标题留白异常）。

### FR-003 去掉类目列表 section 标题

- 列表区外层 MUST NOT 展示 `section-head`（含 **「类目列表」** 标题及 **「删除仅支持 SKU 数量为 0 的类目」** 副标题）。
- 表格卡片内 **工具栏**（`cat-table-toolbar`）MUST **保留**：
  - 左侧：当前树上下文标题（如「全部类目」/「选中类目及子孙」）+ **「共 {total} 条记录」**
  - 右侧：「调整排序」按钮
- 类目树（280px）、表格列、行操作（编辑、启停、删除）规则 MUST 与 `REQ-0005` / BUG-0001 修复后行为一致。

### FR-004 分页区文案与布局（对齐用户管理 v2）

- 分页条位于表格底部，左右两端对齐，结构对齐 `UserManagementPage`（`.pagination` / `.page-summary` / `.page-right`）：
  - **左侧**：**「共 {total} 个类目」**，`total` 为当前筛选条件下的类目总数（与 API `total` 一致）。
  - **右侧**：页码按钮组（上一页、当前页、下一页）+ **「每页显示」** + 条数选择器（10 / 20 / 50，选项文案 **「10 条」** / **「20 条」** / **「50 条」**）。
- MUST NOT 展示「当前显示 x-y / N 条」「x-y / N」等旧文案。
- MUST NOT 使用「10 条/页」等与用户管理 v2 不一致的下拉选项格式。
- 切换 `page_size` MUST 重置页码为 1 并保留筛选条件（行为不变）。

## 6. UI / UE 约束

- 继承 `AdminLayout` 与 `tile-category-management.css` CSS Port；禁止裸 Hex。
- 启停确认弹窗 MUST 复用删除确认弹窗的 modal 样式类，保证管理端确认交互一致。
- 分页区 SHOULD 复用用户管理页分页 DOM 结构与 class（或等价 CSS），避免各页分页样式漂移。
- 变更后须与 `REQ-0005-user-management-list-refine` 分页模式并排验收。

## 7. 关联需求

| 需求 / Change | 关系 |
|---|---|
| REQ-0005-tile-category-management | 父需求；本需求 MODIFIED 列表页检索/列表标题、启停交互、分页展示 |
| REQ-0005-user-management-list-refine | 分页布局与文案参考（FR-004） |
| REQ-0004-admin-home | 布局壳层、Sidebar、指标卡 |
| add-tile-category-management | 已实现基线；本优化建议新建 `fix-tile-category-management-refine` change |
| BUG-0001-tile-category-enable-missing | 已修复；本需求不回归启停按钮可见性 |

## 8. 状态

```yaml
requirement_id: REQ-0007-tile-category-management-refine
priority: P1
status: in_sprint
iteration: sprint-002
owner: 产品负责人
parent_requirement: REQ-0005-tile-category-management
openspec_change: fix-tile-category-management-refine
```
