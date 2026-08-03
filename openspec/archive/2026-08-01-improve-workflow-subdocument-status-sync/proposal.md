## Why

当前 Workflow Sync 主要同步 `trace.md`、registry、Sprint 派生块和归档 residual，导致 `requirement.md`、`bug.md`、`acceptance.md` 等 Issue 子文档会长期停留在 `draft`、`pending_review`、`approved`、`in_sprint` 等早期状态。Sprint 016 复盘也显示 close 前中间态文案和归档证据缺口会让机器状态与人工阅读结论冲突。

本 Change 用于把 REQ/BUG 子文档状态同步、验收结果回填和 drift check 升级为工作流一等能力，而不是只在 archive promote 阻塞后补救。

## What Changes

- 为 Issue 文档包定义状态字段角色边界：`trace.md` 继续作为机器事实源，主文档和验收文档必须能表达当前状态或明确派生语义。
- 扩展 Workflow Sync，使常规状态变化事件能同步 `requirement.md`、`bug.md`、`acceptance.md` 等子文档摘要状态。
- 为 `acceptance.md` 或等价验收结果文档建立验收结论、证据、失败项和来源回填契约。
- 增强 `sync-workflow-status.py --check` 或等价 drift check，覆盖子文档状态、目录阶段、registry、验收结论和 close-time 中间态残留。
- 为历史 archive 漂移提供受控治理流程：scan → classify → dry-run → human confirmation → apply → check。
- 更新 req/bug/opsx/sprint 相关 Skill、规则文档和测试，避免命令成功路径继续遗留子文档状态漂移。

## Capabilities

### New Capabilities

- _None_

### Modified Capabilities

- `agent-workflow-tooling`: 增强工作流命令、Workflow Sync、Issue 归档门禁和 Sprint close 检查对子文档状态、验收结果和 drift 报告的要求。

## Impact

- Affected scripts: `scripts/sync-workflow-status.py`、`scripts/workflow_sync/**`、`scripts/promote-issues-for-archive.py`、可能新增的 issue drift scan/check 脚本。
- Affected workflow docs/skills: `rules/document-governance.md`、`rules/requirement-management.md`、`rules/bug-management.md`、`rules/issues-lifecycle.md`、`.agents/skills/{req,bug,opsx,sprint}-*/SKILL.md`、`.agents/skills/workflow-sync/SKILL.md`。
- Affected tests: workflow sync、issue residual、archive readiness、Sprint close stale scan 相关 pytest。
- API impact: none.
- Database impact: none.
- Web / miniapp runtime impact: none.
- Orval impact: none.
- Docker Compose verification: not required unless later implementation changes test/runtime dependencies.
