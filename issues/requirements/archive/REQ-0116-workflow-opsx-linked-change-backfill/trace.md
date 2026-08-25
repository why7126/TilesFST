---
requirement_id: REQ-0116-workflow-opsx-linked-change-backfill
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-08-22 14:18:08
updated_at: 2026-08-22 14:56:06
lifecycle:
  captured: 2026-08-22 14:18:08
  generated: 2026-08-22 14:21:37
  completed: 2026-08-22 14:27:46
  reviewed: 2026-08-22 14:32:36
  approved: 2026-08-22 14:32:36
iteration: sprint-025
openspec_changes:
  - change_id: update-workflow-opsx-linked-change-backfill
    type: update
    status: archived
related_requirements: []
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-024-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-023-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-022-retrospective.md
cross_cutting_tags:
  - workflow-sync
  - agent-workflow-tooling
related_bugs: []
related_changes:
  - update-workflow-opsx-linked-change-backfill
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0116-workflow-opsx-linked-change-backfill
requirement_name: workflow-opsx-linked-change-backfill
requirement_type: 流程治理 / Workflow Sync
priority: P1
status: done
owner: product
source: 用户反馈 + /explore 只读分析
target_clients:
  web_admin: 不涉及
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
related_requirements: []
related_changes:
  - update-workflow-opsx-linked-change-backfill
lifecycle:
  captured: 2026-08-22 14:18:08
  generated: 2026-08-22 14:21:37
  completed: 2026-08-22 14:27:46
  reviewed: 2026-08-22 14:32:36
  approved: 2026-08-22 14:32:36
iteration: sprint-025
openspec_changes:
  - change_id: update-workflow-opsx-linked-change-backfill
    type: update
    status: archived
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-024-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-023-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-022-retrospective.md
knowledge_base_cross_cutting_report:
  - tag: N/A
    ref: null
    ac_count: 0
readiness: Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance 与 trace；本需求为纯 workflow 治理，不涉及 UI 横切 AC。
expected_openspec_change: update-workflow-opsx-linked-change-backfill
cross_cutting_tags:
  - workflow-sync
  - agent-workflow-tooling
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - trace.md
retrospective_summary: sprint-024、sprint-023、sprint-022 复盘均指出 Workflow Sync 派生块正确时，人写说明区、验收报告或当前态入口仍可能残留旧语义；本需求应把 linked Change 自动回填沉到脚本并提供 focused drift 检查。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-22 14:55:53 | lifecycle-stage-migrate | review → archive（/opsx-archive update-workflow-opsx-linked-change-backfill） |
| 2026-08-22 14:55:47 | /opsx-archive | Change `update-workflow-opsx-linked-change-backfill` 已归档，状态同步完成。 |
| 2026-08-22 14:52:19 | /opsx-apply | Change `update-workflow-opsx-linked-change-backfill` 实现完成并进入归档前复核。 |
| 2026-08-22 14:42:30 | `/req-opsx` | 创建 linked OpenSpec Change `update-workflow-opsx-linked-change-backfill`，并回填 REQ 追踪状态。 |
| 2026-08-22 14:35:45 | `/sprint-propose` | 纳入 `sprint-025` 正式范围，完成迭代范围登记。 |
| 2026-08-22 14:33:07 | lifecycle-stage-migrate | plan → review（/req-review） |
| 2026-08-22 14:32:36 | `/req-review` | 默认评审通过，需求状态更新为 `approved`，待纳入 Sprint。 |
| 2026-08-22 14:27:46 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 trace 扩展信息；Knowledge-base gate 为 N/A。 |
| 2026-08-22 14:21:37 | `/req-generate` | 生成 `requirement.md`，需求状态更新为 `draft`。 |
| 2026-08-22 14:18:08 | `/capture` | 记录增强 `req.opsx` 与 `bug.opsx` linked Change 自动回填的治理需求。 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-08-22 14:55:47 workflow-sync：状态同步为 done（Change archived）
