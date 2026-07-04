## 1. Directory and Governance

- [x] 1.1 Update `rules/directory-structure.md` to add top-level `releases/` with responsibility, boundary, naming, lifecycle, and generated-output policy.
- [x] 1.2 Update `AGENTS.md` to include `releases/` in top-level directory guidance and completion checks.
- [x] 1.3 Update `rules/release.md` with product release object, release announcement, release gate, `PRODUCT_VERSION`, and rollback requirements.
- [x] 1.4 Update relevant README/navigation docs so future agents and developers can locate release artifacts.

## 2. Product Release Artifacts

- [x] 2.1 Create the governed `releases/` directory only after completing task 1.1.
- [x] 2.2 Add an initial product release directory/template structure for versioned releases.
- [x] 2.3 Add machine-readable release metadata fields for version, release time, owner, associated Sprints, REQs, BUGs, OpenSpec Changes, known issues, upgrade steps, rollback notes, and impact scope.
- [x] 2.4 Ensure product release scope supports multiple Sprints and excludes unreviewed, undelivered, or unarchived items from formal release scope.

## 3. Mintlify Announcement

- [x] 3.1 Add Mintlify announcement source template for public release pages.
- [x] 3.2 Ensure announcement template includes new features, fixed BUGs, release notes, known issues, upgrade steps, rollback notes, and impact scope.
- [x] 3.3 Add public-safety checks or checklist items to prevent secrets, customer data, DSNs, MinIO credentials, non-public domains, and sensitive operations details from entering announcements.
- [x] 3.4 Document and run Mintlify build/preview or an equivalent validation command.

## 4. Release Commands and Validation

- [x] 4.1 Add release command docs in `.cursor/commands/` for proposing, preparing, and confirming product releases, or document equivalent command names.
- [x] 4.2 Run `python scripts/sync-agent-commands.py` after command changes and commit synchronized command artifacts.
- [x] 4.3 Implement or document release validation for OpenSpec archive, tests, Orval, Docker Compose, database migrations, `.env.example`, `PRODUCT_VERSION`, and Mintlify build/preview.
- [x] 4.4 Ensure failed mandatory gates block release confirmation and report remediation.
- [x] 4.5 Ensure release commands do not introduce draft/pending/published/retracted state machine semantics.

## 5. Product Version Consistency

- [x] 5.1 Validate release metadata version against `src/shared/product-version.ts` `PRODUCT_VERSION`.
- [x] 5.2 Ensure release material records a rationale when a release intentionally does not change `PRODUCT_VERSION`.
- [x] 5.3 Confirm implementation does not use `package.json`, FastAPI `version`, OpenAPI version, Git commit, or CI build number as the user-visible product version.

## 6. Tests and Validation

- [x] 6.1 Add automated tests for release metadata parsing and release gate validation where practical.
- [x] 6.2 Add tests or scripted checks for `PRODUCT_VERSION` consistency.
- [x] 6.3 Run `openspec validate add-product-release-management --strict`.
- [x] 6.4 Run `python scripts/validate-directory-structure.py`.
- [x] 6.5 Run workflow sync after implementation status changes.

## 7. Trace and Sprint

- [x] 7.1 Update REQ-0026 acceptance/report trace after implementation.
- [x] 7.2 Ensure Sprint 004 docs reflect the Change status before Sprint archive.
