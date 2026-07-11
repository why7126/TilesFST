## Why

Sprint 005 复盘显示，`/sprint-exps` 需要人工读取 Sprint 四件套、Issue trace、OpenSpec tasks 与归档材料后才能整理 Fact Sheet，导致高输入 token 消耗和重复检索。现在已有 `workflow_sync.collect` 与 Sprint archive readiness gate，可将这些机器事实前置聚合，减少复盘命令对长文档全文读取的依赖。

## What Changes

- 为 `/sprint-exps` 增加自动 Sprint Fact Sheet 生成能力，优先用脚本汇总 Sprint、REQ、BUG、Change、tasks、trace 与验收关键事实。
- 新增短小、可复用的 Fact Sheet 输出，作为 `/sprint-exps` 的优先读取入口；只有发现风险或证据不足时才回读具体原文片段。
- 复用现有 Sprint 路径解析、Issue/Change 收集与 tasks 计数逻辑，避免重复实现会漂移的解析规则。
- 在 Fact Sheet 中标记 token 风险来源、建议回读路径和缺失/不一致项，支持复盘中的“模型 Token 使用分析”章节。
- 不改变业务功能、API、数据库、Web、小程序或管理端运行逻辑。

## Capabilities

### New Capabilities

- `agent-workflow-tooling`: 覆盖项目级 Agent 工作流命令、上下文预算、Sprint 复盘事实摘要与工具链输出边界。

### Modified Capabilities

- 无。

## Impact

- 影响 `.agents/skills/source-command-sprint-exps/SKILL.md` 的读取流程和 Fact Sheet 约束。
- 影响 `scripts/` 下 Sprint/Workflow 相关辅助脚本，预计新增 `scripts/generate-sprint-fact-sheet.py` 或等价脚本。
- 可能复用或轻微调整 `scripts/workflow_sync/collect.py` 与 `scripts/validate-sprint-archive-readiness.py` 中的收集逻辑。
- 需要补充脚本级测试或至少用已归档 Sprint 样例验证输出。
- 不影响 API、数据库、Orval、Docker Compose、Web、小程序、管理端业务代码。
