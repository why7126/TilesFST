---
bug_id: BUG-0052-api-docs-metric-cards-inconsistent
status: done
lifecycle_stage: archive
severity: medium
created_at: 2026-07-01 09:09:32
updated_at: 2026-07-04 08:16:02
---

# 缺陷追踪

## 基本信息

```yaml
bug_id: BUG-0052-api-docs-metric-cards-inconsistent
bug_name: api-docs-metric-cards-inconsistent
severity: medium
status: done
owner: product
source: 用户反馈
environment: local
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
related_requirement: REQ-0022-admin-api-docs-menu
related_bug: null
related_changes:
  - fix-api-docs-metric-cards-inconsistent
lifecycle:
  captured: 2026-07-01 09:09:32
  generated: 2026-07-01 09:24:38
  enriching: 2026-07-01 13:54:17
  completed: 2026-07-01 13:54:17
  pending_review: 2026-07-01 13:54:17
  reviewed: 2026-07-01 14:01:11
  approved: 2026-07-01 14:01:11
iteration: sprint-004
openspec_changes:
  - change_id: fix-api-docs-metric-cards-inconsistent
    type: fix
    status: archived
readiness: Archived
readiness_notes: 已完成 `/opsx-apply` 与 `/opsx-archive`，OpenSpec Change `fix-api-docs-metric-cards-inconsistent` 已归档。
documents:
  - capture.md
  - bug.md
  - root-cause.md
  - workaround.md
  - acceptance.md
  - review.md
expected_openspec_change: fix-api-docs-metric-cards-inconsistent
```

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-07-02 09:04:24 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-api-docs-metric-cards-inconsistent） |
| 2026-07-02 09:04:16 | workflow-sync | 状态同步为 done（Change archived） |
| 2026-07-01 20:33:50 | `/bug-opsx` | 创建 OpenSpec Change `fix-api-docs-metric-cards-inconsistent`，状态 proposed |
| 2026-07-01 14:04:19 | `/sprint-propose` | 纳入 sprint-004，待 /bug-opsx 创建修复 Change |
| 2026-07-01 14:01:55 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-01 14:01:11 | `/bug-review` | 评审通过，确认进入常规修复流程 |
| 2026-07-01 13:54:17 | `/bug-complete` | 补齐根因分析、临时规避、验收标准，状态进入 pending_review |
| 2026-07-01 09:24:38 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-07-01 09:09:32 | `/capture` | 记录接口文档页指标卡与瓷砖 SKU 页样式不一致 |
