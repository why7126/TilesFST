## Why

REQ-0020 has been approved because management-side users report the current dark flagship visual style is too heavy for long operating sessions. The product decision is to keep the flagship dark brand expression where it matters, while adding theme switching and comfortable alternatives for admin workflows and store-owner Web pages.

## What Changes

- Add four supported theme modes: `system`, `dark_flagship`, `comfort_dark`, and `light`.
- Add a theme switcher for Web admin and store-owner Web surfaces, with both local persistence and account-level persistence.
- Keep brand display pages eligible to remain in the dark flagship style, while allowing other store-owner Web pages to use comfortable themes.
- Extend the first acceptance matrix to cover login, a list page, a form page, a modal, `/design-system`, and tile SKU components.
- Add account-level theme preference API and database persistence so authenticated users can keep preference across devices.
- Require OpenAPI, Orval, tests, and documentation updates for the new API contract.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `design-system`: define multi-theme semantic token behavior and `/design-system` theme preview requirements.
- `web-client`: add Web theme switching, local persistence, admin acceptance matrix, and store-owner Web theme boundary requirements.
- `auth`: expose and update current-user theme preference through authenticated API contract.
- `database`: persist user theme preference consistently in SQLite and MySQL schemas.

## Impact

- Web: admin login, AdminLayout/theme switcher, `/admin/tile-skus`, SKU form/modal/media upload state, `/design-system`, and store-owner Web catalog pages.
- API: authenticated current-user theme preference contract changes; OpenAPI and Orval regeneration are required during implementation.
- Database: user-level theme preference persistence is required for SQLite and MySQL parity.
- Mini Program: no implementation in this change unless a later requirement explicitly adds it.
- Docker Compose: no service topology change expected, but implementation should verify Web and backend run together after API/client regeneration.
