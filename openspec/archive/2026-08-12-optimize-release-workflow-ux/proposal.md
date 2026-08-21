---
created_at: 2026-08-12 09:15:58
updated_at: 2026-08-12 09:15:58
---

# 优化发布流程操作体验

## 背景

The v1.1.0 release flow proved the release, usage-docs, image-prepare, image-build, and publish commands can complete a full governed release. The flow also exposed small operator-experience gaps:

- Release planning should summarize usage docs, announcement, and image decisions as explicit operator choices.
- Prepare-time blockers such as MySQL drift should include a concrete remediation path.
- Publish-time announcement changes should clearly state whether they affect image input hashes and whether rebuild is required.

## 变更内容

- Tighten release command guidance so release decisions are captured once and echoed consistently.
- Add release-prepare guidance for actionable blocker output, especially MySQL drift and test-environment dependency issues.
- Add image command guidance for clearer warning/blocker treatment and next-step language.
- Add release-publish guidance for post-publish announcement generation without image rebuild loops.
- Record the governance iteration in `docs/spec-logs/`.

## 影响范围

- Affects governance skills and release workflow documentation only.
- Does not change backend API, database schema, Web, miniapp, admin UI, Orval output, Dockerfile, or runtime behavior.
