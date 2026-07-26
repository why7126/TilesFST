## 1. Backend and API Contract

- [x] 1.1 Update tile category create schema so admin clients no longer submit or require `code`.
- [x] 1.2 Implement backend `CAT-` prefixed unique category code generation with collision handling.
- [x] 1.3 Add backend name validation for trim non-empty, max 10 visible characters, and Chinese/English/digits only.
- [x] 1.4 Add same-parent category-name uniqueness checks for create and update, excluding the current record on update.
- [x] 1.5 Add or reuse stable error codes for invalid category name and duplicate same-level category name; sync error-code docs.

## 2. Web Admin Modal

- [x] 2.1 Update `CategoryFormModal` so create/edit modal does not show editable category code input.
- [x] 2.2 Add required markers for parent category, category name and sort order.
- [x] 2.3 Keep parent selector limited to top-level categories and the fixed top-level option; do not allow level-2 parents.
- [x] 2.4 Add frontend validation for category name and sort order with field-level messages.
- [x] 2.5 Submit create payload without `code` using regenerated Orval types.
- [x] 2.6 Keep category code as the only second-line content in the admin category list name column; do not show hierarchy path there.

## 3. Specs, OpenAPI and Orval

- [x] 3.1 Regenerate/export OpenAPI after Pydantic schema changes.
- [x] 3.2 Regenerate Orval client and update Web imports/call sites.
- [x] 3.3 Update API docs and route/error-code references for the category create contract.
- [x] 3.4 Confirm no database schema migration is required; if required by implementation findings, update SQLite/MySQL docs and tests.

## 4. Tests and Verification

- [x] 4.1 Add backend tests for create without `code`, generated `CAT-` code, invalid names, duplicate same-level names and update self-exclusion.
- [x] 4.2 Add Web component tests for hidden code input, required markers, parent options, field validation and no `code` in create payload.
- [x] 4.3 Add API/Orval contract verification for category create request type changes.
- [x] 4.4 Run focused backend tests for tile categories and validation envelope.
- [x] 4.5 Run focused Web tests for category modal and API wrapper behavior.
- [x] 4.6 Add Web page test that the category list name column shows code on the second line and does not show hierarchy path.

## 5. UI Evidence and Trace

- [x] 5.1 Record admin modal conflict resolution in change trace after implementation.
- [x] 5.2 Verify 1440px computed modal width remains 560px or document any approved width change.
- [x] 5.3 Verify short-viewport modal body scroll keeps required fields and footer actions reachable.
- [x] 5.4 Verify TSX does not double mount `modal-card` and a dedicated category modal class.
