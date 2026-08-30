---
created_at: 2026-08-30 09:50:00
updated_at: 2026-08-30 09:50:00
---

# Design

## Release Target Model

Release metadata gains a `release_target` object:

```json
{
  "release_target": {
    "environment": "development",
    "deployment_scope": "development",
    "production_release_required": true,
    "rationale": "This confirmation covers the development deployment only."
  }
}
```

`environment` and `deployment_scope` accept `development` or `production`. Missing legacy fields default to `production` for historical compatibility unless scripts explicitly backfill a release as development.

## Gate Selection

Development publish validation:

- Requires ordinary release gates, product version, announcement safety, usage docs decision, image plan/build evidence when image-governed, and default development upgrade plans.
- Does not require production env proof, production MySQL/COS backup, production no-fallback public media evidence, production public API evidence, or production smoke.

Production publish validation:

- Requires the ordinary release gates.
- Requires production deployment confirmation fields when production deployment is in scope.
- Requires production-targeted upgrade plans unless explicitly justified as not applicable.

## Upgrade Plans

`validate-release-upgrade.py` accepts `--target development|production` and writes `deployment_target`.

Development plans:

- Use development env language.
- Treat `TILESFST_IMAGE_TAG=<version>` as a development deployment confirmation when image-based dev deployment is used.
- Do not classify production-only env keys as required production blockers.

Production plans:

- Preserve current production env, backup, MySQL, object storage, smoke, and rollback expectations.

## Validator Compatibility

- `scripts/validate-release.py` accepts legacy releases that lack `release_target`.
- For releases at or after this governance change, new release objects should include `release_target`.
- Upgrade plan existence is checked at publish stage for normal releases according to target environment.
