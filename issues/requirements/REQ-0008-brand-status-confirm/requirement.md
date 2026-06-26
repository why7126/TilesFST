---
requirement_id: REQ-0008-brand-status-confirm
title: 管理后台品牌列表启停二次确认
terminal: web-admin
version: v1
status: done
iteration: sprint-002
owner: product
source: issues/requirements/REQ-0008-brand-status-confirm/capture.md
priority: P1
parent_requirement: REQ-0005-brand-management
---

# REQ-0008 管理后台品牌列表启停二次确认

## 1. 需求背景

`REQ-0005-brand-management`（OpenSpec `add-brand-management`）已落地瓷砖品牌管理页，含检索、列表、新增/编辑弹窗、启用、停用、条件删除与分页。当前行内「启用」「停用」点击后直接调用 API，误触风险较高；删除操作已有独立确认弹窗。

产品方要求 **启用与停用均增加二次确认**，交互与文案对齐：

- 同页「删除品牌」确认弹窗（`modal-card` 结构）
- 类目管理页已落地的启停确认（`REQ-0007-tile-category-management-refine`）

本需求为 **REQ-0005 子需求**，仅变更列表页启停交互流程；**不包含** 品牌 CRUD 业务规则、API、指标卡、筛选、分页、弹窗字段、删除规则变更。

## 2. 优化项总览

| # | 优化项 | 变更摘要 |
|---|--------|----------|
| O-01 | 启停二次确认 | 点击「启用」「停用」须先确认，再调用 enable/disable API |

## 3. 目标用户

- **后台管理员 / 内部员工（employee）**：维护瓷砖品牌启停状态。

## 4. 范围

### 4.1 本期包含

- 启用/停用确认弹窗（O-01）
- 复用现有删除确认弹窗样式类（`modal-backdrop`、`modal-card`、`modal-head`、`modal-body`、`modal-footer`）
- vitest 覆盖启停确认弹窗 DOM 与交互断言

### 4.2 本期不包含

- 新增/编辑品牌弹窗（沿用 `REQ-0005` modal 原型）
- 4 指标卡、筛选字段、查询/重置逻辑
- 删除确认弹窗（沿用现有「删除品牌」流程）
- 删除/启停 API、OpenAPI、Orval 变更
- 批量启停、导出、分页布局变更
- HTML 原型文件强制改版（可选于 `/req-complete` 同步 context 文档）

## 5. 功能要求

### FR-001 启用/停用二次确认

- 用户点击行内「启用」或「停用」时，MUST NOT 直接调用 API。
- MUST 弹出确认对话框，视觉与结构对齐现有「删除品牌」确认框（`modal-backdrop` + `modal-card` + head/body/footer）。
- 弹窗标题：
  - 停用：**「停用品牌」**
  - 启用：**「启用品牌」**
- 弹窗正文 MUST 包含品牌名称 `{name}`（取列表行 `brand.name`），文案 MUST 为：
  - 停用：**「确认停用品牌「{name}」？停用后前台将不再展示该品牌。」**
  - 启用：**「确认启用品牌「{name}」？」**
- 底部按钮：**「取消」**（关闭弹窗，不调用 API）、**「确认停用」** / **「确认启用」**（主按钮，调用对应 API）。
- 确认成功后 MUST 展示 Toast（沿用「品牌已启用」「品牌已停用」），并刷新品牌列表与指标卡摘要。
- 取消、点击遮罩、按 ESC 或点击 × 关闭时 MUST NOT 改变品牌状态。
- 删除操作仍走独立删除确认弹窗，本 FR 不合并删除与启停。
- 行内按钮文案仍为「启用」/「停用」，仅增加确认前置步骤；按钮可见性与权限规则 MUST 与 `REQ-0005` 一致。

### FR-002 无障碍与一致性

- 确认弹窗 MUST 设置 `role="dialog"`、`aria-modal="true"`，标题元素 MUST 有 `aria-labelledby` 指向弹窗标题 id（对齐删除弹窗实现）。
- 启停确认弹窗 MUST 复用删除确认弹窗的 modal 样式类，保证管理端确认交互一致。
- 禁止在 TSX/CSS 中新增裸 Hex；继承 `AdminLayout` 与 `brand-management.css`。

## 6. UI / UE 约束

- 弹窗结构参考 `BrandManagementPage.tsx` 删除确认弹窗及 `TileCategoryManagementPage.tsx` 启停确认弹窗。
- 文案风格 MUST 与品牌删除、类目启停确认一致：标题为动作名，正文以「确认…「{name}」？」开头，主按钮为「确认停用 / 确认启用」。
- 停用正文 MUST 包含业务说明「停用后前台将不再展示该品牌。」；启用正文不额外补充业务说明。

## 7. 关联需求

| 需求 / Change | 关系 |
|---|---|
| REQ-0005-brand-management | 父需求；本需求 MODIFIED 列表页启停交互 |
| REQ-0007-tile-category-management-refine | 启停确认交互与文案模式参考（FR-001） |
| REQ-0004-admin-home | 布局壳层、Sidebar、指标卡 |
| add-brand-management | 已实现基线；本优化建议新建 `fix-brand-status-confirm` change |

## 8. 状态

```yaml
requirement_id: REQ-0008-brand-status-confirm
priority: P1
status: done
iteration: sprint-002
owner: product
parent_requirement: REQ-0005-brand-management
openspec_change: fix-brand-status-confirm
```
