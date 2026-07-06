---
created_at: 2026-07-05 07:55:25
updated_at: 2026-07-05 07:55:25
---

# Design: update-api-docs-swagger-policy-checklist

## Context

`REQ-0030-api-docs-swagger-policy-checklist` 已通过评审并纳入 `sprint-005`。需求来源包括：

- Sprint 004 复盘行动项 A-006：Swagger / docs 入口 design MUST 声明 dev / Docker / production 代理路径和生产 `Try It Out` 策略。
- `BUG-0051-api-docs-swagger-ui-link-wrong`：Web 层未代理 `/docs` 导致 Swagger 入口落入 Web 首页。
- 已归档能力：`REQ-0022-admin-api-docs-menu` 与 `REQ-0023-api-docs-swagger-detail-link`。

现有正式 spec 已覆盖实际行为，本 Change 的核心不是新增页面或接口，而是把“以后做 API docs refine 时必须检查什么”固化为 checklist 门禁。

## Readiness Report

| 项 | 结论 |
|---|---|
| REQ 状态 | `in_sprint`，允许 `/req-opsx` |
| Readiness | Ready |
| 原型 | 无；本需求不新增 UI，不需要 prototype |
| 父需求 | `REQ-0022-admin-api-docs-menu` |
| 关联 BUG | `BUG-0051-api-docs-swagger-ui-link-wrong` |
| Sprint | `sprint-005` |

## Conflict Report

- 无 prototype，因此不存在 HTML / PNG / acceptance 优先级冲突。
- 不修改 `/admin/api-docs` 可见 UI，因此不触发 Design System 新组件或视觉验收。
- 现有 specs 已有 Swagger 行为要求；本 Change 仅新增“后续变更 checklist 化”要求，避免与已归档行为重复建模。

## Checklist Strategy

后续任何 API docs refine、接口文档页模板化、Swagger 入口调整、Web 代理调整、生产部署文档调整，design / acceptance / trace MUST 明确以下项：

| 类别 | 固定检查项 |
|---|---|
| 同源入口 | Swagger 主入口使用 `/docs` 或经 design 说明的等价同源 Web 路径；不得硬编码 `localhost:8000`、`backend:8000` 或内部服务名 |
| 行级深链 | 仅 `included_in_openapi=true` 且存在可用 `operation_id` 的路由可跳转；deep link 使用同源 `/docs#/{tag}/{operationId}` 或等价编码路径 |
| 不可跳转路由 | 非 OpenAPI 路由或缺失 `operation_id` 的路由保持可见但不可点击，不跳到通用 `/docs` |
| 代理路径 | 检查 `/docs`、`/redoc`、`/openapi.json` 与 Swagger UI 所需静态资源或后端文档资源路径 |
| 环境矩阵 | 记录 Vite dev proxy、Docker Web Nginx、生产反向代理或生产等价 N/A 原因 |
| 生产门禁 | 生产文档 MAY 可见，但 `Try It Out` MUST 禁用、隐藏或等价只读，且由后端环境策略兜底 |
| 安全边界 | 链接、hash、query、localStorage 新键、页面文案和验收记录不得包含 Bearer Token、JWT Secret、数据库 DSN、MinIO 凭据或真实环境变量值 |
| 文档同步 | 明确是否同步 `docs/03-api-index.md` 与 `docs/standards/api-governance.md`；不同步时在 trace 说明原因 |
| 验证记录 | 至少记录本地、Docker、生产等价策略验证；无法自动化时标注人工 smoke |

## Impact Matrix

| 维度 | 影响 |
|---|---|
| 后端 API | 不新增或修改业务 API；不改变请求、响应或错误码 |
| Web 管理端 | 本 Change 不改页面；后续页面文案变更仍需遵守 Design System |
| 店主 Web / 小程序 | 无影响 |
| 数据库 | 无 schema 或数据迁移影响 |
| MinIO / 媒体 | 无影响 |
| Orval | 本 Change 不需要运行；后续 API contract 变化才需要 |
| Docker Compose | 本 Change 不改配置；后续代理配置变更必须验证 |

## Documentation Placement

本 Change 的正式事实源落在 OpenSpec delta specs。后续 apply 阶段应评估并同步：

- `docs/03-api-index.md`：补充管理端接口文档页、Swagger 同源入口、生产只读策略说明。
- `docs/standards/api-governance.md`：补充 OpenAPI / Swagger / Orval 治理 checklist。
- `issues/requirements/review/REQ-0030-api-docs-swagger-policy-checklist/trace.md`：记录本 Change 与 Sprint 004 A-006 的闭环。

## Verification Plan

- `openspec validate update-api-docs-swagger-policy-checklist --strict`
- `python scripts/validate-directory-structure.py`
- 后续 apply 若只更新文档/spec：记录无需 Orval、无需数据库迁移、无需 Docker Compose。
- 后续 apply 若修改 `src/web/vite.config.ts`、`src/web/nginx.conf` 或生产部署文档：补充 `/docs`、`/redoc`、`/openapi.json` 的本地/Docker/生产等价 smoke。
