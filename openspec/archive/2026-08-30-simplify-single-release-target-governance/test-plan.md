---
title: 单一项目发布治理测试计划
created_at: 2026-08-30 16:10:00
updated_at: 2026-08-30 22:01:44
---

# Test Plan

## 自动化校验

- `python -m py_compile scripts/validate-release.py scripts/validate-release-upgrade.py`
- `uv run pytest tests/test_release_upgrade_validation.py tests/test_release_validation.py::<focused-release-target-tests> -q`
- `python scripts/validate-release-upgrade.py validate-plan --plan releases/v1.2.2/upgrade-plans/fresh-to-v1.2.2.json`
- `python scripts/validate-release-upgrade.py validate-plan --plan releases/v1.2.2/upgrade-plans/v1.2.1-to-v1.2.2.json`
- `python scripts/validate-release.py --release-dir releases/v1.2.2 --stage publish`
- `python scripts/validate-release.py --release-dir releases/v1.2.2 --status`
- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `openspec validate simplify-single-release-target-governance`
- `python scripts/validate-doc-prose-hygiene.py <focused governance files>`
- `python scripts/validate-sprint-scope.py sprint-029 --item simplify-single-release-target-governance`

## 人工复核

- 确认当前 release / upgrade 命令示例不再推荐 `--target development|production`。
- 确认状态面板不再输出 production-only follow-up。
- 确认 v1.2.2 upgrade plan 文件名无 `.development` / `.production` 后缀。
