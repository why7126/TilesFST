## Readiness Report

- REQ: `REQ-0020-theme-comfort-refine`
- Status: approved
- Source directory: `issues/requirements/archive/REQ-0020-theme-comfort-refine/`
- Readiness: Ready
- Review artifact: `review.md`
- Expected Change ID: `update-theme-comfort-refine`
- Prototype: `prototype/web/theme-comfort-matrix.html`
- Knowledge base gate: Pass

## Impact Analysis

- Change type: feature / Design System refinement
- Impacted clients: Web admin, store-owner Web
- Not in scope: WeChat Mini Program, MinIO contract changes, SKU business API behavior changes beyond theme preference API.
- API impact: yes, current-user theme preference must be exposed and updatable.
- Database impact: yes, user-level theme mode persistence must be stored in SQLite and MySQL.
- Orval impact: yes, implementation must export OpenAPI and regenerate the Web client.
- Docker impact: no topology change; Docker Compose smoke verification is still recommended after implementation.

## D1 UI Strategy

Use a Design System token strategy. The prototype HTML is an acceptance matrix and visual target for theme comfort, not a production CSS port. Production code should define theme mode values through semantic tokens in `src/web/src/styles/globals.css` and `src/shared/design-system/tokens/`, then apply a stable runtime attribute or class such as `data-theme-mode`.

The theme switcher should update semantic tokens immediately without remounting page content. Components must continue to consume semantic classes such as `bg-page`, `text-primary`, `text-brand-gold`, and `border-border-default`; business components must not introduce raw Hex values.

## Theme Modes

- `system`: follows OS color preference or the product default mapping when OS preference is unavailable.
- `dark_flagship`: preserves the existing industrial stone flagship dark style and existing brand tone.
- `comfort_dark`: reduces pure-black pressure, lowers harsh contrast, and prioritizes long admin sessions.
- `light`: supports bright environments and users who prefer light UI.

Theme names shown to users should be Chinese labels: 系统默认、暗色旗舰、舒适暗色、浅色.

## Persistence Model

Theme preference must be persisted in two layers:

- Local persistence: an unauthenticated or pre-login preference should be stored locally and applied on first paint where feasible.
- Account-level persistence: authenticated users should read and update their preference through the backend so it survives device changes.

Conflict resolution between the two layers:

- Before login, local preference is authoritative.
- After successful login, account-level preference is authoritative when present.
- If account-level preference is absent or `system`, local `system` behavior remains valid.
- When the user changes theme while authenticated, update local state immediately and persist to backend; failed backend persistence must show a recoverable error without losing the local visual selection.

## API And Database Design

Use the existing authentication boundary. `GET /api/v1/auth/me` should include `theme_mode`, and a new authenticated update endpoint should allow the current user to set `theme_mode` to one of `system`, `dark_flagship`, `comfort_dark`, or `light`.

The `users` table should persist the account-level preference as a non-sensitive field with default `system`. SQLite schema, migration logic, and MySQL documentation must remain aligned.

Invalid theme mode values should return HTTP 400 with the unified error envelope. Missing, invalid, expired, disabled, or role-forbidden token cases must follow the existing auth error behavior.

## Acceptance Matrix

The first implementation acceptance pass must cover:

- Login page: background, material composition, form controls, validation/error state, language controls, and pre-login theme selection.
- Tile SKU list page: page hero, metrics, filters, table, sticky action column, pagination, and fixed toast without layout shift.
- Tile SKU form page/state: labels, inputs, validation errors, action footer, and dirty state across themes.
- Tile SKU modal: modal width, scroll behavior, confirm modal reuse, and media upload states.
- `/design-system`: theme switcher, token preview, buttons, inputs, tables, dialogs, cards, toast, and tile SKU examples.
- Store-owner Web: non-brand-display catalog/detail/inquiry surfaces support comfortable themes; brand display pages may remain dark flagship.

## Conflict Resolution

Priority order for UI conflicts:

1. HTML prototype in `issues/requirements/archive/REQ-0020-theme-comfort-refine/prototype/web/`
2. REQ context documents and product decisions
3. Acceptance criteria
4. `rules/ui-design.md`
5. Archived/current OpenSpec specs

Known conflicts and resolutions:

- Existing Design System specs hard-code the current dark background and brand gold values. Those concrete values remain valid for `dark_flagship`; new implementations must route business UI through semantic tokens so `comfort_dark` and `light` can vary safely.
- Existing login-page CSS Port requirements remain valid for layout and brand composition. Theme implementation must not replace that layout strategy, only make its token values theme-aware.
- Existing admin list consistency requirements remain valid. Theme work must reuse `AdminListPage` or equivalent templates instead of duplicating list skeletons.
- Existing SKU media upload requirement names the terminal status `uploaded`; REQ-0020 prototype uses comfort-matrix wording. Treat `uploaded` and user-facing “完成/已上传” as equivalent terminal success states.
- Existing Web specs sometimes say a focused admin fix does not affect the store-owner Web. REQ-0020 intentionally adds store-owner Web theme support outside brand display pages; this is a new cross-surface requirement, not a regression in the older fix scope.

## Testing Strategy

- Backend pytest: theme mode persistence, `/auth/me` response, update endpoint success and invalid-mode errors, disabled/invalid token behavior.
- Database tests: SQLite schema/migration and MySQL schema documentation/checks include the theme preference field and default.
- Frontend Vitest: theme reducer/provider behavior, local persistence, account-level merge, API failure recovery, and semantic class usage for representative components.
- Web integration/E2E or focused manual acceptance: login, `/admin/tile-skus`, SKU modal upload states, `/design-system`, and store-owner Web catalog pages in all four theme modes.
- Governance: OpenAPI export, Orval generation, API docs index update, and no raw Hex in business UI.

## Knowledge Base References

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-form-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
- `docs/knowledge-base/retrospectives/sprint-005-retrospective.md`
