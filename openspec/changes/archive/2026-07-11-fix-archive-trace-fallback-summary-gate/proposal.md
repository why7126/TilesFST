# Proposal: 修复归档 Change 缺失 trace 时兜底摘要门禁缺失

## Why

`BUG-0063-archived-change-trace-fallback-summary` 发现，已归档 OpenSpec Change 可以缺失 `trace.md`，且 `proposal.md`、`design.md`、`tasks.md` 中也没有标准化归档验证摘要时，现有归档 readiness gate 仍可能只因 tasks 全部完成而返回 `PASS`。这会削弱 OpenSpec archive 作为事实源的可信度，让验证结论、测试命令、关联 Issue/Sprint 状态和归档证据只能靠人工拼接。

## What Changes

- 扩展 Sprint / OpenSpec 归档 readiness gate，对 archived Change 增加 `trace.md` 存在性检查。
- 当 archived Change 缺失 `trace.md` 时，检查 `proposal.md`、`design.md`、`tasks.md` 是否包含标准化归档验证摘要。
- 缺失 `trace.md` 且没有兜底摘要时输出 blocker，并在报告中说明缺失项、Change 路径和修正建议。
- 更新 `/opsx-archive` 与 `/sprint-archive` 技能说明，使手工归档流程与脚本门禁一致。
- 补充脚本级回归测试，覆盖 trace 存在、trace 缺失但摘要存在、trace 缺失且无摘要三类场景。

## Capabilities

### New Capabilities
- 无

### Modified Capabilities
- `agent-workflow-tooling`: 增加 archived Change 缺失 `trace.md` 时必须具备标准化归档验证摘要的 readiness gate 行为。

## Impact

- 影响脚本：`scripts/validate-sprint-archive-readiness.py`。
- 影响技能文档：`.agents/skills/source-command-opsx-archive/SKILL.md`、`.agents/skills/source-command-sprint-archive/SKILL.md`。
- 影响测试：新增或更新脚本级 pytest / fixture。
- 不影响后端 API、数据库 schema、Web、小程序或管理端运行时功能。
- 不需要 Orval 生成。

## Rollback Plan

若新门禁误阻断有效归档：

1. 回退 readiness gate 中 trace / fallback summary 检查逻辑。
2. 保留已补充的历史归档摘要文本，不做批量删除。
3. 恢复 `/opsx-archive` 与 `/sprint-archive` 对 archived Change 的原检查口径。
4. 重新运行相关 pytest、`openspec validate fix-archive-trace-fallback-summary-gate --strict` 和必要的 workflow sync check，确认文档与派生状态无漂移。
