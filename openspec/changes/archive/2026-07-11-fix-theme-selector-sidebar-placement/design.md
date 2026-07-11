## Context

`REQ-0020-theme-comfort-refine` introduced theme switching for Web/admin surfaces. BUG-0064 narrows a placement defect in that feature: the selector is visible in the top-right page content area instead of the sidebar area directly above the user avatar/account block.

The selector is a global preference control. It belongs with shell-level navigation, identity, and preference affordances, not with page-specific actions.

## Root Cause

- The theme selector was integrated as a visible global control, but its AdminLayout ownership was not constrained to the sidebar.
- The related acceptance criteria required a clear admin theme entry but did not specify the exact sidebar placement above the user avatar.
- The top-right area was treated as a convenient shell/control area even though it should remain available for page-level actions.

## Fix Strategy

1. Locate the Web admin theme selector component and its AdminLayout placement.
2. Move the selector into the sidebar bottom region above the user profile/avatar/account block.
3. Remove the top-right/header rendering of the same selector on AdminLayout pages.
4. Preserve existing theme mode options and persistence behavior.
5. Ensure expanded and collapsed sidebar states remain stable:
   - expanded: label, icon, select trigger, and selected value are readable;
   - collapsed: selector either uses an icon/compact trigger or an equivalent non-overlapping fallback.
6. Avoid raw Hex colors and use existing semantic token classes, CSS variables, `cn()`, or established admin/sidebar classes.

## Testing

- Add or update AdminLayout/theme selector tests to assert the selector is rendered in the sidebar near the user block.
- Assert the page top-right content/header no longer contains the theme selector.
- Assert selecting a theme still updates the active theme behavior according to existing theme logic.
- Include a visual/manual check at desktop width around 1440px.
- Include a collapsed-sidebar or narrow-width check if current layout supports it.

## Non-Goals

- Do not change backend theme preference API by default.
- Do not change SQLite/MySQL schema.
- Do not regenerate Orval unless implementation scope expands to an API contract issue.
- Do not redesign the entire sidebar or user menu.
- Do not change Mini Program behavior.

## Risks

| Risk | Mitigation |
|---|---|
| Sidebar bottom area becomes crowded | Use compact spacing and verify no overlap with avatar, email, user menu trigger, or collapse control |
| Collapsed sidebar clips text | Provide compact/icon-only treatment or hide nonessential text while preserving access |
| Theme selector duplicate remains | Test top-right removal and sidebar presence |
| Theme behavior regresses | Reuse existing theme state/persistence code and add behavior regression coverage |
