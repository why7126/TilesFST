---
requirement_id: REQ-0121-miniapp-certificate-detail-brand-card-entry
title: 小程序证书详情页品牌入口复用 brand-card
status: done
priority: P1
lifecycle_stage: archive
created_at: 2026-08-24 14:58:45
updated_at: 2026-08-24 17:15:08
lifecycle:
  captured: 2026-08-24 14:58:45
  generated: 2026-08-24 15:02:14
  completed: 2026-08-24 15:26:47
  reviewed: 2026-08-24 15:42:12
  approved: 2026-08-24 15:42:12
iteration: sprint-025
openspec_changes:
  - change_id: update-miniapp-certificate-detail-brand-card-entry
    type: update
    status: archived
related_requirements:
  - REQ-0115-media-multi-variant-images
related_bugs:
  - BUG-0134-miniapp-certificate-detail-display-url
  - BUG-0137-miniapp-lightweight-image-variant-consumption
parent_requirement: REQ-0115-media-multi-variant-images
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md
  - docs/knowledge-base/retrospectives/sprint-024-retrospective.md
cross_cutting_tags: []
readiness: Ready
knowledge_base_gate: N/A
related_changes:
  - update-miniapp-certificate-detail-brand-card-entry
---

# Trace

```yaml
requirement_id: REQ-0121-miniapp-certificate-detail-brand-card-entry
status: done
priority: P1
lifecycle_stage: archive
created_at: 2026-08-24 14:58:45
updated_at: 2026-08-24 17:08:44
lifecycle:
  captured: 2026-08-24 14:58:45
  generated: 2026-08-24 15:02:14
  completed: 2026-08-24 15:26:47
  reviewed: 2026-08-24 15:42:12
  approved: 2026-08-24 15:42:12
iteration: sprint-025
openspec_changes:
  - change_id: update-miniapp-certificate-detail-brand-card-entry
    type: update
    status: archived
related_requirements:
  - REQ-0115-media-multi-variant-images
related_bugs:
  - BUG-0134-miniapp-certificate-detail-display-url
  - BUG-0137-miniapp-lightweight-image-variant-consumption
parent_requirement: REQ-0115-media-multi-variant-images
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md
  - docs/knowledge-base/retrospectives/sprint-024-retrospective.md
cross_cutting_tags: []
readiness: Ready
knowledge_base_gate: N/A
related_changes:
  - update-miniapp-certificate-detail-brand-card-entry
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-24 17:08:44 | lifecycle-stage-migrate | review → archive（/opsx-archive update-miniapp-certificate-detail-brand-card-entry） |
| 2026-08-24 17:08:39 | /opsx-archive | Change `update-miniapp-certificate-detail-brand-card-entry` 已归档，状态同步完成。 |
| 2026-08-24 16:58:31 | /opsx-apply | Change `update-miniapp-certificate-detail-brand-card-entry` 实现完成并进入归档前复核。 |
| 2026-08-24 16:57:52 | /opsx-apply | Change `update-miniapp-certificate-detail-brand-card-entry` 实现推进并完成剩余验收补齐。 |
| 2026-08-24 16:34:40 | /req-opsx | 创建 OpenSpec Change `update-miniapp-certificate-detail-brand-card-entry` 并完成初始追踪登记。 |
| 2026-08-24 16:24:29 | /sprint-propose | 纳入 `sprint-025` 正式范围，并在 Change 创建后完成回填。 |
| 2026-08-24 15:42:48 | lifecycle-stage-migrate | plan → review（/req-review） |
| 2026-08-24 15:42:12 | /req-review | 需求评审通过，状态推进为 `approved`；后续可纳入 Sprint。 |
| 2026-08-24 15:26:47 | /req-complete | 补齐用户故事、业务流程、验收标准和小程序原型上下文；结合小程序媒体四联验收与 sprint-024 媒体 URL 语义复盘，状态推进为 `pending_review`。 |
| 2026-08-24 15:02:14 | /req-generate | 生成 `requirement.md`，需求状态推进为 `draft`。 |
| 2026-08-24 14:58:45 | /capture | 记录小程序证书详情页品牌入口复用 brand-card、补齐 `brand_logo_thumbnail_url`、统一跳转、埋点 `brand_card_click` 与图片轻量化策略的需求。 |

- 2026-08-24 17:08:39 workflow-sync：状态同步为 done（Change archived）
