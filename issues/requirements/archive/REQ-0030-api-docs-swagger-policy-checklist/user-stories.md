---
requirement_id: REQ-0030-api-docs-swagger-policy-checklist
title: 接口文档页 Swagger 代理与生产调试策略 checklist - 用户故事
status: pending_review
owner: product
created_at: 2026-07-04 22:19:09
updated_at: 2026-07-04 22:19:09
---

# 用户故事

## US-001 产品负责人维护接口文档页模板 checklist

作为产品负责人，我希望接口文档页 PRD、design 或模板 checklist 中固定包含 Swagger Web 代理与生产调试策略，以便后续 API docs refine 不只关注页面功能，还能覆盖部署边界和安全门禁。

验收要点：

- checklist 明确适用于 API docs refine、Swagger 入口调整、Web 代理调整和生产部署说明调整。
- checklist 明确 `/docs`、`/redoc`、`/openapi.json` 与 Swagger UI 依赖资源的检查范围。
- checklist 明确生产环境 `Try It Out` 必须禁用或只读。

## US-002 前端开发按同源策略实现 Swagger 入口

作为前端开发，我希望 checklist 明确 Swagger 入口必须使用同源 Web 路由，以便实现时不硬编码后端主机或端口，并避免 `/docs` 被 SPA fallback 接管。

验收要点：

- Swagger 入口使用 `/docs` 或经 design 说明的等价同源路径。
- 行级 Swagger 深链使用同源 URL，不携带 token、密钥或真实环境变量。
- 前端实现不出现 `localhost:8000`、`backend:8000` 等硬编码后端地址。

## US-003 DevOps 按环境验证代理路径

作为 DevOps 或部署负责人，我希望 checklist 分别覆盖 Vite dev proxy、Docker Nginx 和生产反向代理，以便在不同运行环境中都能从 Web 入口打开后端 Swagger 文档。

验收要点：

- 本地 Web 访问 `/docs` 进入后端 Swagger UI 或等价后端文档响应。
- Docker Web 访问 `/docs` 不进入 Web 首页或 SPA fallback。
- 生产等价环境中 `/docs`、`/redoc`、`/openapi.json` 的路由策略有明确验证记录。

## US-004 QA 验证生产在线调试门禁

作为 QA，我希望 checklist 把生产 `Try It Out` 禁用作为必测项，以便确认 Web 代理不会意外放开生产环境在线调试。

验收要点：

- 非生产环境可按策略允许 Swagger 在线调试。
- 生产等价环境中 Swagger 文档可见但 `Try It Out` 禁用、隐藏或等价只读。
- 页面提示与后端实际策略一致，不出现生产可调试的误导文案。

## US-005 后端开发保持 Swagger 策略与 APP_ENV 一致

作为后端开发，我希望 checklist 要求后端 Swagger UI 参数与 `APP_ENV` 策略一致，以便生产环境在后端层面也禁用在线调试，而不是只依赖前端文案。

验收要点：

- 后端生产配置使用 `swagger_ui_parameters.tryItOutEnabled=false` 或等价机制。
- 非生产环境策略与 `local`、`development`、`dev`、`demo`、`test` 等环境定义一致。
- 不新增绕过管理员权限或生产只读策略的 Swagger 调试入口。
