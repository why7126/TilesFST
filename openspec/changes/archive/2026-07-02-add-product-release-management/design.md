## Context

REQ-0026 introduces product-level release management above the existing Sprint workflow. Today, Sprint `release-note.md` documents iteration delivery, and `src/shared/product-version.ts` stores the user-visible version displayed by Web clients. There is no product release object that can combine multiple Sprints into one product version, no governed public release announcement source, and no release gate that checks OpenSpec archive, tests, Orval, Docker Compose, database migration, `.env.example`, product version consistency, and static announcement build readiness together.

This change is governance-heavy and cross-cutting. It affects rules, command definitions, release documentation, product version validation, and directory structure. It does not require a backend release announcement API, database table, management UI entry, owner Web entry, miniapp entry, or login-page entry.

REQ-0026 trace references `docs/knowledge-base/retrospectives/sprint-003-retrospective.md`, especially the recurring risk that acceptance sign-off and release/archive gates can be skipped when Sprint scope expands late. This design therefore treats release gates as a first-class product release artifact instead of a loose checklist.

## Goals / Non-Goals

**Goals:**

- Define a product release object that can map one product version to multiple Sprints.
- Add governed `releases/` top-level directory responsibilities, naming, lifecycle, and relationship to `iterations/`, `issues/`, `openspec/changes/`, and Mintlify source files.
- Define public Mintlify release announcement source requirements.
- Define release readiness gates for OpenSpec archive, tests, Orval, Docker Compose, database migration, `.env.example`, `PRODUCT_VERSION`, and Mintlify build/preview.
- Define release command-family expectations and command-source synchronization through `.cursor/commands/`.
- Extend existing Web client product version requirements so release validation checks `PRODUCT_VERSION` against the product release announcement version.

**Non-Goals:**

- No draft/pending/published/retracted release state machine.
- No admin menu, login page, owner Web, or miniapp release announcement entry.
- No backend announcement API or database table.
- No replacement of Sprint four-piece artifacts.
- No automatic CI version bumping.
- No use of `package.json`, FastAPI `version`, OpenAPI version, Git commit, or CI build number as the user-visible product version.

## Decisions

### D1. Product Release Artifact Shape

Implementation SHALL create product release artifacts under a new top-level `releases/` directory after this OpenSpec Change has been accepted by implementation. A release SHOULD use a versioned directory such as `releases/v0.1.0/` and include a machine-readable release index plus Mintlify announcement source.

Expected release contents SHOULD include:

- release metadata: version, release time, owner, impact scope, related Sprints.
- release scope: related REQs, BUGs, OpenSpec Changes, and archive status.
- gate results: OpenSpec archive, tests, Orval, Docker Compose, database migration, `.env.example`, version consistency, Mintlify build/preview.
- announcement source: public-facing Mintlify Markdown/MDX content.
- rollback and upgrade notes.

Alternative considered: store product releases in `iterations/`. Rejected because a product release can combine multiple Sprints and has a different public announcement lifecycle.

Alternative considered: store announcements in `docs/`. Rejected because `docs/` is long-term project documentation, while product release objects need a release-specific source tree and Mintlify-oriented build structure.

### D2. Directory Governance

Implementation SHALL update `rules/directory-structure.md` before creating `releases/`, and SHALL also update `AGENTS.md` and release-related documentation so the directory is discoverable and governed. `releases/` SHALL be a top-level directory with a narrow responsibility: product release objects and public release announcement source/configuration.

The directory SHALL NOT contain runtime generated site output unless the implementation explicitly documents the generated-output boundary and ignore/commit policy.

### D3. Mintlify Public Announcement

Release announcements SHALL be static documents generated or previewed with Mintlify or an equivalent local Mintlify validation command. Announcement text SHALL be public-safe and SHALL avoid secrets, real customer data, private DSNs, MinIO credentials, internal-only domains, and sensitive operations details.

The public announcement SHALL be distinct from Sprint `release-note.md`. Sprint notes remain iteration-level evidence; product release announcements summarize one product version across one or more Sprints.

### D4. Release Gate Semantics

The release gate SHALL block publish/confirmation when any mandatory check fails. At minimum, the gate SHALL check:

- related OpenSpec Changes are archived or explicitly excluded from formal release scope.
- tests were executed and recorded according to the impact area.
- API changes have OpenAPI and Orval synchronized.
- Docker Compose and deployment documentation are synchronized when deployment changes exist.
- database migrations, database docs, and rollback notes are synchronized when database changes exist.
- `.env.example` and adjacent comments are synchronized when environment variables change.
- `src/shared/product-version.ts` `PRODUCT_VERSION` matches the product release version, or the release records why no version change is required.
- Mintlify build/preview succeeds.

### D5. Command Family

Implementation SHOULD add release command docs in `.cursor/commands/` and synchronize them with `python scripts/sync-agent-commands.py`. Command names may be `/release-propose`, `/release-prepare`, and `/release-publish`, or equivalent names if implementation records the rationale.

The commands SHALL not introduce a draft/pending/published/retracted release state machine. The command flow SHALL focus on creating release material, validating it, and confirming publication evidence.

### D6. UI and Prototype Conflict Resolution

REQ-0026 has no `prototype/` directory and does not add application UI. Therefore, there is no HTML/PNG conflict report and no UI explore strategy gate. If Mintlify output styling is configured, Mintlify documentation-site capabilities SHALL be used; Web application Design System conformance applies only if implementation touches `src/web`.

## Risks / Trade-offs

- [Risk] `releases/` may become a second undocumented docs tree. → Mitigation: update directory rules, AGENTS, release docs, and README/navigation before using it.
- [Risk] release announcements may include sensitive operational details. → Mitigation: include public-safe content checks in release gates and tasks.
- [Risk] late Sprint scope additions can bypass release sign-off. → Mitigation: require OpenSpec archive and recorded test/gate results before formal release scope.
- [Risk] Mintlify tooling may require network or external dependencies. → Mitigation: document local/CI validation command and provide a fallback manual preview instruction if network is unavailable.
- [Risk] `PRODUCT_VERSION` may drift from the announcement version. → Mitigation: add explicit release validation that compares the constant and release metadata.

## Migration Plan

1. Update rules and documentation to permit and define `releases/`.
2. Create `releases/` structure and initial release template/source files.
3. Add release command docs and synchronize agent commands.
4. Add release validation scripts or command logic for gate checks.
5. Add or update tests for release validation logic and documentation structure where practical.
6. Validate OpenSpec, directory structure, command sync, and release preview/build.

Rollback strategy:

- If implementation is not accepted, remove the newly introduced `releases/` directory and command docs, and revert rules/docs additions before archive.
- If a generated announcement is wrong after publication, correct the source in Git and republish the Mintlify static documentation; release notes MUST record the correction.

## Open Questions

- Exact Mintlify command and configuration file names are implementation details to confirm during `/opsx-apply`.
- Exact release command names may remain `/release-propose`, `/release-prepare`, `/release-publish` unless implementation discovers a local naming conflict.
