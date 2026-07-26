## Context

`scripts/generate-sprint-fact-sheet.py` 负责为 `/sprint-exps` 提供读前摘要，当前结构化数据已经包含 `warnings`、`needs_detail`、`token_risks` 与 `evidence_hints`。现有 CLI 只有完整 Markdown 与完整 JSON 两种输出，导致复盘默认路径容易把完整 evidence hints 作为上下文输入或输出，而不是把它作为按需回读索引。

## Goals / Non-Goals

**Goals:**

- 提供面向复盘默认路径的紧凑 `summary` 输出，避免成功路径输出完整 evidence hints。
- 提供 `fields` 输出，支持按字段路径精确取回 `evidence_hints`、`warnings`、`ai_usage_snapshot` 等细节。
- 保持现有 `--json` 完整机器可读输出和默认 Markdown 输出兼容。
- 让测试覆盖 CLI 输出边界，防止后续回退到复盘默认长输出。

**Non-Goals:**

- 不重构 Fact Sheet 的事实采集逻辑。
- 不改变 Sprint、Issue、OpenSpec Change 或 AI usage snapshot 的数据模型。
- 不修改 `/sprint-exps` Skill 主流程以外的工作流命令。
- 不引入新依赖或外部服务。

## Decisions

1. 新增显式输出模式而不是压缩现有 `--json`。
   - 决策：保留 `--json` 输出完整 `fact_sheet`，新增独立的 summary/fields 参数或等价 CLI 模式。
   - 原因：现有测试和调试流程依赖完整 JSON；改变 `--json` 语义会制造不必要的兼容风险。
   - 备选：让 `--json` 默认变短，再加 `--full-json`。该方式破坏现有调用方预期，暂不采用。

2. `summary` 应复用同一份 `fact_sheet` 数据后裁剪。
   - 决策：先构建完整内部事实对象，再渲染 summary，避免维护两套采集逻辑。
   - 原因：输出模式只改变暴露边界，不应改变事实源判断。
   - 备选：为 summary 单独采集精简数据。该方式会增加状态不一致风险。

3. `fields` 使用字段路径选择而不是新增多个专用 flag。
   - 决策：支持类似 `evidence_hints`、`warnings`、`ai_usage_snapshot.totals` 的字段路径，输出结构化 JSON。
   - 原因：未来复盘可按需读取新增字段，不需要每个字段新增 CLI 参数。
   - 备选：新增 `--evidence-hints`、`--warnings` 等 flag。该方式短期简单，但扩展性较弱。

4. `/sprint-exps` 默认消费 summary，遇到风险再取 fields。
   - 决策：复盘默认读取 summary；当 `needs_detail` 为 true、存在 warning/missing/inconsistent 类风险，或用户要求细节时，再调用 fields 获取 `evidence_hints` 并片段回读原始文件。
   - 原因：符合上下文预算治理，且保留证据可追溯性。

## Risks / Trade-offs

- [Risk] 字段路径解析过宽导致输出大量嵌套内容。→ Mitigation：测试覆盖 `evidence_hints` 精确读取，并在帮助文本中引导按顶层或明确子路径使用。
- [Risk] summary 裁剪过度导致复盘无法判断是否需要细节。→ Mitigation：summary 必须保留 `needs_detail`、warnings 计数/摘要、token risks 与 AI usage 状态。
- [Risk] 默认 Markdown 仍包含完整 evidence hints。→ Mitigation：保持人工默认 Markdown 兼容，但 `/sprint-exps` 默认改用 summary；同时测试 summary 不含完整 evidence hints 表。
- [Risk] 调用方混淆完整 JSON 与 fields 输出。→ Mitigation：CLI 测试覆盖 `--json` 完整输出不变，以及 fields 输出可独立解析。
