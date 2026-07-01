---
bug_id: BUG-0051-api-docs-swagger-ui-link-wrong
title: 接口文档页 Swagger UI 入口跳转到 Web 首页
severity: high
status: draft
owner: product
discovered_at: 2026-07-01 09:09:32
environment: local
related_requirement: REQ-0022-admin-api-docs-menu
related_change:
created_at: 2026-07-01 09:23:07
updated_at: 2026-07-01 09:23:07
---

# 现象

管理端接口文档页右上角【Swagger UI】入口点击后，没有进入后端 Swagger UI 页面，而是进入 Web 应用首页 `localhost:3000/`。

# 复现步骤

1. 启动本地或 Docker 演示环境。
2. 使用 admin 账号登录 Web 管理端。
3. 进入 `/admin/api-docs` 接口文档页。
4. 点击页面右上角【Swagger UI】按钮。
5. 观察新打开页面或跳转目标。

# 期望结果

- 点击【Swagger UI】后应进入后端 Swagger UI 页面。
- 本地默认后端 Swagger UI 地址应为 `http://localhost:8000/docs`，或由 Web 代理正确转发到后端 `/docs`。
- Swagger UI 页面应保留当前环境的 Try It Out 策略：开发/演示环境允许调试，生产环境只读或禁用调试。

# 实际结果

- 点击【Swagger UI】后进入 `localhost:3000/`。
- 用户无法从接口文档页直接打开后端 Swagger UI。
- 接口文档页显示的 Swagger 入口与实际行为不一致。

# 影响范围

- 影响页面：Web 管理端 `/admin/api-docs`。
- 影响角色：仅 `admin`，因为接口文档页为管理员可见。
- 影响能力：`REQ-0022-admin-api-docs-menu` 中的 Swagger UI 入口。
- 不影响后端 Swagger UI 本身、业务 API、数据库、媒体上传和 Orval 生成客户端。

# 严重等级说明

严重等级为 `high`。

理由：

- 该入口是接口文档页的核心操作之一，点击后进入错误页面，属于明确的交互阻断。
- 缺陷影响管理员查看运行时接口详情与 Swagger 调试入口的可达性。
- 该问题不阻断核心业务数据维护和前后端接口调用，因此未提升为 `critical` 或 `blocker`。

# 初步探索结论

该问题可稳定复现。当前 Web 页面按钮使用相对链接 `/docs`，在 Web 运行于 `localhost:3000` 时会打开 Web 服务自身的 `/docs`。本地 Vite 与 Docker Nginx 当前均未代理 `/docs` 到后端，因此 Web SPA 回退后会进入首页。

建议后续在 `/bug-complete` 中补充 root-cause、workaround 与验收标准，并通过 `fix-api-docs-swagger-ui-link-wrong` 类 OpenSpec Change 进入修复。
