---
created_at: 2026-08-30 10:25:00
updated_at: 2026-08-30 10:25:00
---

# Acceptance

## Criteria

- `/release-status <version>` has a documented, read-only command contract.
- The release status script reports phase, next command, decision blockers, evidence blockers, and production-only follow-ups separately.
- Missing default upgrade paths are rendered as exact commands for the release target.
- Image build input hashes no longer include release evidence narrative documents that do not affect image/runtime behavior.
- Validators and tests pass for the focused governance scope.

## Evidence

- `python -m py_compile scripts/validate-release.py scripts/validate-image-build.py`：通过。
- `python scripts/validate-release.py --release-dir releases/v1.2.1 --status`：development 状态面板通过。
- `python scripts/validate-release.py --release-dir releases/v1.2.1 --status --target production`：production 状态面板按预期提示缺失 production upgrade plan 和 production evidence。
- `python scripts/validate-image-build.py validate-manifest --release v1.2.1`：通过。
- 聚焦 pytest：3 passed。
