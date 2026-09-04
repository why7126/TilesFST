---
title: 单一项目发布治理验收
created_at: 2026-08-30 16:10:00
updated_at: 2026-08-30 22:01:44
---

# Acceptance

## 验收标准

- Release 命令族与规则文档不再把 development / production 作为本项目发布目标决策。
- `release-publish` 不再要求 `production_deployment` 或生产环境专属证据。
- Release status 不再输出 production-only follow-up；旧 `--target` 入参不改变发布结论。
- Upgrade plan 文件名不包含 `.development` 或 `.production` 后缀。
- v1.2.2 release 事实源使用无 target 后缀升级计划并通过发布校验。

## 验收结果

- `python -m py_compile scripts/validate-agent-context-budget.py scripts/validate-release.py scripts/validate-release-upgrade.py`：通过。
- `uv run pytest tests/test_release_upgrade_validation.py tests/test_release_validation.py::<focused-release-target-tests> -q`：15 passed。
- `uv run pytest tests/test_release_upgrade_validation.py tests/test_release_validation.py -q`：44 passed，3 个既有 usage-docs screenshot fixture 失败，失败点为 `usage-docs/assets` 旧路径校验，与本次发布目标收敛无关。
- `python scripts/validate-release-upgrade.py validate-plan --plan releases/v1.2.2/upgrade-plans/fresh-to-v1.2.2.json`：通过。
- `python scripts/validate-release-upgrade.py validate-plan --plan releases/v1.2.2/upgrade-plans/v1.2.1-to-v1.2.2.json`：通过。
- `python scripts/validate-release.py --release-dir releases/v1.2.2 --stage publish`：通过。
- `python scripts/validate-release.py --release-dir releases/v1.2.2 --status`：published，publish ready yes，blocking decisions/evidence/follow-ups 均为 0，默认升级命令不带 target。
- `python scripts/validate-release.py --release-dir releases/v1.2.2 --stage publish --target production`：通过，旧 target 入参未触发生产专属门禁。
- `python scripts/validate-image-build.py validate-manifest --release v1.2.2`：通过。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `openspec validate simplify-single-release-target-governance`：通过。
- `python scripts/validate-sprint-scope.py sprint-029 --item simplify-single-release-target-governance`：通过。
- `python scripts/validate-doc-prose-hygiene.py <focused-paths>`：仅启发式 warning，无阻断。
- `python scripts/sync-workflow-status.py --event opsx.apply --change simplify-single-release-target-governance --sprint auto`：通过，Updated 2，Errors 0。
- `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change simplify-single-release-target-governance --sprint sprint-029 --json`：actual，warning_count=0。
