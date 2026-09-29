---
requirement_id: REQ-0136-signed-cos-direct-media-read
status: in_sprint
priority: P1
created_at: '2026-09-07 22:38:57'
updated_at: '2026-09-09 08:50:35'
lifecycle_stage: review
lifecycle:
  captured: '2026-09-07 22:38:57'
  generated: '2026-09-07 22:51:39'
  completed: '2026-09-07 22:58:21'
  reviewed: '2026-09-08 08:26:26'
  approved: '2026-09-08 08:26:26'
  enriching: '2026-09-07 22:58:21'
iteration: sprint-030
openspec_changes:
- change_id: add-signed-cos-direct-media-read
  type: add
  status: in_progress
related_requirements:
- REQ-0135-authorized-cos-direct-upload
readiness: Partially Ready
knowledge_base_gate: Pass
knowledge_base_refs:
- docs/knowledge-base/best-practices/admin-list-page-consistency.md
- docs/knowledge-base/best-practices/admin-form-page-consistency.md
- docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
- docs/knowledge-base/best-practices/admin-media-upload-chain.md
- docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md
- docs/knowledge-base/retrospectives/sprint-028-retrospective.md
cross_cutting_tags:
- admin-list
- admin-form
- admin-modal
- media-upload
prototype_refs:
- prototype/web/media-states.html
- prototype/web/context.md
decision_status: approved_baseline
review_blockers: []
product_data_collection_observability:
  status: applicable
  affected_layers:
  - web_admin
  - web_catalog
  - wechat_miniapp
  - backend_api
  - request_logs
  - usage_events
  - task_traces
  - task_trace_spans
  - object_storage
  reason: 三端读取与授权、恢复、外部候选解析适用；直接COS传输不伪造后端读取日志，DB不预设结构变更。
  validation: AC-014至AC-016覆盖链路、脱敏、保留周期、旧数据、API/DB/Orval；开发验证已执行，真实设备及生产环境验收待补；详见Change validation。
review_conditions:
- C-001
- C-002
- C-003
- C-004
related_changes:
  - add-signed-cos-direct-media-read
---

# 需求跟踪

Web 与小程序 COS 签名直读及过期恢复。原始记录见 `capture.md`；需求范围、功能要求、批准基线与观测适用性见 `requirement.md`。两条需求分别覆盖上传和读取，可独立验收，不建立总括父需求。

## 变更记录
| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-09-07 22:38:57 | /req-capture | 记录需求并关联 REQ-0135-authorized-cos-direct-upload；未评审、未纳入 Sprint。 |
| 2026-09-07 22:51:39 | /req-generate | 生成 PRD 草稿并置为 draft；阶段划分、撤权窗口及验收参数保留为评审前决策，未纳入 Sprint 或创建 Change。 |
| 2026-09-07 22:58:21 | /req-complete | 补齐故事、流程、17条功能AC、12条横切AC及状态原型；吸收sprint-028四联证据与分层验收经验，未把历史环境门禁当作当前强制阻断；策略尚待评审。 |
| 2026-09-08 08:26:26 | /req-review | 默认approve；采纳D-001至D-006建议作为需求基线，记录C-001至C-004设计/验收条件，plan迁至review，未纳入Sprint。 |

## Readiness Report

文档：requirement、user-stories、business-flow、acceptance、trace齐备；另有capture与交互原型。Readiness为Partially Ready：引用的管理端最佳实践为draft，PNG待导出；需求已approved，D-001至D-006按PRD形成批准基线；review.md条件项约束后续设计与验收，不表示功能已通过。

## Knowledge-base Cross-cutting Report

| 标签 | 文档 | AC条数 |
|---|---|---|
| admin-list | admin-list-page-consistency.md | 4 |
| admin-form | admin-form-page-consistency.md | 2 |
| admin-modal | admin-modal-width-css-cascade.md | 2 |
| media-upload（仅回显回归） | admin-media-upload-chain.md | 2（含上传N/A） |
| 小程序媒体补充 | miniapp-media-four-part-acceptance-practice.md | 2 |

Gate：Pass；上述文件完整路径见knowledge_base_refs。sprint-028复发预防：API字段、对象可读、签名响应和render必须联合验证；静态/DevTools不冒充真机，当前环境证据脚本仅按现行规则手动诊断。无新增follow-up Issue或Change。

## OpenSpec关联

2026-09-08 08:47:12：通过CLI创建 `add-signed-cos-direct-media-read`，关联sprint-030；实施任务及C-001至C-004见Change。

## 本次实施记录

2026-09-09 08:50:35：`/opsx-apply REQ-0136` 已推进13/19项，用户已确认Skeleton；业务页面接入、隔离Compose/MinIO、真实Web过期续播、DevTools相册与事件联调已有开发证据。完整17功能AC及12横切AC的证明边界见[Change验证记录](../../../../openspec/changes/add-signed-cos-direct-media-read/validation.md)。真机、PDF内容渲染及固定COS性能对照未完成，保持in_progress、验收pending与archive_ready=false；不发送完成事件、不归档、不发布。
