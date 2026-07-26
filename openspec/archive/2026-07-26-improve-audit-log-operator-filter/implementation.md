---
change_id: improve-audit-log-operator-filter
status: applied
created_at: 2026-07-25 14:05:27
updated_at: 2026-07-26 11:20:05
---

# Implementation Notes

## API / Contract

- Reused existing `GET /api/v1/admin/users?page=1&page_size=20&keyword=<query>` for operator candidates.
- Confirmed the users API is protected by `require_system_admin` and returns the option fields needed by the page: `id`, `display_name`, `username`, `role`, and `status`.
- Reused existing `GET /api/v1/admin/logs` `actor_user_id` filtering semantics.
- Added `actor_username` to `GET /api/v1/admin/logs` list/detail log item responses so the Web admin list can display the user account while preserving `actor_name` for detail contexts. No database or error-code changes were required.
- Disabled users remain visible through the existing users list API when no `status` filter is sent. Deleted historical users are not covered by a separate candidate source in this change; adding historical/deleted operator candidates would require a follow-up API decision.

## Web / UI

- Replaced the `/admin/logs` free-text User ID input with a searchable single-select operator dropdown.
- The selected option stores `user.id` and sends it as `actor_user_id`; the closed control displays `display_name || username` instead of a raw User ID.
- Candidate options show two lines only: account (`username`) first, display name second. Role and status are intentionally omitted from the dropdown.
- Candidate loading, empty, and failed states are displayed inside the dropdown. Candidate failures also use the fixed admin toast and do not block the log list or other filters.
- Clear and reset remove `actor_user_id`, reset the page to 1, and keep the rest of the log page interactions unchanged.
- The filter card establishes a higher local stacking context than the following table card, and the operator dropdown has a higher in-filter `z-index`, so expanded options are not covered by the log list below.
- The log detail drawer layer remains above the filter and dropdown layers, so opening a log detail is not obscured by the filter module.
- Filter order is `日志类型 / 时间范围 / 状态 / 结果 / 操作者 / Task Trace ID / 路径 / Request ID / 重置`.
- The time range filter uses fixed recent windows: 5m, 10m, 30m, 1h, 3h, 6h, 12h, 1d, 2d, 3d, and 7d. The previous `全部时间` option was removed.
- The generic text filter label was shortened to `路径 / Request ID`; `Task Trace ID` remains a dedicated exact-input field to avoid duplicate task trace wording in the filter module.
- The list `Task Trace` column now mirrors the `request_id` column density: one shortened ID plus one copy action in a single row, while detailed task status and span information remains in the detail drawer.
- The list operator column displays `actor_username` in one non-wrapping line and no longer displays the user display name in the table row.

## Verification

- `pnpm --dir src/web exec vitest run src/pages/admin/LogAuditPage.test.tsx`
- `pnpm --dir src/web exec vitest run src/pages/admin/AdminMobileAdaptation.test.ts`
- `uv run pytest src/backend/tests/test_product_usage_logging.py`
- `bash scripts/generate-openapi-client.sh`
- CSS contract coverage confirms the ordered log audit layers: table card, filter dropdown, then detail drawer.
- Static check: no `window.confirm` or `window.alert` usage in `LogAuditPage.tsx` or `searchable-select.tsx`.
