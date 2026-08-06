---
bug_id: BUG-0118-fact-sheet-ai-usage-future-start-date-freshness
review_result: approved
reviewed_at: 2026-08-06 08:44:50
reviewer:
created_at: 2026-08-06 08:44:50
updated_at: 2026-08-06 08:44:50
---

# 缺陷评审

## 评审结论

结论：`approved`，确认需要修复。

该缺陷已具备进入 `/bug-opsx` 与 Sprint 规划的条件。当前不需要 hotfix 路径，可按标准 OpenSpec Change 修复 Fact Sheet AI usage freshness baseline 判定。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | `sprint-020` 的未来 `start_date` 与 Fact Sheet baseline 误判链路清晰。 |
| 严重等级合理 | 通过 | `medium` 合理；不影响业务运行，但影响 Sprint 复盘与 AI usage 成本矩阵可信度。 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖未来 `start_date` 跳过、非未来 baseline 保持生效与 `sprint-020` 回归。 |
| 是否需 hotfix 路径 | 不需要 | 属于治理报表/复盘准确性问题，可进入常规修复流程。 |

## 后续动作

- 允许执行 `/bug-opsx BUG-0118` 创建修复 Change。
- 允许纳入 Sprint 正式规划。
