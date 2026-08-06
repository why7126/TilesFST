---
bug_id: BUG-0118-fact-sheet-ai-usage-future-start-date-freshness
created_at: 2026-08-06 08:41:59
updated_at: 2026-08-06 08:42:36
---

# 临时规避方案

## 当前可用规避

在代码修复前，Sprint 复盘或 Fact Sheet 消费方不要仅以 `python scripts/generate-sprint-fact-sheet.py --sprint sprint-020 --summary` 中的 `snapshot_status: stale` 作为最终判断。

可临时使用独立 snapshot check 验证 AI usage snapshot：

```bash
python3 scripts/extract-ai-usage.py --check-snapshot --sprint sprint-020 --json
```

当独立 snapshot check 显示 `snapshot_status: present`、`usage_mode: actual`、`fresh_gate.status: pass`，且 `totals`、`coverage`、`usage_matrices` 完整时，可在复盘文档中明确标注“Fact Sheet summary 已知误报 BUG-0118”，并引用独立 snapshot check 作为真实 token 成本矩阵证据。

## 不建议规避

- 不建议为了绕过 fresh gate 临时修改 `iterations/archive/sprint-020/sprint.yaml` 的 `start_date`，这会污染 Sprint 事实源。
- 不建议将完整 snapshot 强行改为 estimated 或删除 freshness baseline，这会掩盖真实数据质量问题。
- 不建议手工编辑生成的 Fact Sheet summary 字段，除非同时保留独立 snapshot check 证据。

## 修复前风险

使用临时规避时，必须显式记录证据来源与 BUG 编号，避免后续读者误以为 Fact Sheet summary 与独立 snapshot check 都已一致。
