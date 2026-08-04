## 背景

部分历史已归档 Change 缺少 `trace.md`，会让 `/opsx-archive`、Sprint close readiness、Workflow Sync 或复盘工具缺少归档证据入口。现在需要在不破坏历史归档目录的前提下，为缺失 trace 的归档 Change 自动补齐最小可追溯证据，或在无法写入时提供结构化 fallback 摘要，避免人工临时判断。

## 变更内容

- 为已归档 Change 增加缺失 `trace.md` 的自动修复能力：优先生成最小归档 trace，记录 Change ID、归档路径、归档状态、可推断归档时间、任务完成摘要和证据来源。
- 当归档目录不可写、证据不足或历史文件结构无法安全推断时，输出结构化 fallback 摘要，字段足以支撑归档证据校验、Sprint close readiness 和人工复核。
- 调整归档证据校验与相关工作流工具，使其识别“trace present”“auto generated minimal trace”“structured fallback summary”三种闭环证据状态。
- 补充聚焦回归测试，覆盖缺失 trace 的历史归档 Change、不可写或不可推断场景、以及仍应阻断的无证据场景。
- 不引入破坏性变更；不改变 canonical archive path，仍以 `openspec/archive/YYYY-MM-DD-<change-id>/` 为准。

## 能力范围

### 新增能力

- 无。

### 修改能力

- `agent-workflow-tooling`：扩展归档 Change 证据治理能力，要求工具在已归档 Change 缺少 `trace.md` 时自动生成最小归档 trace，或输出结构化 fallback 摘要作为可校验证据。

## 影响范围

- 可能影响 `.agents/skills/opsx-archive/SKILL.md`、`scripts/validate-archive-evidence.py`、`scripts/sync-workflow-status.py`、`scripts/workflow_sync/**`、Sprint close readiness 或 Fact Sheet 相关脚本。
- 需要补充或更新 pytest，重点覆盖归档证据校验、Workflow Sync 归档时间解析和 Sprint close readiness 对缺失 trace 的处理。
- 不影响业务 API、数据库表结构、Web 前端、微信小程序、MinIO 或 Orval 生成物。
