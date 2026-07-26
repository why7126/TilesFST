## 1. Shared Foundation Components

- [x] 1.1 Choose the final component location under `src/web/src/shared/ui/` or an admin-specific shared layer and record the rationale in implementation notes.
- [x] 1.2 Implement `MetricCard` with `label`, `value`, `description`, placeholder/loading behavior, danger description support, `cn()` class merging, and stable `.metric-card`, `.metric-label`, `.metric-value`, `.metric-desc` DOM classes.
- [x] 1.3 Implement `MetricCardGrid` or an equivalent container supporting 2, 3, and 4 card layouts, `aria-label`, and stable `.summary-grid` output.
- [x] 1.4 Ensure new Web UI styles use semantic token classes, CSS variables, or existing admin classes without adding raw Hex or token-equivalent hardcoded `rgba(...)` values.

## 2. Pagination Window

- [x] 2.1 Move or expose `getPaginationWindow` from a shared Web/admin utility layer while keeping old imports compatible until migrated.
- [x] 2.2 Preserve the default maximum of 5 visible page numbers and support custom `maxVisible` when valid.
- [x] 2.3 Add defensive handling for `currentPage < 1`, `currentPage > totalPages`, `totalPages < 1`, and `maxVisible < 1`.
- [x] 2.4 Keep admin pagination presentation aligned to `.page-summary`, `.page-right`, `.page-buttons`, and `.page-size-wrap`.

## 3. Design System Preview

- [x] 3.1 Add `/design-system` or equivalent admin design acceptance examples for normal, empty/loading, and danger metric cards.
- [x] 3.2 Add examples for 2, 3, and 4 card `MetricCardGrid` layouts.
- [x] 3.3 Add pagination-window boundary examples for first page, centered page, and final page.

## 4. First Batch Page Adoption

- [x] 4.1 Select 2 to 3 first-batch pages from `TileSkuManagementPage`, `LogAuditPage`, `ApiDocsPage`, and `BrandManagementPage`.
- [x] 4.2 Replace first-batch metric summary DOM with shared foundation components without changing filtering, pagination state, empty state, permissions, or data behavior.
- [x] 4.3 Migrate first-batch pagination imports to the shared pagination-window helper and keep the admin pagination DOM contract.
- [x] 4.4 Record pages not included in the first batch as follow-up rollout items in trace or implementation notes.

## 5. Tests And Validation

- [x] 5.1 Add `MetricCard` / `MetricCardGrid` render tests for text content and stable DOM classes.
- [x] 5.2 Migrate or extend pagination-window unit tests for single page, full window, beginning boundary, ending boundary, centered page, and invalid input.
- [x] 5.3 Add or update first-batch page structure tests for `.summary-grid`, `.metric-card`, `.page-summary`, `.page-right`, `.page-buttons`, and `.page-size-wrap`.
- [x] 5.4 Run focused Vitest tests for changed Web components, utilities, design-system preview, and first-batch pages.
- [x] 5.5 Run Design System validation or an equivalent check for raw Hex / unauthorized arbitrary color regressions.
