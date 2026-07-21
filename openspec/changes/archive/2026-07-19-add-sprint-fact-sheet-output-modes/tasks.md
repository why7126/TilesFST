## 1. CLI 输出模式

- [x] 1.1 为 `scripts/generate-sprint-fact-sheet.py` 增加 summary 输出模式或等价参数，保持现有默认 Markdown 与 `--json` 完整输出兼容。
- [x] 1.2 为 `scripts/generate-sprint-fact-sheet.py` 增加 fields 输出模式或等价参数，支持请求一个或多个字段路径。
- [x] 1.3 更新 CLI 帮助文本与参数校验，确保未知字段路径返回非零退出码和可读错误信息。

## 2. 输出裁剪与字段选择

- [x] 2.1 实现 summary 构建函数，输出 Sprint 基础信息、scope 计数、warnings 摘要、`needs_detail`、AI usage 状态和 token risks。
- [x] 2.2 确保 summary 默认不包含完整 `evidence_hints` 明细，但保留 evidence hint 计数或需要回读的信号。
- [x] 2.3 实现字段路径选择函数，支持获取 `evidence_hints`、`warnings`、`ai_usage_snapshot` 及必要子字段。
- [x] 2.4 保持完整 JSON 输出仍包含现有 `evidence_hints`、`warnings`、`token_risks` 等字段。

## 3. 复盘消费边界

- [x] 3.1 更新 `/sprint-exps` 相关技能或说明，使复盘默认调用 summary 输出。
- [x] 3.2 明确仅在 `needs_detail`、warning、missing、inconsistent 或用户显式要求时，通过 fields 模式读取完整 `evidence_hints`。
- [x] 3.3 确保复盘输出不得把旧路径残留 evidence hint 当作新的证据链接传播。

## 4. 测试与校验

- [x] 4.1 补充单元测试：summary 包含关键状态与风险摘要，且默认不包含完整 `evidence_hints`。
- [x] 4.2 补充 CLI 测试：fields 可单独输出 `evidence_hints` 且为可解析 JSON。
- [x] 4.3 补充兼容测试：`--json` 完整输出结构保持可解析且仍包含 `evidence_hints`。
- [x] 4.4 运行 `pytest tests/test_generate_sprint_fact_sheet.py`。
- [x] 4.5 运行 OpenSpec 校验，确认 delta spec 与 tasks 可被解析。

## 归档验证摘要

- 验证命令：`pytest tests/test_generate_sprint_fact_sheet.py`，验证结果：pass，16 passed。
- 验证命令：`openspec validate add-sprint-fact-sheet-output-modes --strict`，验证结果：pass。
- 验收结论：通过；summary/fields 输出模式已实现，复盘默认不输出完整 `evidence_hints`。
- Issue/Sprint 状态：无关联 REQ/BUG；Workflow Sync 报告 Sprint skipped，reason 为 change not in sprint scope。
- 归档路径：`openspec/changes/archive/2026-07-19-add-sprint-fact-sheet-output-modes/`。
