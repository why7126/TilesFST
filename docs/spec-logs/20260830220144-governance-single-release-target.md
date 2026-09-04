---
purpose: 规范工程迭代日志
content: 收敛发布治理为单一项目发布语义
source: /spec-opt simplify-single-release-target-governance
update_method: 本日志记录单次治理变更事实；后续变更另开日志或更新 CHANGELOG 摘要
created_at: 2026-08-30 22:01:44
updated_at: 2026-08-30 22:01:44
---

# 单一项目发布治理日志

## 迭代目标

本项目不再区分 development / production 发布目标。发布、镜像和升级流程统一按单一项目发布语义执行，避免后续发布再次出现目标环境分叉、生产专属门禁或 `.development` / `.production` 升级计划文件名。

## 变更摘要

- `validate-release.py` 统一使用 `project` scope，旧 `--target` 入参仅兼容读取，不改变门禁、状态面板或发布确认结果。
- `validate-release-upgrade.py` 生成无目标环境后缀的升级计划，旧 `deployment_target` 字段仅兼容历史数据。
- Release / upgrade 技能命令移除目标环境推荐参数，默认下一步命令不再带 `--target`。
- `rules/release.md`、`rules/agent-context-budget.md` 和 `AGENTS.md` 同步单一项目发布口径。
- `releases/v1.2.2` 移除当前发布对象中的目标环境字段与生产专属待办，默认升级计划改为无后缀文件名。

## 影响范围

| 层级 | 影响 |
|---|---|
| API | 不适用，未修改接口。 |
| DB | 不适用，未修改 schema、migration 或数据模型。 |
| Web | 不适用，未修改业务实现。 |
| 小程序 | 不适用，未修改业务实现。 |
| 管理端 | 不适用。 |
| Orval | 不适用。 |
| Docker Compose | 不适用，未修改 Compose；仅调整发布/升级治理与校验脚本。 |

## 更新文件

- `scripts/validate-release.py`
- `scripts/validate-release-upgrade.py`
- `tests/test_release_validation.py`
- `tests/test_release_upgrade_validation.py`
- `.agents/skills/release-propose/SKILL.md`
- `.agents/skills/release-prepare/SKILL.md`
- `.agents/skills/release-status/SKILL.md`
- `.agents/skills/release-publish/SKILL.md`
- `.agents/skills/upgrade-plan/SKILL.md`
- `.agents/skills/upgrade-validate/SKILL.md`
- `rules/release.md`
- `rules/agent-context-budget.md`
- `AGENTS.md`
- `releases/templates/release.json`
- `releases/v1.2.2/release.json`
- `releases/v1.2.2/announcement.mdx`
- `releases/v1.2.2/upgrade-plans/`
- `openspec/changes/simplify-single-release-target-governance/`
- `iterations/change/sprint-029/`

## 关键决策

- 已采纳：发布目标不再是本项目治理维度，统一记为 `project` scope。
- 已采纳：旧 `--target`、`release_target`、`deployment_target`、`production_only_pending` 只做兼容读取，不再生成专属门禁。
- 已采纳：升级计划文件名去掉 `.development` / `.production` 后缀。
- 未采纳：保留开发发布和生产发布双轨。用户已明确本项目不涉及生产环境分支，该双轨会制造无效决策点。

## 验证结果

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

## 后续建议

- 后续若项目真实引入多环境正式发布，再通过新的 OpenSpec Change 重新设计环境维度，不复用本次删除的旧双轨默认。
