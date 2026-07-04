---
bug_id: BUG-0051-api-docs-swagger-ui-link-wrong
title: 接口文档页 Swagger UI 入口跳转到 Web 首页 - 验收标准
severity: high
status: in_sprint
owner: product
created_at: 2026-07-01 09:27:51
updated_at: 2026-07-01 20:03:09
related_requirement: REQ-0022-admin-api-docs-menu
---

# 验收标准

## AC-001 本地开发 Swagger UI 入口正确

- [x] 启动本地后端与 Web 开发服务。
- [x] 使用 admin 账号进入 `/admin/api-docs`。
- [x] 点击右上角【Swagger UI】。
- [x] Web 开发服务通过 Vite dev proxy 将 `/docs` 转发到后端 Swagger UI。
- [x] 打开的页面不是 Web 首页。
- [x] 页面展示 FastAPI Swagger UI，并能看到 `TilesFST API` 或等价后端 Swagger 标识。

## AC-002 Docker Web 端口访问 `/docs` 正确转发

- [x] 使用 Docker Compose 启动 Web 与 Backend。
- [x] 通过 Web 宿主机端口访问管理端，例如 `http://localhost:3000/admin/api-docs`。
- [x] 点击【Swagger UI】。
- [x] Web 容器 Nginx 将 `/docs` 转发到 backend，而不是进入 SPA fallback。
- [x] 打开的页面不是 `http://localhost:3000/` 首页。
- [x] 打开的页面为 Web 代理后的后端 Swagger UI。

## AC-003 OpenAPI JSON 入口不回退

- [x] 在接口文档页点击【OpenAPI JSON】。
- [x] 打开的页面返回后端 `/openapi.json`。
- [x] 响应包含 `openapi`、`info`、`paths` 等 OpenAPI 基本字段。
- [x] 不返回 Web SPA 的 `index.html`。

## AC-004 生产 Swagger 调试策略不回退

- [x] 将 `APP_ENV` 设置为生产等不允许 Try It Out 的环境。
- [x] 打开接口文档页。
- [x] 页面仍可展示 Swagger 文档入口或只读入口。
- [x] Swagger UI 中 Try It Out 被隐藏或禁用。
- [x] 修复不得通过放开生产调试能力来解决跳转问题。

## AC-005 前端测试覆盖 Swagger 链接行为

- [x] `ApiDocsPage` 单元测试覆盖非生产环境按钮文本为【Swagger UI】且链接目标正确。
- [x] `ApiDocsPage` 单元测试覆盖生产只读按钮文本为【Swagger 只读】且链接目标正确。
- [x] 测试明确防止链接退回 Web 首页。

## AC-006 代理配置回归

- [x] Vite dev proxy 覆盖 Swagger 相关路径。
- [x] Docker Nginx 覆盖 Swagger 相关路径。
- [x] `/api/`、`/media/`、`/openapi.json` 既有代理能力不受影响。

## AC-007 权限与访问范围

- [x] `/admin/api-docs` 仍仅 admin 可访问。
- [x] employee 直接访问 `/admin/api-docs` 仍进入无权限页或等价拦截。
- [x] Swagger UI 入口修复不改变管理端权限边界。

## 验收记录

| 时间 | 验收人 | 结论 | 说明 |
|---|---|---|---|
| 2026-07-01 20:03:09 | Codex | 通过 | `ApiDocsPage` focused Vitest 4/4 通过；Web build 通过；Docker Web 镜像构建通过；容器内 `/docs` 返回 FastAPI Swagger HTML，`/openapi.json` 返回 OpenAPI JSON，`/redoc` 返回 ReDoc HTML；`APP_ENV=production` 下 `allow_swagger_try_it_out()` 为 `False`。 |
