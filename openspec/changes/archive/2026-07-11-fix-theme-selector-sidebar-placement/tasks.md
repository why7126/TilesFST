## 1. Implementation

- [x] 1.1 Locate the current Web admin theme selector rendering path in AdminLayout/theme feature code.
- [x] 1.2 Move the selector into the left sidebar directly above the bottom user avatar/account block.
- [x] 1.3 Remove the selector from the page top-right content/header area on AdminLayout pages.
- [x] 1.4 Preserve existing theme options, immediate switching, local persistence, and account-level persistence behavior.
- [x] 1.5 Ensure expanded and collapsed sidebar states do not overlap navigation, avatar, username/email, user menu, or collapse controls.
- [x] 1.6 Use existing Design System semantic token classes/CSS variables and `cn()` or established project class merging patterns; do not add raw Hex colors.

## 2. Regression Tests

- [x] 2.1 Add/update Web tests verifying the theme selector appears in the sidebar.
- [x] 2.2 Add/update Web tests verifying the page top-right area no longer contains the theme selector.
- [x] 2.3 Add/update Web tests verifying selecting a theme still updates the active theme behavior.
- [x] 2.4 Add/update coverage for collapsed sidebar or narrow layout if the current component exposes that state.

## 3. Verification

- [x] 3.1 Run the focused Web test suite for AdminLayout/theme selector behavior.
- [x] 3.2 Run relevant lint/typecheck/test commands used by the Web project if touched files require them.
- [x] 3.3 Perform a desktop visual check around 1440px that the selector is above the user avatar and absent from the top-right area.
- [x] 3.4 Confirm no API, DB, Orval, Docker, Mini Program, or backend changes were introduced.

## 4. Traceability

- [x] 4.1 Update BUG-0064 trace during apply/archive workflow events.
- [x] 4.2 Record screenshots or equivalent notes in the change trace if visual QA is performed.
- [x] 4.3 Consider `docs/knowledge-base/incidents/` only if implementation reveals a reusable shell-layout failure pattern; otherwise mark N/A.
