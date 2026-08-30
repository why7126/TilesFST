---
created_at: 2026-08-30 09:50:00
updated_at: 2026-08-30 09:50:00
---

# 提案：拆分开发环境发布与生产发布门禁

## 背景

The current release workflow treats a single `/release-publish` confirmation as if it always represents production deployment. In practice, the project also needs development-environment release confirmations. Production-only evidence, such as real production env values, MySQL/COS backup confirmation, public no-fallback media evidence, and production smoke, should not block a development-environment release.

The same ambiguity also affects upgrade plans: normal release preparation should generate upgrade plans, but a development release should create development-targeted plans, while production release remains a separate workflow with production-targeted gates.

## 变更内容

- Add explicit release target semantics: `development` and `production`.
- Extend release metadata with a conservative `release_target` object.
- Make release validation select publish gates based on the target environment.
- Require default upgrade plans for normal development release confirmation, but generate them with development deployment semantics.
- Keep production-only evidence as production release blockers, not development release blockers.
- Update release and upgrade command instructions so operators know which workflow they are confirming.

## 范围外

- No application runtime code changes.
- No API, DB schema, Web, miniapp, or admin product behavior changes.
- No automatic production deployment, production env mutation, database writes, DB restore, or object storage writes.

## 影响范围

- Rules: release governance and deployment documentation.
- Skills: release propose/prepare/publish and upgrade plan/validate command guidance.
- Scripts: release validation and upgrade plan generation/validation.
- Templates: release metadata template.
