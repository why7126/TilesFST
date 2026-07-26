## Context

REQ-0067 has approved a refinement to admin tile category modal rules. The current `tile-category-management` spec still requires create requests to accept `code`, allows category names up to 30 characters, and primarily protects uniqueness via code. The current Web admin `CategoryFormModal` also exposes code entry in create mode.

Existing constraints:

- `tile_categories.code` is already a unique internal field and should remain stable for API compatibility, route/filter compatibility and existing records.
- A completed two-level category change narrows new category depth to two levels; this change must not reintroduce level-2 parents as valid create parents.
- Admin modal work must preserve the `admin-modal` knowledge-base gate: no generic `modal-card` plus dedicated class double mounting, computed width checks and short-viewport body scroll.
- API form validation must continue to use the unified `{ code, message, data }` envelope and Orval-generated types.

## Goals / Non-Goals

**Goals:**

- Remove user-entered category code from the create/edit modal and create payload.
- Generate a unique `CAT-` prefixed code in backend domain logic.
- Validate category name as non-empty, at most 10 visible characters, and Chinese/English/digits only.
- Enforce same-parent category name uniqueness for create and update, excluding the current record on update.
- Keep category modal fields, required markers, inline validation and refresh behavior testable.
- Keep OpenAPI, Orval, error-code docs and backend/Web tests aligned.

**Non-Goals:**

- Do not remove `tile_categories.code` or stop returning it in admin list/tree/detail responses.
- Do not migrate historical duplicate names, historical level-3 records or historical names longer than 10 characters.
- Do not add category merge, drag sorting, import/export, aliases or multilingual category names.
- Do not change miniapp category page rendering, product-list filtering or SKU category association behavior.
- Do not change object storage or media upload behavior.

## Decisions

### D1. UI Strategy: Existing Modal CSS Port + DS Refinement

Use the existing `CategoryFormModal` structure and feature CSS, applying a focused field/content refinement. The HTML prototype is a semantic reference for field order, required markers and inline error placement, not a new visual system. Implementation should keep the category modal dedicated class as the width owner and must not introduce `modal-card` double mounting.

Alternatives considered:

- Full redesign of the tile category page: rejected because REQ-0067 only changes modal form semantics.
- Shared admin modal component extraction: deferred; this change can be implemented safely in the existing component.

### D2. Backend Owns Category Code Generation

The backend service owns category code generation. The create request no longer accepts or requires `code`; the service generates a unique code with `CAT-` prefix and persists it under the existing unique column.

Alternatives considered:

- Generate code on the frontend: rejected because uniqueness and collision handling belong in backend/domain logic.
- Keep user-entered code but hide it after save: rejected because it does not reduce operator burden or prevent bad codes.

### D3. Name Validation and Uniqueness

Category name validation belongs in both frontend and backend. Frontend provides immediate feedback; backend is the source of truth and must reject invalid or duplicated same-level names. Same-level uniqueness uses `parent_id`, including `NULL` for top-level categories. English duplicate matching should be case-insensitive unless implementation discovers a database collation incompatibility that must be documented in trace.

### D4. API Compatibility and Orval

Admin responses may continue returning `code`; only the create request contract changes. Any Pydantic schema change must update OpenAPI and Orval in the same apply. Web code must use the regenerated type instead of hand-written request types.

### D5. Error Codes

Use existing error envelope behavior. If no suitable category-name duplicate business error exists, add a stable category-specific error code such as `CATEGORY_NAME_DUPLICATED` and register it in docs and tests.

## Conflict Resolution

Priority order: prototype HTML > prototype context > acceptance.md > rules/ui-design.md > existing OpenSpec specs.

| Conflict | Resolution |
|---|---|
| Existing `tile-category-management` spec says create accepts `code` | Delta changes create contract so backend generates `CAT-` code and frontend does not submit it |
| Existing spec says category `name` max 30 | Delta narrows new/updated admin names to max 10 visible characters |
| Existing spec only has code uniqueness scenario | Delta adds same-parent category-name uniqueness |
| Existing Web category page spec references old add-modal strategy | Delta adds category modal field and admin-modal quality scenarios |
| Prototype HTML contains raw hex as prototype CSS | Implementation must follow `rules/ui-design.md` semantic token rules; prototype color values are not implementation permission |

## Risks / Trade-offs

- [Risk] Historical records may violate new name length or duplicate rules → Mitigation: apply new rules to create/update; do not auto-migrate history in this change.
- [Risk] Generated code collision under concurrent creates → Mitigation: keep DB unique constraint and add retry or stable business error tests.
- [Risk] Orval drift after removing `code` from create request → Mitigation: make OpenAPI export and Orval regeneration explicit tasks.
- [Risk] Same-level duplicate behavior differs by SQLite/MySQL collation → Mitigation: document case-insensitive comparison strategy and test representative cases.
- [Risk] Modal width/scroll regressions from CSS cascade → Mitigation: keep AC-XCUT in tasks and trace evidence.

## Migration Plan

1. Keep `tile_categories.code` and all existing values.
2. Update backend create schema and service to generate code and validate names.
3. Add repository helper for same-parent name lookup with `exclude_id`.
4. Update Web modal to remove code input and submit no `code`.
5. Regenerate OpenAPI/Orval if schemas change.
6. Run focused backend/Web tests and record admin modal width/scroll evidence.

Rollback: since the `code` column remains, rollback can restore the previous request field and UI without data loss. Codes generated during this change remain valid internal category codes.

## Open Questions

- Final code suffix format after `CAT-` may be numeric sequence, timestamped sequence or short random suffix; implementation must document the selected algorithm in trace.
- Final error code name for same-parent duplicate names should be confirmed against the current error-code registry.
