---
purpose: Workflow Sync Sprint Propose 迭代回填治理日志
content: 记录 sprint.propose 自动回填 REQ/BUG trace iteration 的规范与脚本修复
source: /spec-opt fix-workflow-sync-sprint-propose-iteration
update_method: 本次治理修复完成后记录；后续同类规则变化通过 /spec-opt 更新
created_at: 2026-08-27 00:25:41
updated_at: 2026-08-27 00:25:41
---

# Workflow Sync Sprint Propose 迭代回填治理日志

## 迭代目标

检查并修复 Workflow Sync 对 `sprint.propose` 的 Issue 迭代回填能力，确保已评审 REQ/BUG 被正式写入 `sprint.yaml` 后，Issue `trace.md` 的 `status` 与 `iteration` 同步成为可信机器事实。

## 变更摘要

- 确认当前 Workflow Sync 能从 Sprint scope 推导 Issue `in_sprint` 状态，但 `patch_issue_trace()` 未写入 `iteration`。
- 调整 `scripts/workflow_sync/patch.py` 与 `scripts/workflow_sync/engine.py`，仅对已存在于目标 Sprint `requirements[]` / `bugs[]` 的 Issue 写入 `iteration: sprint-xxx`。
- 补充聚焦测试，覆盖 `approved + iteration: null` 的 REQ 在 `sprint.propose` 后同步为 `in_sprint + iteration:sprint-xxx`。
- 同步 `.agents/skills/workflow-sync/SKILL.md` 与 `rules/document-governance.md` 的 Workflow Sync 规则说明。

## 影响范围

- 治理脚本：Workflow Sync Issue trace 写回逻辑。
- 命令技能：`workflow-sync` 对 `sprint.propose` 的职责说明。
- 规则文档：Sprint scope 与 Issue trace 一致性要求。
- OpenSpec Change：`fix-workflow-sync-sprint-propose-iteration`。

## 更新文件

- `scripts/workflow_sync/patch.py`
- `scripts/workflow_sync/engine.py`
- `tests/test_workflow_sync_time_drift.py`
- `.agents/skills/workflow-sync/SKILL.md`
- `rules/document-governance.md`
- `openspec/changes/fix-workflow-sync-sprint-propose-iteration/`
- `iterations/change/sprint-026/sprint.yaml`
- `docs/spec-logs/CHANGELOG.md`
- `docs/spec-logs/20260827002541-governance-workflow-sync-sprint-propose-iteration.md`

## 关键决策

- 已采纳原因：`iteration` 是 Issue 是否已进入 Sprint 的机器事实，缺失会让后续 `/req-opsx`、`/bug-opsx` 与 `/opsx-apply --sprint auto` 出现状态漂移。
- 未采纳方案：不在 `add-sprint-scope-item.py` 中直接写 Issue trace，避免该脚本同时承担 Sprint scope 持久化和 Issue 状态派生两类职责。
- 替代方案：可让 `/sprint-propose` 手工写 trace，但这会绕过 Workflow Sync 统一派生逻辑，维护成本更高。
- 验证责任：聚焦测试、Sprint scope 校验、OpenSpec 校验与治理脚本校验共同确认。
- 后续触发条件：若 Workflow Sync 新增其他 Sprint scope 事件，需要同步验证 Issue trace `iteration` 和状态是否一致。

## 验证结果

- `uv run pytest tests/test_workflow_sync_time_drift.py -q`：25 passed。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `openspec validate fix-workflow-sync-sprint-propose-iteration`：通过。
- `python scripts/validate-doc-prose-hygiene.py <focused-paths>`：通过执行，返回 11 条启发式 history-narration warning，未发现阻断项。

## API/DB/Web/小程序/管理端/Orval/Docker 影响

- API：不影响。
- 数据库：不影响。
- Web：不影响。
- 小程序：不影响。
- 管理端：不影响。
- Orval：不需要。
- Docker Compose：不需要。

## 后续建议

无明显优化点。
