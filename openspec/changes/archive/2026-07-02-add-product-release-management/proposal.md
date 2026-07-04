## Why

TILESFST already exposes a user-visible `PRODUCT_VERSION`, but the project lacks a product-level release process that can combine multiple Sprints into one public version announcement. Sprint `release-note.md` files describe iteration delivery, while customers, implementation, operations, and the project team need a stable product release object, a public Mintlify announcement, and a release gate that prevents incomplete or unsafe changes from being announced.

## What Changes

- Add product release management as a first-class governance capability.
- Define a product release object that can associate one product version with multiple Sprints, REQs, BUGs, and OpenSpec Changes.
- Add public Mintlify static release announcement requirements, including new features, fixed BUGs, release notes, known issues, upgrade steps, rollback notes, and impact scope.
- Add release readiness gates for OpenSpec archive, tests, Orval, Docker Compose, database migration, `.env.example`, `PRODUCT_VERSION`, and Mintlify build/preview.
- Add governed `releases/` top-level directory rules; the directory may only be created by this OpenSpec Change and must be documented before use.
- Define release command family expectations such as `/release-propose`, `/release-prepare`, and `/release-publish`, with `.cursor/commands/` as the command source.
- Modify the existing Web client product version requirement so release flow validates `PRODUCT_VERSION` against the product release announcement version.

## Capabilities

### New Capabilities

- `product-release-management`: Product version release objects, public Mintlify release announcements, release readiness gates, `releases/` directory governance, and release command-family requirements.

### Modified Capabilities

- `web-client`: Existing product version constant requirements are extended so release flow must validate `src/shared/product-version.ts` `PRODUCT_VERSION` against the product release announcement version.

## Impact

- Affected docs/rules: `rules/directory-structure.md`, `rules/release.md`, `AGENTS.md`, and release-related README/navigation documents.
- Affected command tooling: new release command docs under `.cursor/commands/`, followed by `python scripts/sync-agent-commands.py`.
- Affected release artifacts: new top-level `releases/` directory and Mintlify static announcement source/configuration.
- Affected Web/shared code: release validation must read or verify `src/shared/product-version.ts`; this change must not replace `PRODUCT_VERSION` with `package.json`, FastAPI, OpenAPI, Git, or CI metadata.
- No planned backend release announcement API, database table, management-menu entry, login-page entry, owner Web entry, or miniapp entry.
