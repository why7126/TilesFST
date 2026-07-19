## Why

Workflow Sync 与 AI usage post-command hook 已经具备摘要输出方向，但多个命令成功路径仍容易把无变化文件、派生块、snapshot 或 hook 细节打印成较长日志，增加模型上下文消耗和人工扫读成本。现在需要把 compact summary 输出固化为可验收的 Change，确保成功路径默认短、失败路径仍可诊断。

## What Changes

- 将 Workflow Sync 成功路径默认输出收敛为聚合摘要，压缩 `updated`、`skipped`、`errors`、Sprint 解析与 focus 对象信息。
- 为 Workflow Sync 保留显式详细输出模式，仅在调试、drift 或错误定位时展示逐文件明细。
- 将 AI usage post-command hook 的成功、降级和不可用输出统一为 compact summary 字段集合。
- 约束命令技能和调用方只向用户转述 compact summary，不默认打印完整 JSON、session、snapshot、工具日志或大 diff。
- 补充针对成功路径降噪、失败路径诊断和 hook 降级场景的测试。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `agent-workflow-tooling`: 明确 Workflow Sync 与 AI usage post-command hook 的 compact summary 输出契约、默认成功路径降噪规则和详细输出保留策略。

## Impact

- 影响脚本：`scripts/sync-workflow-status.py`、`scripts/workflow_sync/engine.py`、`scripts/extract-ai-usage.py`、`scripts/ai_usage.py`。
- 影响技能：`.agents/skills/workflow-sync/SKILL.md` 以及调用 Workflow Sync / AI usage hook 的 req、bug、opsx、sprint、release 技能说明。
- 影响测试：新增或更新 Workflow Sync 报告输出、AI usage hook JSON/摘要字段、成功路径日志长度和失败路径诊断覆盖。
- 不影响业务 API、数据库表结构、Web 前端、小程序、Orval 或 Docker Compose 部署。
