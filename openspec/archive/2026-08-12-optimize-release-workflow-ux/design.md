---
created_at: 2026-08-12 09:15:58
updated_at: 2026-08-12 09:15:58
---

# Design

## Scope

This is a governance-only optimization for the release command family:

- `release-propose`
- `release-prepare`
- `image-prepare`
- `image-build`
- `release-publish`
- `usage-docs-generate`
- `rules/release.md`
- `rules/agent-context-budget.md`

## Design Principles

1. Make release decisions explicit early.
   Release proposal should surface usage docs, announcement, and image build choices together, and should preserve operator choices in `release.json`.

2. Make blockers actionable.
   When prepare finds an environment or release gate blocker, output should include the exact safe next command or remediation path where possible.

3. Avoid image evidence loops.
   Publish and announcement refreshes after image build must not write checksum facts into `announcement.mdx`; image checksum truth remains in `image-manifest.json` and the tarball sidecar.

4. Keep governance-only changes out of runtime.
   No `src/` changes are allowed in this change.

## Acceptance

- Skill docs contain explicit guidance for release decision summaries, actionable prepare blockers, image warning handling, and post-publish announcement handling.
- Release rules document the same operator-experience contract.
- Context budget rules remind agents not to reread broad release history when only command state is needed.
- Governance log and changelog are updated.
