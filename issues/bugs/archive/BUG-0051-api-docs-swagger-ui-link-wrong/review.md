---
bug_id: BUG-0051-api-docs-swagger-ui-link-wrong
title: 接口文档页 Swagger UI 入口跳转到 Web 首页 - 缺陷评审
severity: high
status: approved
owner: product
reviewed_at: 2026-07-01 14:02:05
review_result: approved
created_at: 2026-07-01 14:02:05
updated_at: 2026-07-01 14:02:05
related_requirement: REQ-0022-admin-api-docs-menu
related_change:
---

# 缺陷评审

## 评审结论

评审通过，确认修复。

`BUG-0051-api-docs-swagger-ui-link-wrong` 属于 `REQ-0022-admin-api-docs-menu` 已交付能力中的入口跳转缺陷。接口文档页右上角【Swagger UI】应进入后端 Swagger UI，但当前相对路径 `/docs` 在 Web Origin 下被 Web 服务处理，最终进入 Web 首页。

## 评审清单

- [x] 可复现或根因充分
- [x] 严重等级合理
- [x] 回归验收明确
- [x] 是否需 hotfix 路径

## 严重等级确认

严重等级维持 `high`。

理由：

- Swagger UI 是接口文档页的核心入口之一，点击后进入错误页面，属于明确交互阻断。
- 问题影响管理员查看后端运行时接口详情与调试入口。
- 问题不阻断核心业务维护、数据写入或用户登录，因此不升级为 `critical` / `blocker`。

## 修复策略确认

采用 **Web 层代理 Swagger**：

- Vite dev proxy MUST 覆盖 Swagger 相关路径。
- Docker Nginx MUST 覆盖 Swagger 相关路径。
- 保持管理端页面 `href="/docs"` 或等价 Web Origin 路径可用。
- 不通过硬编码后端宿主机端口解决。
- 生产环境 MUST 继续隐藏或禁用 Swagger `Try It Out`，不得放开生产在线调试能力。

## Hotfix 判断

不走 hotfix。

理由：

- 该缺陷影响接口文档入口，但不影响业务 API 实际运行。
- 已有临时规避方案：直接访问后端 `http://localhost:8000/docs` 或部署环境实际后端地址。
- 可进入常规 `fix-*` OpenSpec Change 修复。

## 后续动作

1. 执行 `/bug-opsx BUG-0051-api-docs-swagger-ui-link-wrong` 创建 `fix-api-docs-swagger-ui-link-wrong`。
2. 评估是否正式纳入 `sprint-004`；纳入前需通过 `/sprint-propose` 写入正式范围。
3. 修复后按 `acceptance.md` 验证本地开发、Docker Web、OpenAPI JSON、生产只读策略和权限边界。
