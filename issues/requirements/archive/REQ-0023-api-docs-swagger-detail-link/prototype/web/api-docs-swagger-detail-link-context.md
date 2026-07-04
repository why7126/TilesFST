---
requirement_id: REQ-0023-api-docs-swagger-detail-link
title: 接口文档行级 Swagger 查看入口原型上下文
status: pending_review
owner: product
source: requirement.md
created_at: 2026-07-01 13:55:01
updated_at: 2026-07-01 13:55:01
---

# Prototype Context

## 视觉来源优先级

1. `issues/requirements/archive/REQ-0022-admin-api-docs-menu/prototype/web/api-docs.html`
2. `issues/requirements/archive/REQ-0022-admin-api-docs-menu/prototype/web/api-docs-context.md`
3. `issues/requirements/archive/REQ-0023-api-docs-swagger-detail-link/prototype/web/api-docs-swagger-detail-link.html`
4. `issues/requirements/archive/REQ-0023-api-docs-swagger-detail-link/acceptance.md`
5. `rules/ui-design.md`

## 本原型表达内容

- 在现有 `/admin/api-docs` 表格右侧新增 ACTION 列。
- OpenAPI 路由显示可点击「查看」，示例 href 为 `/docs#/admin-api-docs/get_api_docs_api_v1_admin_api_docs_get`。
- 非 OpenAPI 路由显示禁用态「查看」，并解释「未纳入 OpenAPI」。
- Swagger 行级入口使用新窗口策略；当前管理端页面保持不动。

## 非本原型范围

- 不重新定义 REQ-0022 的页面 hero、summary、filter 视觉。
- 不内嵌 Swagger UI。
- 不展示 token 自动注入或 Swagger Authorize 行为。
- PNG Golden 暂未导出；后续如需视觉验收，可从 HTML 在 1440×1024 视口导出。

## 验收提示

- 对照 `/admin/users` 分页 DOM：`page-summary` + `page-right`。
- 检查禁用态按钮不可点击，没有 href。
- 检查可用链接 `target="_blank"` 且不包含 token。
