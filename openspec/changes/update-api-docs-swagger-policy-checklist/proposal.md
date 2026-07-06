---
created_at: 2026-07-05 07:55:25
updated_at: 2026-07-05 07:55:25
---

# Change: update-api-docs-swagger-policy-checklist

## Why

REQ-0030 源自 Sprint 004 复盘 A-006 与 BUG-0051：接口文档页已有 Swagger 入口和生产只读策略，但后续 API docs refine 或模板化时缺少固定 checklist，容易再次遗漏 Web 代理路径、SPA fallback、生产 `Try It Out` 门禁和敏感信息边界。

本 Change 将这些经验沉淀为 OpenSpec 层面的治理约束，确保后续接口文档页设计、验收、文档同步和测试记录都能复用同一套门禁。

## What Changes

- 更新接口文档页能力规范，要求后续 API docs refine、Swagger 入口调整或接口文档页模板化时必须包含“Swagger Web 代理与生产 Try It Out 策略”检查章节。
- 更新 Web 客户端接口文档入口规范，要求同源 `/docs`、行级 deep link、不可跳转路由、安全新上下文与生产只读策略在后续变更中保持 checklist 化验收。
- 更新部署能力规范，要求 dev / Docker / production 等价路径明确记录 `/docs`、`/redoc`、`/openapi.json` 代理策略和 SPA fallback 边界。
- 更新测试能力规范，要求后续实现或文档变更记录本地、Docker、生产等价验证；无法自动化时必须注明人工 smoke 方式。
- 不新增业务 API、不改变请求/响应/错误码、不修改数据库、不新增 Web 可见功能。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `admin-api-docs`: 增加接口文档页模板 checklist 的固定触发场景和内容。
- `web-client`: 增加 Swagger 同源入口、行级 deep link 与生产只读策略的模板化验收约束。
- `deployment`: 增加 Web 层 Swagger 代理策略的设计/验收 checklist 约束。
- `testing`: 增加 Swagger 代理与生产 `Try It Out` 策略的测试/验收记录门禁。

## Impact

- 影响范围：OpenSpec specs、后续 API docs design / acceptance / trace / docs 同步流程。
- 可能影响后续文档：`docs/03-api-index.md`、`docs/standards/api-governance.md`、接口文档页模板说明。
- 不影响后端接口契约、Orval 生成物、SQLite schema、MinIO、店主 Web、小程序或管理端页面功能。
- 本 Change 本身不要求运行 Docker Compose；后续若修改 Web 代理或部署配置，必须补充 Docker Compose 或生产等价 smoke 记录。

## Rollback Plan

如 checklist 约束与后续 API docs 工作流冲突，可回滚本 Change 的 delta spec，并在 REQ-0030 trace 中标记为 rejected 或 superseded。回滚后，Swagger 代理与生产 `Try It Out` 策略仍需依赖现有 `admin-api-docs`、`web-client`、`deployment` 与 `testing` 行为规范人工检查。
