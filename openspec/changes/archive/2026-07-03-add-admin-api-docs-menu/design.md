## Context

REQ-0022 adds an admin-only API documentation surface inside the Web admin app. Existing documentation is split between `/docs`, `/openapi.json`, `docs/03-api-index.md`, and Orval output at `src/web/src/shared/api/generated.ts`; none of these provide an admin-facing route inventory that includes schema-excluded or non-`/api/v1` routes.

The change is cross-cutting: it touches Web admin navigation and routing, route inventory/API governance, Swagger production policy, Orval method mapping, documentation, and tests. No database or storage schema changes are required.

## Goals / Non-Goals

**Goals:**

- Add `/admin/api-docs` under SYSTEM, immediately below "系统设置".
- Restrict the page and any backend aggregation endpoint to `admin`.
- Show all system routes, including `/api/v1/*`, `/health`, `/media/{object_key:path}`, and other FastAPI app routes.
- Show OpenAPI inclusion status and Orval generated method names.
- Allow Swagger `Try It Out` in local/development/demo while hiding or disabling it in production.
- Preserve Admin Shell, Design System semantic token usage, and admin list/table consistency gates.

**Non-Goals:**

- No public API documentation site for shop owner Web or miniapp users.
- No API editing, mock data, route enable/disable, or permission configuration.
- No production Swagger online debugging.
- No management UI for changing OpenAPI, Orval config, or backend route definitions.
- No database migration.

## Decisions

### D1. UI Strategy: prototype-led Tailwind DS

Implementation SHALL use the existing Admin Shell, route guard, sidebar data, semantic token classes, and admin list/table styles. The HTML prototype defines the layout and information hierarchy, but the implementation MUST compose with existing design-system patterns rather than copying prototype CSS wholesale.

Alternatives considered:

- CSS port from `prototype/web/api-docs.html`: higher visual fidelity but repeats prior Sprint 002/003 list/form layout issues.
- New marketing-style documentation page: rejected because this is an operational admin page.

### D2. Conflict Resolution Priority

For UI and behavior conflicts, implementation SHALL use this priority:

1. `issues/requirements/archive/REQ-0022-admin-api-docs-menu/prototype/web/api-docs.html`
2. `issues/requirements/archive/REQ-0022-admin-api-docs-menu/prototype/web/api-docs.png` when exported
3. `issues/requirements/archive/REQ-0022-admin-api-docs-menu/prototype/web/api-docs-context.md`
4. `issues/requirements/archive/REQ-0022-admin-api-docs-menu/acceptance.md`
5. `rules/ui-design.md`
6. `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
7. `docs/knowledge-base/best-practices/admin-form-page-consistency.md`
8. Existing `openspec/specs/*`

Conflict report:

- HTML prototype uses local CSS variables and fixed colors; implementation MUST translate these to semantic tokens and existing Tailwind classes.
- PNG Golden is pending; HTML/context are authoritative until PNG is exported.
- Swagger UI may not fully inherit the dark theme; implementation MUST place it in a bounded admin panel or use an external link while preserving layout.
- Acceptance requires "system all routes"; OpenAPI alone may omit `/health`, `/media/{object_key:path}`, or `include_in_schema=false` routes, so implementation MUST supplement route inventory.

### D3. Route Inventory Source

Implementation SHOULD add an admin-only aggregation endpoint, tentatively `GET /api/v1/admin/api-docs`, when client-side OpenAPI loading cannot fully represent non-schema routes or Orval mapping. The endpoint MUST be guarded by the same admin-only authorization used by user management/system settings admin-only actions.

The response SHOULD normalize route entries with:

- method
- path
- tag/module
- summary/description
- auth requirement
- included_in_openapi
- operation_id
- orval_method_name
- source

The implementation MAY compute Orval method names from OpenAPI `operationId` and/or parse the generated client as a build/runtime-safe static mapping. It MUST avoid exposing secrets or environment values.

### D4. Swagger Production Policy

Production SHALL show the API docs entry and route inventory but MUST hide or disable Swagger `Try It Out`. The implementation may use one or more of:

- Swagger UI parameter/config that disables supported submit actions.
- A read-only embedded viewer in production and direct Swagger link only in non-production.
- Backend or deployment-level docs configuration.

Regardless of implementation, tests or production-equivalent verification MUST prove that production does not permit `Try It Out`.

### D5. Documentation and Orval

If a backend aggregation endpoint is introduced, the change MUST update OpenAPI, run Orval, and update `docs/03-api-index.md`. If only client-side page logic is introduced, docs still MUST explain the `/admin/api-docs` page, route inventory scope, and production Swagger policy.

## Risks / Trade-offs

- [OpenAPI route omission] `/health`, `/media/{object_key:path}`, or `include_in_schema=false` routes may not appear in `/openapi.json` -> supplement from FastAPI route inventory and mark source/inclusion status.
- [Production accidental debugging] Swagger `Try It Out` could remain enabled in production -> add explicit production verification and UI state tests.
- [Orval drift] Displayed method names may drift from `generated.ts` -> derive mapping from OpenAPI operation IDs plus generated client output, and run Orval when API changes.
- [UI regression] A new admin table could repeat pagination/toast/layout bugs -> reuse admin list patterns and enforce knowledge-base cross-cutting acceptance.
- [Security exposure] Docs page could reveal secrets or sensitive deployment values -> whitelist route metadata only and never display raw environment variable values.

## Migration Plan

1. Add OpenSpec tasks and specs in this change.
2. Implement backend aggregation only if needed by `/opsx-apply`.
3. Implement Web admin route, sidebar item, page, filters, Orval mapping, and Swagger policy.
4. Update docs/OpenAPI/Orval if API surface changes.
5. Run backend pytest, frontend Vitest, Orval generation when applicable, and production-equivalent Swagger policy verification.

Rollback: remove the `/admin/api-docs` route/sidebar item and any aggregation endpoint; no database rollback is required.

## Open Questions

- Whether Orval method mapping should be computed entirely from OpenAPI `operationId` or parsed from `src/web/src/shared/api/generated.ts`.
- Whether production should embed a read-only Swagger panel or show a bounded external Swagger/OpenAPI link.
