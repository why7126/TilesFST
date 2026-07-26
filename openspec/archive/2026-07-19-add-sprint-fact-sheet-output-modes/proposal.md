## Why

`generate-sprint-fact-sheet.py` 当前只有完整 JSON 与完整 Markdown 输出，`/sprint-exps` 在成功路径容易接收完整 `evidence_hints` 表，削弱 Fact Sheet 原本用于节省上下文的价值。现在需要让复盘默认读取更短摘要，并在确实需要回读证据时按字段显式取用。

## What Changes

- 为 `generate-sprint-fact-sheet.py` 增加 `summary` 输出模式，默认面向 `/sprint-exps` 提供 Sprint、scope、warnings、AI usage、token risks 等紧凑摘要。
- 为脚本增加 `fields` 输出模式，允许调用方按字段路径选择性输出如 `evidence_hints`、`warnings`、`ai_usage_snapshot` 等内容。
- 调整复盘消费约束：`/sprint-exps` 默认不得输出完整 `evidence_hints`，仅在 `needs_detail`、warning、missing、inconsistent 或用户显式要求时读取或展示对应 evidence hints。
- 保留现有完整 JSON 与完整 Markdown 能力，避免破坏现有调试和人工审阅路径。
- 补充脚本单元测试与 CLI 测试，覆盖 summary 默认不含完整 evidence hints、fields 可精确取回 evidence hints、JSON 兼容性不回退。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `agent-workflow-tooling`: 调整 Sprint Fact Sheet 输出模式与 `/sprint-exps` 默认 evidence hints 消费边界。

## Impact

- 影响代码：`scripts/generate-sprint-fact-sheet.py`。
- 影响测试：`tests/test_generate_sprint_fact_sheet.py`。
- 影响 OpenSpec：修改 `agent-workflow-tooling` delta spec。
- 不影响 API、数据库、Web、微信小程序、对象存储、Orval 或 Docker Compose。
