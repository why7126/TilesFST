---
created_at: 2026-08-12 10:30:00
updated_at: 2026-08-12 14:27:27
---

# 验收记录

## 验收要点

- 复盘前自动提示或输出刷新 snapshot 的 recommended action。
- 刷新 snapshot 后必须重新运行 Fact Sheet summary 复核 fresh gate。
- 未通过 fresh gate 时，`--ai-usage-markdown` 不输出真实 token 矩阵。
- fresh gate pass 后，`--ai-usage-markdown` 可输出 Token Usage Fact Sheet 与四张矩阵。

## 验收结果

- `python scripts/generate-sprint-fact-sheet.py --sprint sprint-023 --summary`：通过；`usage_matrices_summary.raw_present=true` 但 `available=false`，`matrix_write_gate.status=blocker`。
- `python scripts/generate-sprint-fact-sheet.py --sprint sprint-023 --ai-usage-markdown`：通过；输出 blocker、recommended action 和刷新后重新 summary 指引，未输出四张真实矩阵。
- `python scripts/validate-sprint-scope.py sprint-023 --item strengthen-sprint-exps-ai-usage-fresh-gate`：通过。
