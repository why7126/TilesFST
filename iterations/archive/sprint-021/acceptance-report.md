---
note: workflow-sync — 10/10 Change 已 archive；0 applied；待人工 sign-off
sprint_id: sprint-021
status: completed
acceptance_status: passed
created_at: 2026-08-06 09:01:00
updated_at: 2026-08-06 17:17:37
---

# Sprint 021 验收报告

## 验收范围

| 类型 | 编号 | 状态 | 验收要点 |
|---|---|---|---|
| REQ | REQ-0102-sprint-goal-scope-consistency-validation | done | 目标编号列表与 Scope 主表一致；缺失项提示具体编号；sprint-020 / REQ-0100 漏列场景可复现 |
| BUG | BUG-0118-fact-sheet-ai-usage-future-start-date-freshness | done | future start_date 不阻塞完整 snapshot；future planned time 进入 skipped；stale updated_at 仍生效；sprint-020 类场景已随 Change 归档闭环 |
| BUG | BUG-0123-openspec-archive-proposal-warning-stdout | done | 中文优先 Change 归档成功输出不展示已知 proposal scaffold warning；未知 stdout/stderr 与失败诊断保留；BUG-0119 不回归 |
| Change | fix-fact-sheet-ai-usage-start-date-freshness | archived | 归档路径：`openspec/archive/2026-08-06-fix-fact-sheet-ai-usage-start-date-freshness/` |

## 横切验收

- [x] `tests/test_generate_sprint_fact_sheet.py` 覆盖 future start_date。
- [x] future start_date / end_date 均进入 skipped，不成为 `min_generated_at` source。
- [x] stale `updated_at` baseline 仍能阻止陈旧 snapshot。
- [x] `sprint-020` 类场景 summary 得到 `actual` / `present`。
- [x] `validate-sprint-scope.py sprint-020 --item REQ-0100-mintlify-docs-site-ia-content-experience` 能发现目标编号列表缺失并输出具体缺失项。
- [x] `scripts/archive-change.sh` 成功路径吸收已知 proposal scaffold warning，但保留未知 stdout/stderr。
- [x] 不输出或保存原始 session JSONL、prompt、系统/开发者指令、本机绝对路径或敏感信息。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-06 17:16:00
accepted_by: sprint-archive
evidence:
  - python3 scripts/validate-sprint-archive-readiness.py --sprint sprint-021
  - python3 scripts/check-sprint-close-stale-scan.py --sprint sprint-021
failed_items: []
notes:
  - 10/10 Change 已归档，107/107 tasks 完成，Sprint close stale scan 0 blocker。
```
