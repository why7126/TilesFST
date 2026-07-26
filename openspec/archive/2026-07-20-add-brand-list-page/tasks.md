## 1. Data and API Contract

- [x] 1.1 Confirm whether brand page carousel reuses existing Banner management or requires a brand-page placement enum; document the chosen source in implementation notes.
- [x] 1.2 Implement or reuse miniapp brand list data access so only enabled and public brands are returned.
- [x] 1.3 Implement or reuse miniapp brand carousel data access using safe public/authorized media URLs.
- [x] 1.4 If API contract changes, update OpenAPI, Orval generated client, API docs, and relevant backend tests.
- [x] 1.5 Add tests ensuring responses do not expose disabled brands, private brands, internal notes, raw object keys, Authorization headers, cookies, or management-only fields.

## 2. Miniapp Page and Routing

- [x] 2.1 Add the brand list page route, page registration, runtime script, template, style, and JSON config under `src/miniapp/pages/`.
- [x] 2.2 Update the existing brand entry from “找砖” or construction fallback to “品牌” and route it to the brand list page.
- [x] 2.3 Ensure the page supports initial loading, empty state, error state, retry, and optional pagination/load-more behavior.
- [x] 2.4 Ensure the page can safely return to the previous page or home when entered from share/external/direct paths.

## 3. Brand Carousel

- [x] 3.1 Render a top brand carousel aligned with the miniapp home carousel autoplay, circular, indicator, title, subtitle, and brand-gold active indicator behavior.
- [x] 3.2 Implement carousel click handling for brand, product, search, store, or supported fallback targets.
- [x] 3.3 Add safe degradation for missing carousel data, image load failure, and unreachable targets.

## 4. Brand Grid and Card Behavior

- [x] 4.1 Extend or reuse the miniapp brand-card component for a two-column grid variant without duplicating core logo fallback and click fallback logic.
- [x] 4.2 Render brand cards one row with two cards, each showing at least Logo and brand name plus optional short metadata.
- [x] 4.3 Implement logo missing/error fallback and long brand name handling without layout shift, overlap, or horizontal scrolling.
- [x] 4.4 Implement card click to brand detail/home when available, or brand-filtered product list fallback when `REQ-0058` is not available.
- [x] 4.5 Prevent unavailable brands from opening invalid routes and show a lightweight unavailable prompt.

## 5. Analytics and Privacy

- [x] 5.1 Record brand list page view with `brand_list_page_view` or equivalent event.
- [x] 5.2 Record brand carousel click with carousel ID, jump type, and index where available.
- [x] 5.3 Record brand card click with brand ID, index, source page, and source entry where available.
- [x] 5.4 Verify analytics does not record phone numbers, addresses, WeChat IDs, authorization headers, cookies, or unrelated sensitive data.

## 6. Miniapp Navigation and Device Evidence

- [x] 6.1 Apply the miniapp custom navigation best-practice for status bar, capsule reserve, page offset, return fallback, and touch target size.
- [x] 6.2 Verify DevTools 320 pt, 375 pt, and 430 pt viewports for carousel framing, two-column cards, TabBar overlap, loading state, empty state, and error state.
- [x] 6.3 Record evidence using the project miniapp device evidence template; mark real-device coverage as `blocked` or `follow_up` if unavailable.
- [x] 6.4 Add or update static tests to detect miniapp `.ts` / `.js` runtime entry drift for the new page.

## 7. Validation and Documentation

- [x] 7.1 Run focused backend/API tests if API changes are made.
- [x] 7.2 Run focused miniapp static tests for route registration, entry text, page runtime, and brand card rendering constraints.
- [x] 7.3 Validate OpenSpec change with `openspec validate add-brand-list-page --strict`.
- [x] 7.4 Update acceptance evidence references in the Sprint or Change output before marking apply complete.
