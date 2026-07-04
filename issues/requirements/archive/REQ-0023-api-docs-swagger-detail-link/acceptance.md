---
requirement_id: REQ-0023-api-docs-swagger-detail-link
title: 接口文档列表行级查看并跳转 Swagger 详情 - Acceptance
status: pending_review
owner: product
source: requirement.md
created_at: 2026-07-01 13:55:01
updated_at: 2026-07-01 13:55:01
---

# 验收标准

## 1. 功能验收

- [ ] **AC-001** 管理员访问 `/admin/api-docs` 时，接口列表表格 MUST 展示行级操作列。
- [ ] **AC-002** `included_in_openapi=true` 且 `operation_id` 非空的接口行 MUST 展示可点击「查看」入口。
- [ ] **AC-003** 点击可用「查看」入口 MUST 在新窗口或新标签页打开 Swagger UI。
- [ ] **AC-004** Swagger UI 链接 MUST 定位到具体 `operationId` 锚点，而不是仅打开通用 `/docs`。
- [ ] **AC-005** Swagger 深链 MUST 对 tag 与 operationId 做 URL 安全编码。
- [ ] **AC-006** 当前 `/admin/api-docs` 页面在点击后 MUST 保持原筛选条件、列表状态和登录状态。

## 2. 非 OpenAPI 路由验收

- [ ] **AC-007** `included_in_openapi=false` 的路由仍 MUST 展示在接口目录中。
- [ ] **AC-008** `included_in_openapi=false` 的路由 MUST 显示禁用态「查看」或等价不可点击状态。
- [ ] **AC-009** 禁用态入口 MUST 给出原因，例如「未纳入 OpenAPI，暂无 Swagger 详情」。
- [ ] **AC-010** 禁用态入口 MUST NOT 带有可点击 href，MUST NOT 跳转到通用 `/docs` 或错误 operationId。
- [ ] **AC-011** `included_in_openapi=true` 但 `operation_id` 缺失时 MUST 按不可跳转状态处理。

## 3. 权限与安全验收

- [ ] **AC-012** `employee` 用户仍 MUST 无法访问 `/admin/api-docs`，并且看不到行级查看入口。
- [ ] **AC-013** 行级 Swagger 链接 MUST NOT 在 URL、hash、query 或 DOM 可见文本中暴露 Bearer Token、Cookie、用户信息、数据库连接串、MinIO 凭据或环境变量真实值。
- [ ] **AC-014** 新窗口打开 MUST 使用 `rel="noreferrer"` 或等价安全属性。
- [ ] **AC-015** 本需求 MUST NOT 新增 Swagger 自动注入 token 的机制。
- [ ] **AC-016** 生产环境仍 MUST 隐藏或禁用 Swagger `Try It Out`，不得因行级查看入口放宽策略。

## 4. UI 与交互验收

- [ ] **AC-017** 新增 ACTION 列后，接口表格在 1440×1024 视口下 MUST 不出现文字重叠或操作列遮挡。
- [ ] **AC-018** 新增 ACTION 列后，移动窄视口下表格 MUST 继续通过横向滚动查看完整列。
- [ ] **AC-019** 可点击「查看」与禁用态「查看」在视觉和可访问名称上 MUST 可区分。
- [ ] **AC-020** 空结果状态仍 MUST 显示「暂无匹配接口」或等价文案，不渲染误导性的行级操作。
- [ ] **AC-021** 新增 TSX/CSS MUST 使用 semantic token 或既有管理端 CSS 变量，MUST NOT 新增裸 Hex。

## 5. 测试与治理验收

- [ ] **AC-022** 前端测试 MUST 覆盖 OpenAPI 路由生成 `/docs#/{tag}/{operationId}` 链接。
- [ ] **AC-023** 前端测试 MUST 覆盖非 OpenAPI 路由的禁用态「查看」。
- [ ] **AC-024** 前端测试 MUST 断言链接使用新窗口打开且不包含 token。
- [ ] **AC-025** 若实现新增后端字段（例如 `swagger_url`），MUST 同步 OpenAPI、Orval 与 `docs/03-api-index.md`；若仅前端构造链接，则记录为无 API 变更。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 管理端列表页复发类缺陷。

- [ ] **AC-XCUT-001** 新增 ACTION 列后，`/admin/api-docs` 底部分页 DOM MUST 继续对齐 `/admin/users` 基准：左侧 `page-summary`，右侧 `page-right`。
- [ ] **AC-XCUT-002** 行级查看成功、不可用或错误提示如需展示，MUST 使用 fixed toast 或等价不占文档流反馈，MUST NOT 推挤 hero、筛选栏或表格。
- [ ] **AC-XCUT-003** N/A — 本需求不包含状态变更、删除、上下架等危险操作；若后续新增状态类行操作，MUST 使用 Design System confirm modal。
- [ ] **AC-XCUT-004** 实现 MUST NOT 使用 `window.confirm` 或 `window.alert`；当前需求不需要确认弹窗。

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 写入 AC 条数 | 说明 |
|---|---|---:|---|
| `admin-list` | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 4 | 接口目录为管理端表格 + 行内操作；已写入分页 DOM、feedback、confirm N/A、禁止原生弹窗 |
| retrospective | `docs/knowledge-base/retrospectives/sprint-003-retrospective.md` | 0 | 复发模式为列表分页 DOM、toast layout shift、原生 confirm；已转化到 AC-XCUT |
