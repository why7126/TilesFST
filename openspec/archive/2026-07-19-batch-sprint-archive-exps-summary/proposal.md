## Why

当一个 Sprint 包含 10 个以上 OpenSpec Change 时，`/sprint-archive` 与 `/sprint-exps` 容易为了确认 tasks、trace、验收和复盘证据而一次性读取大量文件，造成上下文峰值过高、输出噪音增加，并提高遗漏阻断项的风险。
现有 Fact Sheet 已提供聚合摘要能力，但还缺少针对大 Sprint 的分批 archive/exps 摘要契约，无法明确要求命令按批次处理和复用批次摘要。

## What Changes

- 为 10+ Change 的大 Sprint 定义分批摘要机制：按 Sprint scope 中的 Change 顺序或依赖顺序拆分为固定上限的批次。
- `/sprint-archive` 在 readiness、archive queue、close 前检查中 MUST 优先生成并消费批次摘要，避免一次性展开全部 Change 的 `tasks.md` 与 `trace.md`。
- `/sprint-exps` 在复盘大 Sprint 时 MUST 优先消费 Sprint Fact Sheet 与批次摘要，按 warnings/evidence hints 回读必要片段。
- Fact Sheet 或辅助脚本 MUST 输出机器可读的 batch summary，覆盖批次范围、完成度、阻断项、warnings、证据路径和 token 风险。
- 成功路径输出保持 compact summary；失败路径保留能定位具体 Change、批次和文件的诊断信息。

## Capabilities

### New Capabilities

### Modified Capabilities

- `agent-workflow-tooling`: 增加大 Sprint 分批 archive/exps 摘要、批次证据边界和 compact 输出要求。

## Impact

- 影响 `.agents/skills/sprint-archive/SKILL.md`、`.agents/skills/sprint-exps/SKILL.md` 的读取顺序、输出契约和大 Sprint 门禁说明。
- 可能影响 `scripts/generate-sprint-fact-sheet.py`、`scripts/validate-sprint-archive-readiness.py` 或新增/复用辅助脚本，用于生成 batch summary。
- 需要补充脚本/流程测试，覆盖 10+ Change Sprint、批次 warning、失败诊断和 compact 输出。
- 不影响业务 API、数据库结构、Web/小程序/管理端页面、Orval 或 Docker Compose 配置。
