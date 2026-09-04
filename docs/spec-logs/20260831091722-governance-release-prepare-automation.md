---
created_at: 2026-08-31 09:17:22
updated_at: 2026-08-31 09:17:22
---

# 发布准备自动化策略收敛治理日志

## 迭代目标

将发布流程中的公告、usage docs 与升级计划决策统一前移到 `/release-propose`，并由 `/release-prepare` 按 `release.json` 自动生成和校验，避免发布时在 status、usage-docs、upgrade 和 publish 命令之间反复人工切换。

## 变更摘要

- `/release-propose` 增加 `--usage-docs`、`--no-usage-docs`、`--upgrade-from <fresh|version>` 契约；默认声明公告必生成/更新、usage docs skipped、升级路径包含 fresh 与上一正式版本。
- `/release-prepare` 改为读取 `release.json` 决策，自动同步 `PRODUCT_VERSION`、生成/更新公告、按需生成 usage docs / Mintlify 投影，并生成校验默认与显式升级计划。
- `/release-status` 保持只读；缺默认或声明升级计划时主线修复指向 `/release-prepare <version>`。
- `/release-publish` 收敛为确认命令，不生成主公告、usage docs、Mintlify 投影或 upgrade plan。
- release validator 支持 `upgrade_plans.explicit_sources` 与 usage docs `requested` 状态；usage docs 迁移会清理 release-local assets 并修正页面图片引用为共享 Mintlify 资产。

## 影响范围

- 影响 `.agents/skills/release-*`、`upgrade-plan`、`image-build`、`usage-docs-*` 命令契约。
- 影响 `rules/release.md`、`rules/agent-context-budget.md`、`rules/directory-structure.md`、`AGENTS.md` 发布摘要。
- 影响 `scripts/validate-release.py`、`scripts/validate-usage-docs.py`、`scripts/generate-usage-docs.py` 与发布治理测试。
- 不影响业务 `src/`、API、数据库 schema、Web 页面、小程序页面或管理端业务实现。

## 更新文件

- `.agents/skills/release-propose/SKILL.md`
- `.agents/skills/release-prepare/SKILL.md`
- `.agents/skills/release-status/SKILL.md`
- `.agents/skills/release-publish/SKILL.md`
- `.agents/skills/upgrade-plan/SKILL.md`
- `.agents/skills/image-build/SKILL.md`
- `.agents/skills/usage-docs-generate/SKILL.md`
- `.agents/skills/usage-docs-validate/SKILL.md`
- `AGENTS.md`
- `rules/release.md`
- `rules/agent-context-budget.md`
- `rules/directory-structure.md`
- `releases/templates/release.json`
- `scripts/validate-release.py`
- `scripts/validate-usage-docs.py`
- `scripts/generate-usage-docs.py`
- `tests/test_release_validation.py`
- `openspec/changes/converge-release-prepare-automation/`
- `iterations/change/sprint-029/`

## 关键决策

- 已采纳：usage docs 默认 skipped，显式 `--usage-docs` 才生成，避免每次发布都卡人工确认。
- 已采纳：公告每版必生成/更新，prepare 负责落盘，publish 不再修正文案。
- 已采纳：默认升级计划属于 release prepare 自动化产物；standalone `/upgrade-plan` 只用于显式追加或单条返修。
- 未采纳：恢复 development / production 发布目标区分。本项目当前明确采用单一项目发布语义。

## 验证结果

- `python -m py_compile scripts/validate-release.py scripts/validate-release-upgrade.py scripts/generate-usage-docs.py scripts/validate-usage-docs.py`：通过。
- `uv run pytest tests/test_release_validation.py tests/test_release_upgrade_validation.py`：51 passed。
- `openspec validate converge-release-prepare-automation`：通过。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `python scripts/validate-sprint-scope.py sprint-029 --item converge-release-prepare-automation`：通过。
- `python scripts/validate-doc-prose-hygiene.py <focused-paths>`：返回 20 条兼容旧字段、历史状态和规则说明相关启发式 warning，无阻断。
- `python scripts/sync-workflow-status.py --event opsx.apply --change converge-release-prepare-automation --sprint auto`：通过。
- `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change converge-release-prepare-automation --sprint sprint-029 --json`：actual usage 记录成功，warning_count=0。

## 影响声明

- API：不涉及。
- 数据库：不涉及。
- Web：不涉及业务实现；仅发布版本源治理规则。
- 小程序：不涉及业务实现；仅发布版本源治理规则。
- 管理端：不涉及。
- Orval：不需要。
- Docker Compose：不需要真实 Compose 验证；本次未改变 Compose 文件。

## 后续建议

- 下一次 `/release-propose` 应直接写入四类发布决策摘要，避免 usage docs 再进入 pending 默认态。
- 后续如要把 release-prepare 进一步做成完全确定性脚本，可在此规范基础上新增 `scripts/prepare-release.py`，但仍需保持 publish confirmation-only。
