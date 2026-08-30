---
created_at: 2026-08-30 09:50:00
updated_at: 2026-08-30 09:50:00
acceptance_status: pending
---

# Acceptance

## Criteria

- Release metadata and rules clearly distinguish development release confirmation from production release confirmation.
- Development release validation does not block on production-only env, MySQL/COS backup, no-fallback public media, production API, or production smoke evidence.
- Production release validation can still require production-targeted deployment and evidence gates.
- Upgrade plans can be generated and validated with a target environment.
- No business runtime code under `src/` is modified.
