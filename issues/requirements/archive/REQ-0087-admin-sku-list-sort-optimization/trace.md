---
requirement_id: REQ-0087-admin-sku-list-sort-optimization
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-31 23:53:02
updated_at: 2026-08-01 08:20:30
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0087-admin-sku-list-sort-optimization
requirement_name: admin-sku-list-sort-optimization
requirement_type: 管理端 / SKU 列表排序优化
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
related_requirements:
  - REQ-0006-tile-sku-management
  - REQ-0079-admin-sku-list-published-at
related_bugs:
  - BUG-0090-admin-sku-list-publish-sort-order
related_changes: []
lifecycle:
  captured: 2026-07-31 23:53:02
  generated: 2026-08-01 07:05:30
  completed: 2026-08-01 07:11:09
  reviewed: 2026-08-01 07:18:18
  approved: 2026-08-01 07:18:18
iteration: sprint-016
openspec_changes:
  - change_id: update-admin-sku-list-sort-optimization
    type: update
    status: archived
readiness: Ready
readiness_notes: 已基于 capture.md 与 requirement.md 补齐用户故事、业务流程、验收标准、trace 和 prototype/web；命中 admin-list 横切标签，已将管理端列表页一致性 best-practice 转化为 AC-XCUT。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - prototype/web/context.md
  - prototype/web/admin-sku-list-sort-optimization.html
  - review.md
  - trace.md
expected_openspec_change: update-admin-sku-list-sort-optimization
cross_cutting_tags:
  - web-admin
  - sku-list
  - sorting
  - admin-list
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-015-retrospective.md
knowledge_base_gate: Pass
knowledge_base_notes: 本 REQ 为管理端 SKU 列表排序优化，命中 admin-list；已读取列表页一致性 best-practice 与 sprint-015 管理端筛选下拉复盘，验收标准中写入分页 DOM、指标卡、筛选下拉、fixed toast、DS confirm/window.confirm 横切 AC。
cross_cutting_report:
  - tag: admin-list
    refs:
      - docs/knowledge-base/best-practices/admin-list-page-consistency.md
      - docs/knowledge-base/retrospectives/sprint-015-retrospective.md
    ac_count: 6
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-01 08:20:02 | lifecycle-stage-migrate | review → archive（/opsx-archive update-admin-sku-list-sort-optimization） |
| 2026-08-01 08:19:32 | /opsx-archive | Change `update-admin-sku-list-sort-optimization` 已归档，状态同步完成。 |
| 2026-08-01 07:50:41 | /opsx-modify | Change `update-admin-sku-list-sort-optimization` 验收返修已同步，待复验或 archive。 |
| 2026-08-01 07:42:20 | /opsx-apply | Change `update-admin-sku-list-sort-optimization` apply 完成，待 archive。 |
| 2026-08-01 07:31:37 | `/sprint-propose` | 纳入 sprint-016 正式范围，关联 Change `update-admin-sku-list-sort-optimization` |
| 2026-08-01 07:25:59 | `/req-opsx` | 校正状态：Change 已 proposed，但 REQ 尚未纳入 Sprint，保持 approved，待 /sprint-propose 后再进入 in_sprint |
| 2026-08-01 07:22:21 | `/req-opsx` | 创建 OpenSpec Change `update-admin-sku-list-sort-optimization`，状态 proposed |
| 2026-08-01 07:18:55 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-08-01 07:18:18 | `/req-review --approve` | 需求评审通过；确认后续可进入 /req-opsx 与 Sprint 规划 |
| 2026-08-01 07:11:09 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 prototype/web；命中 admin-list 横切标签并写入 6 条 AC-XCUT，状态更新为 pending_review |
| 2026-08-01 07:05:30 | `/req-generate` | 基于 capture.md 生成 requirement.md，状态更新为 draft |
| 2026-07-31 23:53:02 | `/capture` | 记录管理端 SKU 列表排序优化需求，状态为 captured |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0090-admin-sku-list-publish-sort-order | medium | done | null | Web 端瓷砖 SKU 列表曾存在未按发布与创建时间排序的偏差，本需求在此基础上细化默认排序策略 |
- 2026-08-01 08:19:13 workflow-sync：状态同步为 done（Change archived）
