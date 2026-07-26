## 1. Contract And Planning

- [x] 1.1 Confirm final endpoint naming for current-user theme preference and document it in API docs before implementation.
- [x] 1.2 Update `docs/03-api-index.md` and API governance notes for the new authenticated theme preference contract.
- [x] 1.3 Confirm no WeChat Mini Program implementation is included in this change.

## 2. Backend And Database

- [x] 2.1 Add user theme preference persistence to SQLite schema and migration logic.
- [x] 2.2 Update MySQL schema documentation/checks for parity with SQLite.
- [x] 2.3 Extend current-user auth schemas to include `theme_mode`.
- [x] 2.4 Add authenticated theme preference update endpoint using unified response and error envelopes.
- [x] 2.5 Add backend tests for success, invalid value, missing token, disabled user, and persistence behavior.

## 3. Web Theme Infrastructure

- [x] 3.1 Add Design System theme tokens for `system`, `dark_flagship`, `comfort_dark`, and `light`.
- [x] 3.2 Add a theme provider/switcher with local persistence and account-level synchronization.
- [x] 3.3 Regenerate OpenAPI and Orval client after backend contract changes.
- [x] 3.4 Ensure first-paint theme application avoids visible theme flash where feasible.

## 4. Admin And Store-owner Web Acceptance

- [x] 4.1 Update login page theme selection and post-login preference handoff.
- [x] 4.2 Validate `/admin/tile-skus` list modules across all theme modes.
- [x] 4.3 Validate tile SKU form states and SKU modal width/scroll/upload states across all theme modes.
- [x] 4.4 Update `/design-system` to expose theme switching, token previews, and tile SKU component examples.
- [x] 4.5 Add store-owner Web comfortable theme support outside brand display pages while allowing brand display pages to remain dark flagship.

## 5. Verification

- [x] 5.1 Run backend pytest for auth/database theme preference coverage.
- [x] 5.2 Run frontend unit tests for theme provider and representative components.
- [x] 5.3 Run raw Hex/design token checks for modified Web files.
- [x] 5.4 Run OpenAPI export and Orval generation checks.
- [x] 5.5 Run Docker Compose or equivalent Web/backend smoke verification if implementation changes both services.
- [x] 5.6 Capture acceptance evidence for login, list, form, modal, `/design-system`, and store-owner Web catalog surfaces.
