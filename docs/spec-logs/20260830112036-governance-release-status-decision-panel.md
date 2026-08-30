---
purpose: 发布流程状态面板治理日志
content: 记录 release status 决策面板、blocker 分类、默认 upgrade 路径提示与 image input hash 边界优化
source: /spec-opt 固化发布流程 Release Status 决策面板、blocker 分类、默认 upgrade 路径提示与 image input hash 边界
update_method: 本日志为本次治理迭代事实源；后续变更通过新的 spec log 或关联 Change 更新
created_at: 2026-08-30 11:20:36
updated_at: 2026-08-30 11:20:36
---

# Release Status 决策面板治理日志

## 迭代目标

把 release、image、upgrade 和 publish 的当前状态统一呈现给操作者，减少多命令之间的记忆负担；本次不引入 `/release-orchestrate` 或自动编排发布命令。

## 变更摘要

- 新增 OpenSpec Change `add-release-status-decision-panel`，定义只读发布状态面板、发布 blocker 分类契约、默认 upgrade 路径提示和 image stable input 边界。
- 新增 `.agents/skills/release-status/SKILL.md`，作为只读状态查看入口。
- 扩展 `scripts/validate-release.py --status`，输出版本、目标环境、阶段、publish readiness、下一步、决策阻塞、证据阻塞、生产后续和默认 upgrade 路径。
- 收窄 `scripts/validate-image-build.py` 的 image stable input 候选，移除长期发布/部署叙述文档；旧 plan 中已记录的叙述文档 drift 也不再作为 image input drift。
- 更新 `rules/release.md`、`rules/agent-context-budget.md`、`AGENTS.md` 和 release/image/upgrade 技能说明。

## 影响范围

- API：不影响。
- DB：不影响。
- Web：不影响。
- 小程序：不影响。
- 管理端：不影响。
- Orval：不需要。
- Docker Compose：不修改 Compose；仅调整发布镜像输入 hash 边界。
- 测试：新增 release status 与 image input boundary 聚焦测试。

## 更新文件

- `AGENTS.md`
- `rules/release.md`
- `rules/agent-context-budget.md`
- `.agents/skills/release-status/SKILL.md`
- `.agents/skills/release-propose/SKILL.md`
- `.agents/skills/release-prepare/SKILL.md`
- `.agents/skills/release-publish/SKILL.md`
- `.agents/skills/image-prepare/SKILL.md`
- `.agents/skills/upgrade-plan/SKILL.md`
- `scripts/validate-release.py`
- `scripts/validate-image-build.py`
- `tests/test_release_validation.py`
- `openspec/changes/add-release-status-decision-panel/`

## 验证结果

- `python -m py_compile scripts/validate-release.py scripts/validate-image-build.py`：通过。
- `python scripts/validate-release.py --release-dir releases/v1.2.1 --status`：通过；development 目标显示已发布，生产专属证据归为非阻塞 follow-up。
- `python scripts/validate-release.py --release-dir releases/v1.2.1 --status --target production`：通过；提示缺失两条 production upgrade plan 与 production deployment evidence。
- `python scripts/validate-image-build.py validate-manifest --release v1.2.1`：通过。
- `uv run pytest tests/test_release_validation.py::test_release_status_reports_missing_default_upgrade_plan_command tests/test_release_validation.py::test_release_status_keeps_production_followups_non_blocking_for_development tests/test_release_validation.py::test_image_input_candidates_exclude_release_evidence_narrative_docs`：3 passed。
- `uv run pytest tests/test_release_validation.py tests/test_release_upgrade_validation.py`：40 passed，3 failed；失败项集中在既有 usage docs screenshot fixture 与共享截图资产契约漂移，非本次 release status / image input boundary 改动引入。

## 决策记录

- 已采纳：新增只读状态面板，先改善用户决策信息，不把多步发布流程改成自动编排。
- 已采纳：默认 upgrade 路径由状态面板直接输出可复制命令，减少操作者记忆成本。
- 已采纳：image stable input 不再包含长期发布证据和部署叙述文档，避免纯治理文档变更触发镜像重建。
- 未采纳：暂不新增 `/release-orchestrate`，避免发布自动化边界过早扩大。

## 后续建议

- 后续若发布流程仍频繁需要人工串联命令，可另起 Change 评估 `/release-orchestrate`，但应以 `/release-status` 的分类结果作为前置输入。
- 既有 usage docs screenshot fixture 漂移可独立通过测试治理或 usage docs 流程修复。
