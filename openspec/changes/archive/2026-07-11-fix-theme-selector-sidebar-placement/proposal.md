## Why

BUG-0064-theme-selector-sidebar-placement has been approved because the Web admin theme selector is currently rendered in the page top-right content area, while the expected management shell layout places global user preference controls in the left sidebar above the bottom user avatar/account block.

The current placement mixes a cross-page theme preference with page-level top actions and exposes the same layout mismatch across admin pages. The theme switching capability itself remains useful; this fix corrects its shell placement and preserves existing theme behavior.

## What Changes

- Move the Web admin 「界面主题」 selector from the page top-right content area into the AdminLayout sidebar.
- Place the selector immediately above the bottom user avatar/account block.
- Ensure the top-right content/header area no longer renders the theme selector on AdminLayout pages.
- Preserve existing theme mode selection, local/account persistence behavior, and route/page state during switching.
- Add regression coverage for sidebar placement, top-right removal, and theme switching behavior.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `web-client`: tighten AdminLayout theme selector placement and regression requirements.

## Impact

- Web: AdminLayout/sidebar and related theme selector tests.
- API: no default API contract change.
- Database: no schema change.
- Orval/OpenAPI: no regeneration expected unless implementation discovers a contract issue outside this fix scope.
- Mini Program: no impact.
- Docker Compose: no topology change; Web verification is sufficient unless implementation scope expands.

## Rollback Plan

If the sidebar placement causes a layout regression, revert the AdminLayout/theme selector UI changes and associated tests from this change while keeping the existing theme preference contract intact. Because the default scope is Web-only layout work, rollback should not require database migration rollback, Orval regeneration, or backend API changes.
