---
requirement_id: REQ-0023-api-docs-swagger-detail-link
status: draft
lifecycle_stage: plan
priority: P1
created_at: 2026-07-01 09:09:32
updated_at: 2026-07-01 09:28:16
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0023-api-docs-swagger-detail-link
requirement_name: api-docs-swagger-detail-link
requirement_type: 管理端 / 接口文档页
priority: P1
status: draft
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
related_requirements:
  - REQ-0022-admin-api-docs-menu
related_changes: []
lifecycle:
  captured: 2026-07-01 09:09:32
  generated: 2026-07-01 09:26:32
  completed: null
  reviewed: null
  approved: null
iteration: null
openspec_changes: []
readiness: Not Ready
readiness_notes: 已生成 requirement.md；待 req-complete 补齐 user-stories、business-flow、acceptance、trace，并在 OpenSpec design 阶段验证 Swagger operationId 深链格式。
documents:
  - capture.md
  - requirement.md
expected_openspec_change: add-api-docs-swagger-detail-link
```

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-07-01 09:26:32 | `/req-generate` | 生成 requirement.md；明确 Swagger operationId 深链、新窗口打开、非 OpenAPI 路由禁用态与鉴权上下文保留策略；status → draft |
| 2026-07-01 09:09:32 | `/capture` | 记录接口文档列表行级“查看”按钮并跳转 Swagger UI 详情能力 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
