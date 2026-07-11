## Why

当前 Issue 归档门禁能发现子文档残留 `draft`、`pending_review`、`applied` 等未闭环状态，但修复路径仍依赖人工逐个打开 Markdown 批量修改，容易遗漏 frontmatter 与 fenced YAML block 的双写字段。需要将“发现问题”延伸到“可自动同步或给出精确修复命令”，降低 Sprint 归档和 Issue 归档时的机械成本。

## What Changes

- 增强 Issue 子文档状态一致性能力：门禁报告 MUST 给出可直接执行的修复命令，覆盖 REQ/BUG、具体文件、状态来源与目标闭环状态。
- 为 workflow sync 或专用脚本增加 reconcile 模式：在 Issue 主状态和关联 Change 已闭环时，自动同步包内 Markdown 子文档 frontmatter 与 fenced YAML block 的残留状态。
- reconcile MUST 默认支持 dry-run，先报告将修改的文件、字段、旧值与新值；实际写入后刷新文档 `updated_at` 并保持变更记录可追溯。
- reconcile MUST 不绕过评审或验收：当 Issue 主状态、关联 Change 或 Sprint 状态未闭环时，只能报告 blocker，不能把子文档强制改成闭环状态。

## Capabilities

### New Capabilities

- 无

### Modified Capabilities

- `agent-workflow-tooling`: Issue 归档子文档状态一致性门禁增加自动 reconcile 与明确修复命令要求。

## Impact

- 影响 `scripts/sync-workflow-status.py` 或新增/配套工作流状态修复脚本。
- 影响 `.agents/skills/workflow-sync/SKILL.md`、相关 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 技能说明中对子文档残留状态的处理指引。
- 影响 workflow sync / archive promote 的报告输出和测试用例。
- 不影响对外 API、数据库表结构、Web 前端、小程序或 Orval 生成物。
