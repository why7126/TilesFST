---
change_id: fix-api-docs-swagger-ui-link-wrong
type: fix
status: applied
created_at: 2026-07-01 14:15:14
updated_at: 2026-07-01 20:03:09
related_bug: BUG-0051-api-docs-swagger-ui-link-wrong
related_requirement: REQ-0022-admin-api-docs-menu
sprint: sprint-004
---

# Trace

## Source

- BUG: `issues/bugs/archive/BUG-0051-api-docs-swagger-ui-link-wrong/`
- Sprint: `iterations/change/sprint-004/`
- Fix direction: Web 层代理 Swagger

## Acceptance Mapping

| BUG AC | Change Coverage |
|---|---|
| AC-001 本地开发 Swagger UI 入口正确 | tasks 1.1, 1.2, 3.1, 4.1 |
| AC-002 Docker Web 端口访问 `/docs` 正确转发 | tasks 1.3, 3.3, 4.3 |
| AC-003 OpenAPI JSON 入口不回退 | tasks 1.4, 3.3 |
| AC-004 生产 Swagger 调试策略不回退 | tasks 2.1, 2.2 |
| AC-005 前端测试覆盖 Swagger 链接行为 | tasks 3.1, 3.2 |
| AC-006 代理配置回归 | tasks 1.2, 1.3, 1.4 |
| AC-007 权限与访问范围 | tasks 4.1, 4.4 |

## Verification

| 时间 | 项目 | 结果 |
|---|---|---|
| 2026-07-01 20:01:43 | `pnpm --dir src/web test src/pages/admin/ApiDocsPage.test.tsx` | 1 file / 4 tests passed |
| 2026-07-01 20:01:54 | `pnpm --dir src/web build` | passed；存在既有 lightningcss/Tailwind at-rule warning 与 chunk warning |
| 2026-07-01 20:02:xx | `docker compose build web` | passed；新 `nginx.conf` 已复制进镜像 |
| 2026-07-01 20:02:xx | `docker compose run --rm --no-deps web nginx -t` | passed |
| 2026-07-01 20:03:09 | 容器内 `GET /docs` | 返回 `TilesFST API - Swagger UI` HTML，不是 SPA 首页 |
| 2026-07-01 20:03:09 | 容器内 `GET /openapi.json` | 返回包含 `openapi`、`info`、`paths` 的 JSON |
| 2026-07-01 20:03:09 | 容器内 `GET /redoc` | 返回 `TilesFST API - ReDoc` HTML |
| 2026-07-01 20:03:xx | `APP_ENV=production ... allow_swagger_try_it_out()` | `False`，生产 Try It Out 保持禁用 |

## Knowledge Base Decision

本缺陷是开发/部署代理遗漏导致的单点回归，已通过 BUG 文档、OpenSpec design 和 sprint acceptance 沉淀；暂不新增 `docs/knowledge-base/incidents/`，后续若 Swagger/Web 代理类问题重复出现再提炼为 best practice。
