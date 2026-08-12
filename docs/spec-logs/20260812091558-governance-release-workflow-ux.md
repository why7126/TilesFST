---
purpose: 发布流程体验治理优化日志
content: 固化发布版本、使用文档、公开公告、镜像准备、镜像构建与发布确认的操作体验契约
source: /spec-opt optimize-release-workflow-ux
update_method: 本日志作为单次治理迭代事实源；后续同类优化新建日志并维护 CHANGELOG
created_at: 2026-08-12 09:15:58
updated_at: 2026-08-12 09:15:58
---

# 发布流程体验治理优化日志

## 迭代目标

将 v1.1.0 发布流程中验证有效的操作体验优化固化到命令规范：

- 发布提议阶段明确 usage docs、公开公告和镜像构建三类决策。
- 发布准备阶段把阻塞项输出为可执行修复路径。
- 镜像准备/构建阶段清晰区分 warning、blocker 和可继续命令。
- 发布确认后补充公告时避免触发镜像 evidence 循环。

## 变更摘要

- `/release-propose` 新增发布决策摘要契约。
- `/release-prepare` 新增 actionable blockers 契约。
- `/image-prepare` 新增 warning / blocker 输出契约。
- `/image-build` 新增 build failure phase 分类。
- `/release-publish` 明确发布后公告补生成的校验与不重建条件。
- `/usage-docs-generate` 明确缺少确认时的两条 unblock path。
- `rules/release.md` 与 `rules/agent-context-budget.md` 同步发布命令族体验规则。

## 影响范围

| 维度 | 影响 |
|---|---|
| API | 无 |
| DB | 无 |
| Web | 无 |
| 小程序 | 无 |
| 管理端 | 无 |
| Orval | 无 |
| Docker | 无运行时变更；仅镜像命令规范说明更新 |
| 治理资产 | `.agents/skills/`、`rules/`、`openspec/changes/`、`iterations/change/`、`docs/spec-logs/` |

## 更新文件

- `.agents/skills/release-propose/SKILL.md`
- `.agents/skills/release-prepare/SKILL.md`
- `.agents/skills/image-prepare/SKILL.md`
- `.agents/skills/image-build/SKILL.md`
- `.agents/skills/release-publish/SKILL.md`
- `.agents/skills/usage-docs-generate/SKILL.md`
- `rules/release.md`
- `rules/agent-context-budget.md`
- `openspec/changes/optimize-release-workflow-ux/`
- `iterations/change/sprint-023/`
- `docs/spec-logs/CHANGELOG.md`

## 验证结果

- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `openspec validate optimize-release-workflow-ux`：通过。

## 后续建议

- 后续如新增 `/release-*` 或 `/image-*` 命令，应复用三类发布决策摘要与 actionable blocker 输出契约。
- 若未来引入自动交互卡片，应将 usage docs、公开公告、镜像构建决策做成同一张发布决策卡。
