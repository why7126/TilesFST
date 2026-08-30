---
purpose: 规范工程迭代日志
content: 强化发布流程产品版本号门禁
source: /spec-opt enforce-product-version-release-gates
update_method: 本日志记录单次治理变更事实；后续变更另开日志或更新 CHANGELOG 摘要
created_at: 2026-08-30 15:44:12
updated_at: 2026-08-30 15:47:12
---

# 产品版本号发布门禁治理日志

## 迭代目标

强化发布流程产品版本号门禁，避免 Web 或小程序用户可见 `PRODUCT_VERSION` 未对齐目标发布版本时仍可进入 release prepare 或 release publish。

## 变更摘要

- `release-prepare` 必须校验 Web shared、小程序 TS、小程序 JS 版本源均对齐发布版本。
- `release-publish` 在用户可见版本号不一致时阻断，`version_change_rationale` 不再作为放行条件。
- `scripts/validate-release.py` 增加多版本源校验，并将版本号不一致归类为 `prepare_evidence_missing`。
- `scripts/validate-image-build.py` 将小程序版本源加入 image input hash 候选，版本源变更后需要重跑 `/image-prepare` 和 `/image-build`。
- 发布技能、发布规则、上下文预算摘要和 AGENTS 入口摘要已同步。

## 影响范围

| 层级 | 影响 |
|---|---|
| API | 不适用，未修改后端接口。 |
| DB | 不适用，未修改 schema、migration 或数据模型。 |
| Web | 仅发布治理检查 Web shared 版本源，不修改 Web 业务实现。 |
| 小程序 | 仅发布治理检查小程序版本源，不修改小程序业务实现。 |
| 管理端 | 不适用。 |
| Orval | 不适用。 |
| Docker Compose | 不适用，未修改 Compose；版本源变更后要求重跑镜像准备与构建。 |

## 更新文件

- `scripts/validate-release.py`
- `scripts/validate-image-build.py`
- `tests/test_release_validation.py`
- `.agents/skills/release-propose/SKILL.md`
- `.agents/skills/release-prepare/SKILL.md`
- `.agents/skills/release-status/SKILL.md`
- `.agents/skills/release-publish/SKILL.md`
- `.agents/skills/image-prepare/SKILL.md`
- `rules/release.md`
- `rules/agent-context-budget.md`
- `AGENTS.md`
- `openspec/changes/enforce-product-version-release-gates/`
- `iterations/change/sprint-029/`

## 关键决策

- 已采纳：发布阶段不再允许 rationale 放行产品版本号不一致，因为用户可见版本属于发布事实，不是可解释风险。
- 已采纳：小程序 TS/JS 版本源纳入 release validator 和 image input hash，覆盖实际小程序用户可见版本。
- 未采纳：新增独立版本同步命令。本次优先通过发布 validator 强门禁阻断，保持治理变更范围最小。
- 后续触发条件：如新增 App、桌面端或其他用户可见版本源，应同步加入 release validator 与 image input hash 候选。

## 验证结果

- `python -m py_compile scripts/validate-release.py scripts/validate-image-build.py`：通过。
- `uv run pytest tests/test_release_validation.py::test_version_mismatch_blocks_release_even_with_rationale tests/test_release_validation.py::test_miniapp_product_version_mismatch_blocks_publish tests/test_release_validation.py::test_release_status_classifies_product_version_mismatch_as_prepare_gap tests/test_release_validation.py::test_image_input_candidates_include_user_visible_product_versions -q`：4 passed。
- `python scripts/validate-release.py --release-dir releases/v1.2.2 --stage publish --target development`：通过。
- `python scripts/validate-release.py --release-dir releases/v1.2.2 --status --target development`：published，publish ready yes，无阻塞项。
- `openspec validate enforce-product-version-release-gates`：通过。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `python scripts/validate-sprint-selection.py --sprint sprint-029`：通过。
- `python scripts/validate-sprint-scope.py sprint-029 --item enforce-product-version-release-gates`：通过。
- `python scripts/validate-doc-prose-hygiene.py <focused-paths>`：仅启发式 warning，无阻断。
- `python scripts/sync-workflow-status.py --event opsx.apply --change enforce-product-version-release-gates --sprint auto`：通过。
- `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change enforce-product-version-release-gates --sprint sprint-029 --json`：actual，warning_count=0。

## 后续建议

- 后续若产品增加新的端侧版本源，应先通过 `/spec-opt` 更新版本源列表与测试，再纳入发布流程。
- 可以另行评估是否增加一个轻量版本同步命令，但不作为本次治理门禁落地的前置条件。
