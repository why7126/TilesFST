---
requirement_id: REQ-0131-media-object-key-business-id-layout
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-08-29 19:15:09
updated_at: 2026-08-29 23:25:21
lifecycle:
  generated: 2026-08-29 19:20:11
  completed: 2026-08-29 19:23:12
  reviewed: 2026-08-29 19:30:52
  approved: 2026-08-29 19:30:52
iteration: sprint-027
openspec_changes:
  - change_id: update-media-object-key-business-id-layout
    type: update
    status: archived
related_changes:
  - update-media-object-key-business-id-layout
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0131-media-object-key-business-id-layout
requirement_name: media-object-key-business-id-layout
requirement_type: 对象存储 / 媒体治理 / 兼容迁移
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 需评估
  wechat_miniapp: 需评估
related_requirements:
  - REQ-0012-object-storage-key-layout
  - REQ-0115-media-multi-variant-images
  - REQ-0122-batch-image-processing-runbook
related_changes:
  - update-media-object-key-business-id-layout
lifecycle:
  captured: 2026-08-29 19:15:09
  generated: 2026-08-29 19:18:29
  completed: 2026-08-29 19:23:12
  reviewed: 2026-08-29 19:30:52
  approved: 2026-08-29 19:30:52
iteration: sprint-027
openspec_changes:
  - change_id: update-media-object-key-business-id-layout
    type: update
    status: archived
readiness: Partially Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance、trace 和 prototype 策略；命中的 media-upload best-practice 为 draft，且本需求默认不新增 UI 原型 PNG，故 readiness 暂为 Partially Ready。
cross_cutting_tags:
  - object-storage
  - media-upload
  - media-maintenance
  - compatibility
  - product-data-collection-observability
knowledge_base_refs:
  - docs/knowledge-base/README.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-026-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-025-retrospective.md
product_data_collection_observability:
  status: applicable
  affected_layers:
    - request_logs
    - task_traces
    - task_trace_spans
    - backend_api
    - web_admin_request_flow
    - wechat_miniapp_request_flow
    - maintenance_jobs
  reason: 本需求涉及媒体上传、业务对象保存后 formalize、存量对象迁移、维护任务审计、受控媒体 URL 和数据库媒体引用一致性，需要记录请求日志、任务链路、流程节点和脱敏维护摘要。
  validation: 已在 requirement.md 与 acceptance.md 声明适用层级；后续 OpenSpec Change 必须补齐具体字段、脱敏规则、测试和验收证据。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - prototype/web/context.md
  - review.md
expected_openspec_change: update-media-object-key-business-id-layout
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-29 23:24:36 | lifecycle-stage-migrate | review → archive（/opsx-archive update-media-object-key-business-id-layout） |
| 2026-08-29 23:24:26 | /opsx-archive | Change `update-media-object-key-business-id-layout` 已归档，状态同步完成。 |
| 2026-08-29 21:15:09 | /opsx-modify | Change `update-media-object-key-business-id-layout` 验收返修已同步，待复验或 archive。 |
| 2026-08-29 20:09:36 | /opsx-apply | Change `update-media-object-key-business-id-layout` apply 进行中，待补齐剩余验收。 |
| 2026-08-29 19:31:39 | lifecycle-stage-migrate | plan → review（/req-review） |
| 2026-08-29 19:30:52 | `/req-review` | 评审通过；确认可进入 Sprint 规划，约束后续 Change 必须保留旧媒体兼容、迁移 dry-run/apply/audit/rollback、对象存储与媒体规范同步 |
| 2026-08-29 19:23:12 | `/req-complete` | 补齐用户故事、业务流程、验收标准与原型策略；写入 media-upload 横切 AC、产品数据采集与链路观测门禁、sprint-025/026 媒体复盘引用 |
| 2026-08-29 19:18:29 | `/req-generate` | 生成统一媒体对象 Key 按业务对象 id 分目录 PRD，状态更新为 draft |
| 2026-08-29 19:15:09 | `/req-capture` | 记录统一媒体对象 Key 按业务对象 id 分目录，并补齐旧媒体兼容、迁移与文档规范的需求 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-08-29 23:24:26 workflow-sync：状态同步为 done（Change archived）
