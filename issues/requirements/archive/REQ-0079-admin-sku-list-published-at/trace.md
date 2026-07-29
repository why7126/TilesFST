---
requirement_id: REQ-0079-admin-sku-list-published-at
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-28 22:37:35
updated_at: 2026-07-29 07:54:54
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0079-admin-sku-list-published-at
requirement_name: admin-sku-list-published-at
requirement_type: 管理端 / 瓷砖 SKU / 列表字段展示
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
related_changes:
  - update-admin-sku-list-published-at
lifecycle:
  captured: 2026-07-28 22:37:35
  generated: 2026-07-28 22:43:17
  completed: 2026-07-28 22:46:01
  reviewed: 2026-07-28 22:50:27
  approved: 2026-07-28 22:50:27
iteration: sprint-013
openspec_changes:
  - change_id: update-admin-sku-list-published-at
    type: update
    status: archived
readiness: Ready
readiness_notes: 五件套已补齐，UI 原型策略已落地；已写入 admin-list 横切 AC，后续可进入 /req-review。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/web/prototype-context.md
  - prototype/web/admin-sku-list-published-at.html
expected_openspec_change: update-admin-sku-list-published-at
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-012-retrospective.md
cross_cutting_tags:
  - web-admin
  - admin-list
  - tile-sku
knowledge_base_summary: 已将管理端列表页分页 DOM、fixed toast、危险操作 DS confirm、禁止 window.confirm 等 gate 转化为 5 条 AC-XCUT；Sprint-012 复盘提醒管理端宽表与长文本需继续复用 admin-list 最佳实践并控制横切验收范围。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-29 07:54:22 | lifecycle-stage-migrate | review → archive（/opsx-archive update-admin-sku-list-published-at） |
| 2026-07-29 07:53:57 | /opsx-archive | Change `update-admin-sku-list-published-at` 已归档，状态同步完成。 |
| 2026-07-28 23:15:51 | /opsx-apply | Change `update-admin-sku-list-published-at` apply 完成，待 archive。 |
| 2026-07-28 23:03:00 | `/sprint-propose` | 纳入 sprint-013 正式范围，关联 Change `update-admin-sku-list-published-at`。 |
| 2026-07-28 22:57:10 | `/req-opsx` | 创建 OpenSpec Change `update-admin-sku-list-published-at`，状态为 proposed。 |
| 2026-07-28 22:51:06 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-28 22:50:27 | `/req-review --approve` | 需求评审通过，状态更新为 approved，计划迁移到 review 阶段目录。 |
| 2026-07-28 22:46:01 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 prototype/web；写入 admin-list 横切 AC，状态更新为 pending_review。 |
| 2026-07-28 22:43:17 | `/req-generate` | 生成 requirement.md，状态更新为 draft。 |
| 2026-07-28 22:37:35 | `/req-capture` | 记录管理端瓷砖 SKU 列表新增发布时间列需求。 |

- 2026-07-29 07:53:54 workflow-sync：状态同步为 done（Change archived）
