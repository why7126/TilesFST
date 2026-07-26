## 1. Backend/API and Data Contracts

- [x] 1.1 Confirm whether to implement `GET /api/miniapp/home` or equivalent aggregation, and document request, response and error code contract.
- [x] 1.2 Implement or adapt public miniapp home aggregation using existing store, Banner, SKU, brand, category, spec and media data sources.
- [x] 1.3 Ensure miniapp responses expose only public fields and safe image URLs, with no admin-only fields, internal notes, raw object keys or sensitive configuration.
- [x] 1.4 Add or adapt usage event handling for `product_detail_view`, `home_share`, `product_share`, `home_contact_click` and `product_contact_click`.
- [x] 1.5 If behavior statistics require schema changes, update SQLite/MySQL schema or migrations, database docs and indexes for query paths.
- [x] 1.6 Add or update hot product query logic so manual ordering wins and behavior statistics act as fallback/secondary ranking.
- [x] 1.7 Export OpenAPI and run Orval generation if any API contract changes.

## 2. Miniapp Pages

- [x] 2.1 Create or confirm native WeChat miniapp project structure under `src/miniapp/`.
- [x] 2.2 Implement home page layout using `prototype/miniapp/prototype.html` and `prototype/miniapp/prototype.png` as visual references.
- [x] 2.3 Implement store header and store information page navigation.
- [x] 2.4 Implement search entry, search page and filtered result navigation for space, spec, style, color and all categories.
- [x] 2.5 Implement product detail page with public SKU fields and safe media rendering.
- [x] 2.6 Implement Banner rendering, carousel indicators and safe jump fallback for unsupported targets.
- [x] 2.7 Implement new product and hot product sections with empty-state hiding and product card navigation.
- [x] 2.8 Implement share behavior for home and product detail pages.
- [x] 2.9 Implement at least one available contact method for home/product consultation and safe-hide unavailable methods.

## 3. Scope and UX Guardrails

- [x] 3.1 Remove, hide or disable prototype favorite heart interactions so no usable collection feature is shipped.
- [x] 3.2 Ensure no appointment form, inquiry pricing rule, shortcut-entry admin configuration, service-entry admin configuration, complex user profile or collection-driven ranking is introduced.
- [x] 3.3 Implement loading, empty, network error, image failure and module-level fallback states.
- [x] 3.4 Verify all main tappable targets are at least 44x44 pt and TabBar respects safe area.

## 4. Documentation and Tests

- [x] 4.1 Update API docs, database docs and related standards if API or DB contracts change.
- [x] 4.2 Add backend tests for miniapp home aggregation, public-field filtering, usage event validation and behavior-stat ranking.
- [x] 4.3 Add miniapp smoke or equivalent tests for home load, search, shortcut filters, product detail, store info, share and contact.
- [x] 4.4 Validate 375x812, 390x844 and 320-430 pt width layouts against the prototype.
- [x] 4.5 Record evidence that collection, appointment, inquiry pricing and admin configuration out-of-scope items are not implemented.
