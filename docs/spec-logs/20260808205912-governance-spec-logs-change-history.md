---
purpose: 规范工程治理迭代日志
content: 记录新增 docs/spec-logs 变更历史总账的治理优化
source: /spec-opt add-spec-logs-change-history
update_method: 本日志为单次治理迭代记录；后续修正同一主题时更新对应 CHANGELOG 条目
created_at: 2026-08-08 20:59:12
updated_at: 2026-08-08 21:03:00
---

# 新增规范工程变更历史总账

## 迭代目标

在 `docs/spec-logs/` 下新增规范工程变更历史文档，用于汇总记录每一次规范、脚本、技能、命令和治理文档更新，降低只依赖分散时间戳日志带来的追溯成本。

## 变更摘要

- 新增 `docs/spec-logs/CHANGELOG.md`，作为规范工程变更历史总账。
- 明确 `CHANGELOG.md` 与单次 `YYYYMMDDhhmmss-governance-*.md`、`YYYYMMDDhhmmss-study-*.md` 日志的职责边界。
- 为 `CHANGELOG.md` 的变更历史表新增“跨项目落地提示词”列，记录其他项目落地同类治理规范时可复用的脱敏 Prompt。
- 更新 `docs/spec-logs/README.md`、`docs/README.md`、`rules/document-governance.md`、`rules/directory-structure.md`、`AGENTS.md` 和 `/spec-opt` 技能说明。
- 新增 OpenSpec Change `add-spec-logs-change-history`，记录本次规范变更的 proposal、design、tasks 和 delta spec。

## 影响范围

- 影响：文档治理、目录边界说明、AI 执行入口、`/spec-opt` 技能规则、OpenSpec 治理规格。
- 不影响：业务 `src/` 运行时代码。

## 更新文件

- `docs/spec-logs/CHANGELOG.md`
- `docs/spec-logs/README.md`
- `docs/spec-logs/20260808205912-governance-spec-logs-change-history.md`
- `docs/README.md`
- `rules/document-governance.md`
- `rules/directory-structure.md`
- `AGENTS.md`
- `.agents/skills/spec-opt/SKILL.md`
- `openspec/changes/add-spec-logs-change-history/proposal.md`
- `openspec/changes/add-spec-logs-change-history/design.md`
- `openspec/changes/add-spec-logs-change-history/tasks.md`
- `openspec/changes/add-spec-logs-change-history/specs/agent-workflow-tooling/spec.md`

## 验证结果

- 通过：`python scripts/validate-agent-context-budget.py`
- 通过：`python scripts/validate-openspec-language.py`
- 通过：`python scripts/validate-directory-structure.py`
- 通过：`openspec validate add-spec-logs-change-history`
- 通过：`python scripts/validate-sprint-scope.py sprint-022 --item add-spec-logs-change-history`
- 通过：补充“跨项目落地提示词”列后的治理文档与 OpenSpec 校验

## API / DB / Web / 小程序 / 管理端 / Orval / Docker 影响

- API：不影响。
- 数据库：不影响。
- Web：不影响。
- 小程序：不影响。
- 管理端：不影响。
- Orval：不需要。
- Docker Compose：不需要。

## 后续建议

- 下一步执行 `/opsx-archive add-spec-logs-change-history`，将本次治理 delta 合并到正式 OpenSpec 规格。
