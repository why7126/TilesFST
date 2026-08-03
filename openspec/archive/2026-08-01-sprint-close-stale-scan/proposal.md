## Why

Sprint 收尾与归档前仍可能在四件套中残留中间态文案，例如已创建或已归档 Change 仍显示“待 `/req-opsx` / `/bug-opsx` / `/opsx-apply`”，也可能继续引用历史旧路径 `openspec/changes/archive/`。这些残留会让 Sprint 关闭结论、复盘事实和后续自动化判断互相冲突，因此需要在 Sprint close 阶段增加自动 stale scan 门禁。

## What Changes

- 为 Sprint close / archive 前置或后置校验增加四件套 stale scan，覆盖 `sprint.md`、`release-note.md`、`acceptance-report.md` 和 `sprint.yaml`。
- 自动识别已不应出现的中间态文案，包括已创建 Change 后仍提示待 `/req-opsx` 或 `/bug-opsx`、已 apply/archived 后仍提示待 `/opsx-apply`、已归档 Change 仍显示 proposed/applied 待处理语义等。
- 自动识别旧归档路径 `openspec/changes/archive/` 的真实目录、派生事实、报告文本或新生成引用；仅允许迁移工具、兼容读取和测试 fixture 中作为 legacy 字符串存在。
- stale scan 发现阻断项时返回非零退出码，并输出文件路径、命中片段、判定原因和建议修复命令。
- Workflow Sync 或 Sprint close 相关脚本在刷新四件套时不得保留过期规划文案；修复后应可重复运行且保持幂等。
- 补充聚焦回归测试，覆盖 stale scan 命中、允许的 legacy 例外、Workflow Sync 派生块刷新和 Sprint close 门禁失败路径。

## Capabilities

### New Capabilities

- 无

### Modified Capabilities

- `sprint-planning-governance`: 增加 Sprint close stale scan 的归档门禁要求，确保四件套状态文案与真实 Change/Issue 生命周期一致。
- `agent-workflow-tooling`: 增加命令脚本的 stale scan 输出、例外边界和可执行修复建议要求。
- `testing`: 增加 Sprint close stale scan 与旧归档路径残留的回归测试契约。

## Impact

- 影响脚本与工作流：`scripts/sync-workflow-status.py`、`scripts/workflow_sync/**`、Sprint archive/close 相关校验脚本，可能新增专用 stale scan 脚本或扩展现有 validator。
- 影响文档与规范：按需更新 `rules/document-governance.md`、`rules/iterations-lifecycle.md`、`rules/directory-structure.md` 或相关 workflow skill，明确 stale scan 门禁与允许例外。
- 影响测试：新增或更新 pytest，覆盖 Sprint 四件套 fixture、legacy archive path 例外、Workflow Sync 刷新结果和失败报告。
- 不影响业务 API、数据库结构、Web 管理端、店主端、小程序、MinIO 上传链路或 Orval 生成物。
