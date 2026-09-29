---
requirement_id: REQ-0132-workbuddy-custom-connector
status: in_sprint
lifecycle_stage: review
priority: P1
created_at: 2026-09-04 16:43:52
updated_at: 2026-09-06 14:57:59
lifecycle:
  captured: 2026-09-04 16:43:52
  generated: 2026-09-04 16:51:47
  completed: 2026-09-04 16:55:18
  reviewed: 2026-09-04 17:32:29
  approved: 2026-09-04 17:32:29
iteration: sprint-029
openspec_changes:
  - change_id: add-workbuddy-custom-connector
    type: add
    status: in_progress
related_changes:
  - add-workbuddy-custom-connector
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0132-workbuddy-custom-connector
requirement_name: workbuddy-custom-connector
requirement_type: 集成能力 / AI 连接器 / MCP
priority: P1
status: in_sprint
owner: product
source: 用户输入
target_clients:
  web_admin: 本期
  web_catalog: 间接受影响
  wechat_miniapp: 间接受影响
related_requirements: []
related_changes:
  - add-workbuddy-custom-connector
lifecycle:
  captured: 2026-09-04 16:43:52
  generated: 2026-09-04 16:50:11
  completed: 2026-09-04 16:55:18
  reviewed: 2026-09-04 17:32:29
  approved: 2026-09-04 17:32:29
iteration: sprint-029
openspec_changes:
  - change_id: add-workbuddy-custom-connector
    type: add
    status: in_progress
readiness: Partially Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance 与 trace；本 REQ 不新增管理端 UI 页面，prototype 策略为 N/A。命中的 media-upload best-practices 为 draft，因此 readiness 暂为 Partially Ready。
cross_cutting_tags:
  - media-upload
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-028-retrospective.md
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
expected_openspec_change: add-workbuddy-custom-connector
product_data_collection_observability:
  status: applicable
  affected_layers:
    - backend_api
    - request_logs
    - task_traces
    - task_trace_spans
    - admin_web_indirect
    - object_storage_indirect
    - deployment
  reason: 连接器将作为直接 API 调用方访问 ProjectTilesFST，并在第二阶段执行管理端写操作、媒体上传和远程 MCP 服务部署，涉及请求来源识别、工具调用审计、任务链路、错误摘要、环境变量和凭据安全。
  validation: 后续 OpenSpec Change 需覆盖直接 API 调用、鉴权越权、dry-run 不写入、真实写操作审计、上传链路、OpenAPI/Orval、Docker/HTTPS 部署和脱敏日志验证。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-09-05 21:45:05 | /opsx-modify | Change `add-workbuddy-custom-connector` 验收返修已同步，待复验或 archive。 |
| 2026-09-04 18:17:47 | /opsx-apply | Change `add-workbuddy-custom-connector` apply 完成，待 archive。 |
| 2026-09-04 17:58:56 | `/req-opsx` | 创建并关联 OpenSpec Change `add-workbuddy-custom-connector`，已回填 sprint-029 scope |
| 2026-09-04 17:47:01 | `/sprint-propose` | 纳入 sprint-029 正式范围，状态更新为 in_sprint，下一步创建 OpenSpec Change |
| 2026-09-04 17:33:42 | lifecycle-stage-migrate | plan → review（/req-review） |
| 2026-09-04 17:32:29 | `/req-review` | 默认 approve：需求评审通过，状态更新为 approved，准备迁入 review 阶段 |
| 2026-09-04 16:55:18 | `/req-complete` | 补齐用户故事、业务流程、验收标准、media-upload 横切 AC 与产品数据采集/链路观测声明；状态更新为 pending_review |
| 2026-09-04 16:50:11 | `/req-generate` | 生成腾讯 WorkBuddy 自定义连接器支持 PRD，状态更新为 draft |
| 2026-09-04 16:43:52 | `/req-capture` | 记录腾讯 WorkBuddy 自定义连接器分阶段建设需求 |
