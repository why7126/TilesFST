---
requirement_id: REQ-0107-real-user-page-load-rum
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-08-10 22:26:02
updated_at: 2026-08-11 23:14:18
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0107-real-user-page-load-rum
requirement_name: real-user-page-load-rum
requirement_type: 性能监控 / 真实用户体验观测
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 待确认
  web_catalog: 待确认
  wechat_miniapp: 本期
related_requirements:
  - REQ-0072-client-request-identity-standard
  - REQ-0076-observability-dashboard
related_changes: []
lifecycle:
  captured: 2026-08-10 22:26:02
  generated: 2026-08-10 22:36:20
  completed: 2026-08-10 22:56:55
  reviewed: 2026-08-10 23:04:22
  approved: 2026-08-10 23:04:22
iteration: sprint-022
openspec_changes:
  - change_id: add-real-user-page-load-rum
    type: add
    status: archived
readiness: Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance、trace 与 prototype/web 策略；本需求不命中 admin-list/admin-form/admin-modal/media-upload 横切标签，knowledge-base gate 为 N/A。
cross_cutting_tags:
  - rum
  - performance
  - telemetry
  - miniapp
  - web
knowledge_base_refs: []
retrospective_refs:
  - docs/knowledge-base/retrospectives/sprint-021-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-020-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-019-retrospective.md
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - prototype/web/context.md
  - prototype/web/performance-rum-dashboard.html
  - review.md
expected_openspec_change: add-real-user-page-load-rum
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-11 23:14:14 | lifecycle-stage-migrate | review → archive（/opsx-archive add-real-user-page-load-rum） |
| 2026-08-11 23:14:05 | /opsx-archive | Change `add-real-user-page-load-rum` 已归档，状态同步完成。 |
| 2026-08-11 08:47:38 | /opsx-modify | Change `add-real-user-page-load-rum` 验收返修已同步，后续已归档。 |
| 2026-08-10 23:50:10 | /opsx-apply | Change `add-real-user-page-load-rum` apply 完成，后续已归档。 |
| 2026-08-10 23:18:00 | `/req-opsx REQ-0107` | 创建 OpenSpec Change `add-real-user-page-load-rum`，后续已归档。 |
| 2026-08-10 23:07:12 | `/sprint-propose sprint-022 --req REQ-0107` | 纳入 sprint-022 正式范围。 |
| 2026-08-10 23:04:59 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-08-10 23:04:22 | `/req-review --approve` | 需求评审通过，状态更新为 approved，准备迁移至 review 阶段 |
| 2026-08-10 22:56:55 | `/req-complete` | 补齐用户故事、业务流程、验收清单和 prototype 策略；读取知识库索引与近期复盘，确认无横切 AC 标签，状态更新为 pending_review |
| 2026-08-10 22:36:20 | `/req-generate` | 生成真实用户加载耗时监控 PRD，状态更新为 draft |
| 2026-08-10 22:26:02 | `/req-capture` | 记录微信小程序和 Web 页面真实用户加载耗时监控需求，方案倾向为轻量自建 RUM |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-08-11 23:14:05 workflow-sync：状态同步为 done（Change archived）
