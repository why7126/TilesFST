---
requirement_id: REQ-0030-api-docs-swagger-policy-checklist
title: 接口文档页 Swagger 代理与生产调试策略 checklist
terminal: web-admin
version: v1
status: in_sprint
owner: product
source: capture.md
priority: P2
parent_requirement: REQ-0022-admin-api-docs-menu
created_at: 2026-07-04 22:13:25
updated_at: 2026-07-04 22:30:20
---

# REQ-0030 接口文档页 Swagger 代理与生产调试策略 checklist

## 1. 需求背景

`REQ-0022-admin-api-docs-menu` 已交付 Web 管理端 `/admin/api-docs` 页面，支持管理员查看系统接口目录、OpenAPI/Swagger/Orval 映射，并按环境控制 Swagger 在线调试策略。后续 `BUG-0051-api-docs-swagger-ui-link-wrong` 暴露出一个横切问题：接口文档页本身有 `/docs` 入口，但 Web 层没有在 Vite dev proxy 与 Docker Nginx 中完整代理 Swagger 相关路径，导致点击 Swagger UI 时进入 Web 首页。

该问题已经通过修复解决，但它不是单个链接文案问题，而是接口文档页模板缺少“跨服务文档入口与生产调试门禁”的固定 checklist。后续若继续做 API docs refine、接口文档页模板化或管理端文档类页面，很容易再次遗漏 Web 代理、生产只读策略、同源链接与回归测试。

本需求用于将 Swagger Web 代理与生产 `Try It Out` 策略沉淀为接口文档页模板 checklist，作为后续设计、实现、验收和回归测试的固定门禁。

## 2. 目标用户

| 角色 | 需求价值 |
|---|---|
| 产品 / 需求负责人 | 在 API docs refine 阶段明确必须检查的部署与安全边界，避免只描述页面功能 |
| 前端开发 | 在实现 `/admin/api-docs` 或同类文档入口时，有固定 checklist 检查同源链接、行级深链和代理路径 |
| 后端开发 | 保持 FastAPI Swagger 配置与 `APP_ENV` 调试策略一致，不因 Web 代理放开生产调试 |
| DevOps / 部署负责人 | 在 Vite、Docker Nginx、生产反代中同步确认 Swagger 文档路径不会落入 SPA fallback |
| QA / 验收人员 | 可按 checklist 验证 `/docs`、`/redoc`、`/openapi.json` 与生产只读策略 |

## 3. 范围

### 3.1 本期包含

- 在接口文档页相关 PRD、design 或模板 checklist 中补充 Swagger 文档入口检查项。
- checklist MUST 覆盖 Web 同源访问策略：
  - `/docs`；
  - `/redoc`；
  - `/openapi.json`；
  - Swagger UI 运行所需的静态资源或等价后端文档资源路径。
- checklist MUST 覆盖本地开发、Docker Compose、生产等价环境：
  - Vite dev proxy；
  - Docker Web Nginx；
  - 生产反向代理或生产部署说明。
- checklist MUST 明确生产环境 Swagger `Try It Out` 禁用或只读策略，且不得因 Web 层代理而放开生产在线调试。
- checklist MUST 要求 Swagger 入口使用同源 Web 路由，不在前端硬编码后端主机或端口。
- checklist SHOULD 覆盖行级 Swagger operationId 深链与不可跳转路由的禁用态。
- checklist SHOULD 说明需要同步的长期文档或知识库位置，例如 `docs/03-api-index.md`、`docs/standards/api-governance.md` 或接口文档页模板说明。
- checklist SHOULD 要求测试或验收记录覆盖 Web 代理 smoke、生产只读策略和 SPA fallback 不误接管 `/docs`。

### 3.2 本期不包含

- 不重新设计 `/admin/api-docs` 页面 UI。
- 不新增接口文档页的新业务功能、筛选项或表格字段。
- 不修改 FastAPI 业务接口请求、响应、错误码或数据库结构。
- 不要求生产环境允许 Swagger 在线调试。
- 不新增面向店主 Web、微信小程序或未登录用户的接口文档入口。
- 不引入自动注入 Bearer Token 到 Swagger UI 的机制。
- 不将本需求直接作为代码实现任务；后续必须经 `/req-complete`、评审与 `/req-opsx` 后进入 OpenSpec Change。

## 4. 功能要求

### FR-001 checklist 归属与触发场景

- MUST 将 Swagger 代理与生产调试策略作为接口文档页模板 checklist 的固定章节。
- MUST 在 API docs refine、接口文档页模板化、Swagger 入口调整、Web 代理调整、生产部署文档调整时触发该 checklist。
- SHOULD 在后续 OpenSpec design 中明确 checklist 的最终落点，避免分散在口头约定或一次性 trace 记录中。

### FR-002 Web 同源 Swagger 入口

- MUST 要求 Swagger 入口使用同源 Web 路径，例如 `/docs` 或等价同源代理路径。
- MUST 禁止前端硬编码后端宿主机、端口或内部服务名，例如 `localhost:8000`、`backend:8000`。
- MUST 要求 `/docs` 不被 React Router 或 Web SPA fallback 接管。
- SHOULD 要求行级 Swagger 查看链接使用同源 `/docs#/{tag}/{operationId}` 或经验证的等价 Swagger UI deep link。

### FR-003 代理路径检查

- MUST 在 checklist 中列出 Vite dev proxy 对 Swagger 相关路径的检查项。
- MUST 在 checklist 中列出 Docker Nginx 对 Swagger 相关路径的检查项。
- MUST 在 checklist 中列出生产反向代理或部署说明对 Swagger 相关路径的检查项。
- SHOULD 将 `/docs`、`/redoc`、`/openapi.json` 与 Swagger UI 依赖资源作为最小检查集合；若实现中使用不同路径，必须在 design 中记录替代路径与原因。

### FR-004 生产 Try It Out 策略

- MUST 明确非生产环境可以允许 Swagger 在线调试。
- MUST 明确生产环境文档可见但 `Try It Out` 必须禁用、隐藏或等价只读。
- MUST 要求后端 `swagger_ui_parameters.tryItOutEnabled=false` 或等价机制在生产环境生效。
- MUST 要求前端页面文案与后端实际策略一致，不展示“可调试”等误导性状态。
- MUST 禁止通过 Web 代理、前端参数或部署配置绕过生产只读策略。

### FR-005 安全与敏感信息边界

- MUST 保持 `/admin/api-docs` 仅管理员可访问的边界，不因 checklist 或文档入口调整放宽权限。
- MUST 禁止在 Swagger URL、hash、query、localStorage 新键或页面文案中注入 Bearer Token、数据库连接串、MinIO 凭据、JWT Secret 或真实环境变量值。
- MUST 在 checklist 中保留“生产不启用 Try It Out”的安全门禁。
- SHOULD 明确 Swagger UI 新窗口打开时使用安全属性，例如 `rel="noreferrer"` 或等价策略。

### FR-006 测试与验收记录

- MUST 要求后续实现或模板变更记录至少覆盖以下验证：
  - 本地 Web 访问 `/docs` 时进入后端 Swagger UI 或等价后端文档响应；
  - Docker Web 访问 `/docs` 时不会进入 Web 首页或 SPA fallback；
  - `/openapi.json` 可通过 Web 同源路径访问；
  - 生产等价环境中 `Try It Out` 禁用或只读；
  - 行级 Swagger 深链不向 URL 泄露 token 或敏感值。
- SHOULD 在前端测试、后端测试或部署 smoke 中选择合适组合；若无法自动化，必须在验收记录中说明人工验证方式。

### FR-007 文档同步

- SHOULD 在后续 OpenSpec 阶段评估是否同步 `docs/03-api-index.md` 的接口文档页说明。
- SHOULD 在后续 OpenSpec 阶段评估是否同步 `docs/standards/api-governance.md` 的 OpenAPI/Swagger/Orval 治理说明。
- SHOULD 将 Sprint 004 复盘中 “Swagger / docs 入口 design MUST 声明 dev / Docker / production 代理路径和 Try It Out 策略” 沉淀为长期可引用条目。

## 5. UI 约束

- 本需求不要求新增可见 UI，但若后续更新 `/admin/api-docs` 页面文案，MUST 继承现有管理端暗色旗舰风。
- 若页面展示当前环境调试策略，MUST 使用现有管理端状态 Badge、提示条或轻量文案，不新增独立视觉体系。
- 新增或调整 Web UI 代码时 MUST 使用 Design System semantic token class，不得新增裸 Hex 颜色。
- 生产环境文案建议表达为“生产只读”或“已禁用在线调试”；最终文案需在 `/req-complete` 或 OpenSpec design 中确认。

## 6. 关联需求与文档

| 关联项 | 关系 |
|---|---|
| `REQ-0022-admin-api-docs-menu` | 父需求；已提供接口文档页、Swagger 入口和生产调试策略 |
| `REQ-0023-api-docs-swagger-detail-link` | 相邻需求；已补充行级 Swagger operationId 深链 |
| `BUG-0051-api-docs-swagger-ui-link-wrong` | 经验来源；暴露 Web 代理未覆盖 `/docs` 导致进入 Web 首页 |
| `docs/03-api-index.md` | 长期接口索引；后续可同步接口文档页与 Swagger 策略说明 |
| `docs/standards/api-governance.md` | API 治理文档；后续可同步 Swagger/Orval checklist |
| `docs/knowledge-base/retrospectives/sprint-004-retrospective.md` | 复盘行动项来源，A-006 建议进入 `/req-capture` 或 API docs refine |
| `src/web/vite.config.ts` | 本地开发 Web 代理检查对象 |
| `src/web/nginx.conf` | Docker Web 代理检查对象 |
| `src/backend/app/main.py` | FastAPI Swagger 与 `Try It Out` 策略检查对象 |

## 7. 状态块

```yaml
status: in_sprint
readiness: Ready
next_step: /req-opsx REQ-0030-api-docs-swagger-policy-checklist
expected_openspec_change: update-api-docs-swagger-policy-checklist
needs_prototype: false
needs_api_change: false
needs_database_change: false
needs_orval: false
needs_docker_validation: likely
```

## 8. 待完善项

- `/req-review` 阶段确认是否批准进入 OpenSpec。
- OpenSpec 阶段确认 checklist 最终落点：接口文档页 design 模板、API governance 文档、知识库，或三者组合。
- OpenSpec 阶段确认是否仅更新文档和测试 checklist，还是需要同步补充现有测试用例。
