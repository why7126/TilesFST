---
requirement_id: REQ-0023-api-docs-swagger-detail-link
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-01 09:09:32
updated_at: 2026-07-04 08:16:02
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-003-retrospective.md
cross_cutting_tags:
  - admin-list
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0023-api-docs-swagger-detail-link
requirement_name: api-docs-swagger-detail-link
requirement_type: 管理端 / 接口文档页
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
related_requirements:
  - REQ-0022-admin-api-docs-menu
related_changes:
  - add-api-docs-swagger-detail-link
lifecycle:
  captured: 2026-07-01 09:09:32
  generated: 2026-07-01 09:26:32
  completed: 2026-07-01 13:55:01
  reviewed: 2026-07-01 14:06:40
  approved: 2026-07-01 14:06:40
iteration: sprint-004
openspec_changes:
  - change_id: add-api-docs-swagger-detail-link
    type: add
    status: archived
readiness: Ready
readiness_notes: requirement、user-stories、business-flow、acceptance、trace、prototype/context 已齐；admin-list 横切 AC 已写入 acceptance；已纳入 sprint-004，OpenSpec Change 已完成 apply，待验收与归档。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/web/api-docs-swagger-detail-link.html
  - prototype/web/api-docs-swagger-detail-link-context.md
expected_openspec_change: add-api-docs-swagger-detail-link
prototype_png_status: pending_export
needs_api_change: false
needs_database_change: false
needs_orval: false
needs_docker_validation: false
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-003-retrospective.md
cross_cutting_tags:
  - admin-list
cross_cutting_acceptance:
  admin-list: AC-XCUT-001..004
knowledge_base_gate: Pass
```

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 | 说明 |
|---|---|---:|---|
| `admin-list` | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 4 | 接口目录为管理端表格 + 行内操作；已写入分页 DOM、feedback、confirm N/A、禁止原生弹窗 |
| retrospective | `docs/knowledge-base/retrospectives/sprint-003-retrospective.md` | 0 | Sprint 003 复发模式：分页 DOM 不一致、toast layout shift、原生 confirm；已转为横切 AC |

## 原型 trace checklist

| 检查项 | HTML | PNG | Context | 说明 |
|---|---|---|---|---|
| ACTION 列 | ✓ | 待导出 | ✓ | `api-docs-swagger-detail-link.html` 展示 OpenAPI 与非 OpenAPI 两类行 |
| operationId 深链 | ✓ | 待导出 | ✓ | 示例 `/docs#/admin-api-docs/get_api_docs_api_v1_admin_api_docs_get` |
| 非 OpenAPI 禁用态 | ✓ | 待导出 | ✓ | `/media/{object_key:path}` 显示禁用「查看」 |
| 新窗口与安全属性 | ✓ | 待导出 | ✓ | 可用链接使用 `target="_blank"` + `rel="noreferrer"` |

## 变更记录

| 2026-07-03 13:12:50 | lifecycle-stage-migrate | review → archive（/opsx-archive add-api-docs-swagger-detail-link） |
| 2026-07-01 14:08:07 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-07-02 22:16:42 | 用户反馈修复 | 筛选后左下角 `共 * 个接口` 改为当前筛选结果数量；ApiDocsPage 与管理端相关 Vitest 19 tests、OpenSpec strict、目录结构校验通过 |
| 2026-07-02 22:05:09 | 用户追加 ACTION 固定列 | ACTION 表头与操作单元格固定在表格最右侧；管理端相关 Vitest 19 tests、OpenSpec strict、目录结构校验通过 |
| 2026-07-02 21:54:56 | 用户追加 PATH 列查看入口 | PATH 列在可跳转路由上复用 `/docs#/{tag}/{operationId}` 深链；非 OpenAPI/缺失 operationId 保持普通文本；ApiDocsPage Vitest 通过 |
| 2026-07-02 10:34:20 | `/opsx-apply add-api-docs-swagger-detail-link` | 完成 `/docs#/{tag}/{operationId}` 编码深链、行级 ACTION 列、非 OpenAPI/缺失 operationId 禁用态；Vitest 回归通过；无 API/Orval/数据库/Docker 变更 |
| 2026-07-02 09:26:53 | `/req-opsx REQ-0023` | 创建 `add-api-docs-swagger-detail-link`；status proposed；修改 web-client/testing specs |
| 2026-07-02 09:17:47 | `/sprint-propose REQ-0023 纳入 sprint-004` | 已纳入 sprint-004 正式范围；status → in_sprint；OpenSpec Change 待 `/req-opsx REQ-0023-api-docs-swagger-detail-link` |
| 2026-07-01 14:06:40 | `/req-review --approve` | 评审通过；确认范围、验收、UI 原型策略、BUG-0051 边界与 admin-list 横切 AC；status → approved |
| 2026-07-01 13:55:01 | `/req-complete` | 补齐 user-stories、business-flow、acceptance、prototype/context；写入 admin-list knowledge-base 横切 AC；status → pending_review |
| 2026-07-01 09:26:32 | `/req-generate` | 生成 requirement.md；明确 Swagger operationId 深链、新窗口打开、非 OpenAPI 路由禁用态与鉴权上下文保留策略；status → draft |
| 2026-07-01 09:09:32 | `/capture` | 记录接口文档列表行级“查看”按钮并跳转 Swagger UI 详情能力 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-07-03 13:12:46 workflow-sync：状态同步为 done（Change archived）
