---
bug_id: BUG-0051-api-docs-swagger-ui-link-wrong
title: 接口文档页 Swagger UI 入口跳转到 Web 首页 - 根因分析
severity: high
status: pending_review
owner: product
created_at: 2026-07-01 09:27:51
updated_at: 2026-07-01 09:27:51
related_requirement: REQ-0022-admin-api-docs-menu
---

# 根因分析

## 直接原因

接口文档页右上角 Swagger 入口在 Web 前端中使用相对路径：

```text
/docs
```

当管理端运行在 `localhost:3000` 时，浏览器会将该链接解析为：

```text
http://localhost:3000/docs
```

当前 Web 服务没有把 `/docs` 代理到后端 FastAPI 服务。Docker Nginx 配置中 `/docs` 会落入 SPA 回退规则，React 路由未定义 `/docs`，最终被通配路由重定向到 `/`，表现为进入 Web 首页。

## 根本原因

接口文档页的“后端文档入口”与 Web 部署路由边界没有统一设计：

| 层级 | 现状 | 结果 |
|---|---|---|
| Web 页面 | Swagger 链接写为相对路径 `/docs` | 链接指向 Web Origin |
| Vite dev proxy | 仅代理 `/api`、`/media` | 本地开发下 `/docs` 不会到后端 |
| Docker Nginx | 仅代理 `/api/`、`/openapi.json`、`/media/` | Docker 下 `/docs` 进入 SPA fallback |
| React Router | 通配路由 `*` 重定向 `/` | 用户看到 Web 首页 |

后端 FastAPI 已提供 Swagger UI，并通过 `swagger_ui_parameters.tryItOutEnabled` 控制环境调试策略；问题不在后端 Swagger 本身，而在 Web 入口没有正确抵达后端文档路由。

## 触发条件

满足以下条件即可触发：

1. Web 管理端运行在独立 Origin，例如 `http://localhost:3000`。
2. 后端 Swagger UI 运行在后端服务，例如 `http://localhost:8000/docs`。
3. 管理端接口文档页点击相对链接 `/docs`。
4. Web 服务器未代理 `/docs` 到后端。

## 分类

| 分类 | 判断 |
|---|---|
| code | 是，前端链接与 Web 代理配置未覆盖 Swagger 路由 |
| design | 是，接口文档入口的跨服务访问策略未明确 |
| deployment | 是，Docker Nginx 缺少 `/docs` 代理规则 |
| api | 否，不涉及业务 API 请求/响应结构变更 |
| db | 否，不涉及数据库 |
| security | 否，不涉及鉴权绕过；但修复时必须保留生产 Swagger 只读策略 |
| ui | 是，用户点击入口后到达错误页面 |

## 关联实现点

- Web 页面入口：`src/web/src/pages/admin/ApiDocsPage.tsx`
- 本地开发代理：`src/web/vite.config.ts`
- Docker Web 代理：`src/web/nginx.conf`
- Web 路由回退：`src/web/src/app/App.tsx`
- 后端 Swagger 配置：`src/backend/app/main.py`
- 环境策略：`src/backend/app/core/config.py`

## 修复方向建议

后续修复 Change 中建议优先选择一种明确策略：

1. Web 层代理 Swagger：在 Vite 与 Nginx 中补充 `/docs`、`/redoc` 以及 Swagger 静态资源所需路由代理，保持页面 `href="/docs"` 可用。
2. 后端绝对地址：由接口文档 API 返回 Swagger/OpenAPI 的后端外部访问 URL，Web 页面使用该 URL 打开后端 Swagger。

若选择代理策略，必须同步验证：

- 本地开发与 Docker Web 访问 `/docs` 均进入 FastAPI Swagger UI。
- `/openapi.json` 仍可访问后端 OpenAPI JSON。
- 生产环境仍禁用或隐藏 Swagger `Try It Out`，不因代理而放开调试能力。
