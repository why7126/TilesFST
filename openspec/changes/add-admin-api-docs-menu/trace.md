---
change_id: add-admin-api-docs-menu
requirement_id: REQ-0022-admin-api-docs-menu
type: add
status: proposed
created_at: 2026-07-01 00:40:14
updated_at: 2026-07-01 00:40:14
iteration: sprint-004
---

# Change Trace

## Source Requirement

| 字段 | 值 |
|---|---|
| REQ | `issues/requirements/review/REQ-0022-admin-api-docs-menu/` |
| 状态 | `in_sprint` |
| 优先级 | P1 |
| Sprint | sprint-004 |

## Requirement Readiness Report

| 检查项 | 结果 | 说明 |
|---|---|---|
| `requirement.md` | Ready | 管理端接口文档菜单与在线调试 PRD 已生成 |
| `user-stories.md` | Ready | 覆盖管理员、运营权限、Orval、Swagger 生产策略 |
| `business-flow.md` | Ready | 覆盖访问、接口目录、Orval 映射、Swagger 流程 |
| `acceptance.md` | Ready | AC-001～AC-037 与 AC-XCUT-001～008 已定义 |
| `trace.md` | Ready | 状态 `in_sprint`，已纳入 sprint-004 |
| `prototype/web/api-docs.html` | Ready | HTML 原型可用 |
| `prototype/web/api-docs.png` | Partially Ready | PNG Golden 待导出，不阻塞 req-opsx |
| `prototype/web/api-docs-context.md` | Ready | 原型上下文与优先级已说明 |

## Impact

```yaml
impact:
  backend: possible
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: possible
capabilities:
  new:
    - admin-api-docs
  modified:
    - web-client
    - api-governance
    - testing
```

## Conflict Report

Priority:

```text
1. prototype/web/api-docs.html
2. prototype/web/api-docs.png（Golden Reference，待导出）
3. prototype/web/api-docs-context.md
4. issues/requirements/review/REQ-0022-admin-api-docs-menu/acceptance.md
5. rules/ui-design.md
6. docs/knowledge-base/best-practices/admin-list-page-consistency.md
7. docs/knowledge-base/best-practices/admin-form-page-consistency.md
8. openspec/specs
```

- HTML uses raw CSS variables and demo colors; implementation must translate them to Design System semantic token classes.
- PNG is pending; HTML/context remain authoritative until exported.
- Swagger UI dark-theme fidelity may differ from prototype; implementation must keep a bounded panel/link that does not break layout.
- OpenAPI alone may omit non-`/api/v1` routes; route inventory must explicitly include `/health`, `/media/{object_key:path}`, and schema-excluded app routes.

## UI Strategy

`tailwind-ds + prototype-led`

Use the HTML prototype for hierarchy and page composition, while implementing with existing Admin Shell, route guards, semantic token classes, admin table/filter patterns, fixed feedback, and Design System modal patterns.

## Prototype Trace Checklist

| 检查项 | HTML | PNG | Context | Change |
|---|---|---|---|---|
| Admin Shell + SYSTEM 接口文档菜单 | yes | pending | yes | `add-admin-api-docs-menu` |
| page-hero + 环境策略提示 | yes | pending | yes | `add-admin-api-docs-menu` |
| summary-strip 指标 | yes | pending | yes | `add-admin-api-docs-menu` |
| filter-bar + api-route-table | yes | pending | yes | `add-admin-api-docs-menu` |
| Swagger panel / link | yes | pending | yes | `add-admin-api-docs-menu` |
| Orval 方法名状态 | yes | pending | yes | `add-admin-api-docs-menu` |

## Workflow

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-07-01 00:40:14 | `/req-opsx REQ-0022` | 创建 proposal/design/specs/tasks/trace |
