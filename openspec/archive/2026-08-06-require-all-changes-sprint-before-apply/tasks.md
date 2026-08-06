---
change_id: require-all-changes-sprint-before-apply
title: 实施任务
status: proposed
created_at: 2026-08-06 14:01:45
updated_at: 2026-08-06 14:01:45
---

# 任务

## 1. 规则与文档同步

- [x] 1.1 更新 `AGENTS.md`，说明所有 Change 在 `/opsx-apply` 前都必须纳入 Sprint。
- [x] 1.2 更新 `rules/document-governance.md`，移除纯治理 Change 可豁免 Sprint 门禁的表述。
- [x] 1.3 更新 `rules/iterations-lifecycle.md`，补充非 REQ/BUG Change 的 Sprint scope 规则。
- [x] 1.4 更新 `docs/README.md` 或相关索引，提示 `/opsx-propose` 直接创建的 Change 也需先纳入 Sprint。

## 2. 技能同步

- [x] 2.1 更新 `.agents/skills/opsx-apply/SKILL.md`，对所有 Change 强制执行 Sprint Inclusion Gate。
- [x] 2.2 更新 `.agents/skills/spec-opt/SKILL.md`，删除纯治理 Change 的 `/opsx-apply` Sprint Gate 豁免。
- [x] 2.3 更新 `.agents/skills/workflow-sync/SKILL.md`，说明 `opsx.apply` skipped/unresolved 阻断所有 Change。

## 3. 脚本与校验

- [x] 3.1 评估是否需要扩展 `scripts/validate-agent-context-budget.py` 或其他治理校验脚本，防止豁免表述回退。
- [x] 3.2 若修改脚本，运行对应脚本级最小验证；若不修改脚本，记录不适用原因。
- [x] 3.3 运行 `python scripts/validate-agent-context-budget.py`。
- [x] 3.4 运行 `python scripts/validate-openspec-language.py`。
- [x] 3.5 运行 `python scripts/validate-directory-structure.py`。
- [x] 3.6 运行 `openspec validate require-all-changes-sprint-before-apply`。

## 4. 复核

- [x] 4.1 复核没有修改业务 `src/` 代码。
- [x] 4.2 使用聚焦 `git diff --stat` 确认影响范围只包含治理资产和本 Change。
- [x] 4.3 最终输出下一步与待用户决策/处理，且两者不重复。
