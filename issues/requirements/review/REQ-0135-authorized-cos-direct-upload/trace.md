---
requirement_id: REQ-0135-authorized-cos-direct-upload
status: in_sprint
priority: P1
created_at: '2026-09-07 22:38:57'
updated_at: '2026-09-08 09:21:59'
lifecycle_stage: review
lifecycle:
  captured: '2026-09-07 22:38:57'
  generated: '2026-09-07 22:48:13'
  completed: '2026-09-07 22:56:16'
  reviewed: '2026-09-07 22:59:24'
  approved: '2026-09-07 22:59:24'
iteration: sprint-029
openspec_changes:
- change_id: add-authorized-cos-direct-upload
  type: add
  status: in_progress
related_requirements:
- REQ-0136-signed-cos-direct-media-read
readiness: Partially Ready
knowledge_base_gate: Pass
knowledge_base_refs:
- docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
- docs/knowledge-base/best-practices/admin-media-upload-chain.md
- docs/knowledge-base/retrospectives/sprint-028-retrospective.md
cross_cutting_tags:
- admin-modal
- media-upload
product_data_collection_observability:
  status: applicable
  affected_layers:
  - web_admin
  - backend_api
  - request_logs
  - usage_events
  - task_traces
  - task_trace_spans
  - object_storage
  reason: 授权、确认、派生、绑定和清理为跨系统多阶段任务；店主端及小程序仅回归展示，不新增上传封装。
  validation: 验收计划 AC-016～018；当前仅完成需求文档检查，运行时验证待实施。
related_changes:
  - add-authorized-cos-direct-upload
---

# 需求跟踪

后端授权的 COS 媒体直传与上传确认。范围、证据与观测适用性见 `capture.md`。两条需求分别覆盖上传和读取，可独立验收，不建立总括父需求。

## 变更记录
| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-09-07 22:38:57 | /req-capture | 记录需求并关联 REQ-0136-signed-cos-direct-media-read；未评审、未纳入 Sprint。 |
| 2026-09-07 22:48:13 | /req-generate | 生成PRD草稿，明确视频与图片两阶段、确认与权限边界；图片选型等待评审前确定。 |
| 2026-09-07 22:56:16 | /req-complete | 补齐故事、流程、验收及交互原型；转化6条横切AC；继承sprint-028媒体四联证据与环境边界；状态待评审，未批准。 |
| 2026-09-07 22:59:24 | /req-review | 条件通过，批准需求范围；技术选型及参数依review.md在对应阶段实现前关闭；未执行功能验收。 |
| 2026-09-08 08:33:01 | /req-opsx | 关联add-authorized-cos-direct-upload；两阶段完整范围，设计条件保留为实现门禁。 |
| 2026-09-08 08:41:47 | /opsx-apply | 完成契约核查1/22，C-001～003未关闭，Change保持in_progress；未修改业务代码。 |
| 2026-09-08 09:21:59 | /opsx-apply | 浏览器验证、设计门禁及持久会话完成，累计5/22；54项本地和10项隔离MySQL测试通过，业务直传入口未接入。 |

## 交付与评审状态

Readiness 为 Partially Ready：知识库引用为 draft，原型 PNG 待导出及视觉确认。功能验收尚未执行。产品与技术决策以 requirement.md 第8节为唯一清单，按 review.md 条件通过项在对应阶段实现前关闭；未选定付费图片处理服务。后续 Change design 必须引用 knowledge_base_refs，并落实 UI Contract、Skeleton、1440px/computed style 及关键交互视觉验收。
