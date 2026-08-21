---
created_at: 2026-08-12 10:30:00
updated_at: 2026-08-12 10:30:00
---

# 测试计划

## 脚本验证

- 使用现有 Sprint snapshot 运行 `python scripts/generate-sprint-fact-sheet.py --sprint <sprint-id> --summary`，确认 summary 暴露 fresh gate 与矩阵写入 gate。
- 构造临时 stale snapshot，运行 `--ai-usage-markdown`，确认输出 blocker 指引且不输出矩阵表。

## 治理校验

- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `openspec validate strengthen-sprint-exps-ai-usage-fresh-gate`
