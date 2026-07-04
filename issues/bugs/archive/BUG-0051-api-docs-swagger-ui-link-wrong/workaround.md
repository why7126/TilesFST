---
bug_id: BUG-0051-api-docs-swagger-ui-link-wrong
title: 接口文档页 Swagger UI 入口跳转到 Web 首页 - 临时规避
severity: high
status: pending_review
owner: product
created_at: 2026-07-01 09:27:51
updated_at: 2026-07-01 09:27:51
related_requirement: REQ-0022-admin-api-docs-menu
---

# 临时规避方案

## 管理员操作规避

在修复前，管理员需要手动打开后端 Swagger UI 地址：

```text
http://localhost:8000/docs
```

如果本地 Docker 或部署环境修改了宿主机后端端口，应使用实际 `HOST_PORT_BACKEND`：

```text
http://<host>:<HOST_PORT_BACKEND>/docs
```

## Docker / 演示环境规避

如果只通过 Web 端口访问系统，暂时不要依赖接口文档页右上角【Swagger UI】按钮。可从部署文档或 README 中的“Backend API Docs”地址进入后端 Swagger。

## 生产环境注意事项

生产环境中即使能打开 Swagger UI，也必须保持只读或禁用 Try It Out。不得为了规避该 BUG 临时打开生产在线调试能力。

## 风险

该规避方案需要用户知道后端端口和部署地址，无法满足接口文档页“一键进入 Swagger UI”的交付预期。因此该 BUG 仍需进入后续修复流程。
