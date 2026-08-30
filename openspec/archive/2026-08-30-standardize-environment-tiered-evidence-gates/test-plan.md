---
created_at: 2026-08-30 12:26:56
updated_at: 2026-08-30 12:26:56
---

# 测试计划

## 校验范围

- OpenSpec delta spec 结构与语言校验。
- 目录结构治理校验。
- Agent 上下文预算治理校验。
- 本次触达长期文档的表达卫生校验。
- 聚焦 diff 复核未修改 `src/` 业务代码。

## 业务测试

本变更仅修改治理规范、技能说明和文档，不改变运行时代码、API、DB、Web、小程序或管理端行为，因此不运行 pytest、Vitest、Orval 或 Docker Compose 业务验证。
