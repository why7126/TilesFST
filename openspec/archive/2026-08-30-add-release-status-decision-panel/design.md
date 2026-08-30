---
created_at: 2026-08-30 10:25:00
updated_at: 2026-08-30 10:25:00
---

# Design

## Release Status Panel

`/release-status <version>` reads release artifacts and validators, then prints a compact decision panel:

- release target and deployment boundary
- current workflow phase
- publish readiness
- next command
- blocking decisions
- blocking evidence
- production-only follow-ups that do not block development target
- default upgrade path commands for missing target plans

The command is read-only and does not update `release.json`, image plans, manifests, upgrade plans, or publish confirmation.

## Classification Contract

Release blockers and follow-ups use these normalized classifications:

- `decision_missing`
- `prepare_evidence_missing`
- `publish_evidence_missing`
- `production_only_pending`
- `input_drift`
- `environment_unavailable`
- `scope_incomplete`
- `public_safety`
- `schema_invalid`

Each actionable item should include phase, affected target, owner, current evidence, safe remediation, and rerun check when known.

## Default Upgrade Path Hints

The status panel derives the expected default sources from the existing upgrade validator:

- `fresh -> <version>`
- `<previous-release-version> -> <version>` when a previous release exists

Missing target plans are rendered as exact `/upgrade-plan --from ... --to ... --target ...` commands.

## Image Input Boundary

Image stable input hashes should include files that can change the built images or deployment package behavior: product version, Dockerfiles, Nginx config, Compose files, env examples, build scripts, schemas, migrations, deploy Compose/scripts, and stable release scope. Long-form release evidence and operational narrative documents should not by themselves cause image plan or manifest drift.
