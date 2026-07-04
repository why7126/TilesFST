---
requirement_id: REQ-0022-admin-api-docs-menu
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-06-30 21:57:46
updated_at: 2026-07-04 08:16:02
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-form-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-003-retrospective.md
cross_cutting_tags:
  - admin-list
  - admin-form
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0022-admin-api-docs-menu
requirement_name: admin-api-docs-menu
requirement_type: 管理端 / 接口文档
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
related_requirements:
  - REQ-0017-system-settings
related_changes:
  - add-admin-api-docs-menu
lifecycle:
  captured: 2026-06-30 21:57:46
  generated: 2026-06-30 22:10:51
  completed: 2026-07-01 00:16:00
  reviewed: 2026-07-01 00:23:13
  approved: 2026-07-01 00:23:13
iteration: sprint-004
openspec_changes:
  - change_id: add-admin-api-docs-menu
    type: add
    status: archived
readiness: Ready
readiness_notes: 五件套齐全，UI 原型 HTML/context 已提供，PNG Golden 待导出但不阻塞 req-review；横切 AC 已写入 acceptance.md。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - trace.md
  - review.md
  - prototype/web/api-docs.html
  - prototype/web/api-docs-context.md
prototype_png_status: pending_export
expected_openspec_change: add-admin-api-docs-menu
needs_api_change: possible
needs_database_change: false
needs_orval: likely
needs_docker_validation: optional
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-form-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-003-retrospective.md
cross_cutting_tags:
  - admin-list
  - admin-form
cross_cutting_acceptance:
  admin-list: AC-XCUT-001..004
  admin-form: AC-XCUT-005..008
knowledge_base_gate: Pass
```

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 | 说明 |
|---|---|---:|---|
| `admin-list` | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 4 | 接口目录表格、筛选、反馈稳定性；危险操作项标 N/A 并保留 guard |
| `admin-form` | `docs/knowledge-base/best-practices/admin-form-page-consistency.md` | 4 | 接口文档为全页管理端页面；保存/恢复默认项按 N/A 约束后续扩展 |
| retrospective | `docs/knowledge-base/retrospectives/sprint-003-retrospective.md` | 0 | 复发模式：列表 DOM、toast layout shift、原生 confirm、表单页重复 CTA 已转化为 AC-XCUT |

## 原型 trace checklist

| 检查项 | HTML | PNG | Context | 实现 |
|---|---|---|---|---|
| Admin Shell + SYSTEM 接口文档菜单 | ✓ | 待导出 | ✓ | 已实现：`src/web/src/features/admin/data/admin-nav.ts`、`AdminSidebar.tsx` |
| page-hero + 环境策略提示 | ✓ | 待导出 | ✓ | 已实现：`src/web/src/pages/admin/ApiDocsPage.tsx` |
| summary-strip 指标 | ✓ | 待导出 | ✓ | 已实现：`src/web/src/pages/admin/ApiDocsPage.tsx` |
| filter-bar + api-route-table | ✓ | 待导出 | ✓ | 已实现：`ApiDocsPage.tsx`、`api-docs.css` |
| Swagger panel / link | ✓ | 待导出 | ✓ | 已实现：`APP_ENV` 控制 `Try It Out`，生产只读 |
| Orval 方法名状态 | ✓ | 待导出 | ✓ | 已实现：OpenAPI 路由显示 Orval 方法，schema 外路由显示「未生成」 |

## 变更记录

| 2026-07-03 23:55:28 | lifecycle-stage-migrate | review → archive（/opsx-archive add-admin-api-docs-menu） |
| 2026-07-01 00:23:47 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-07-01 08:48:56 | `/opsx-apply add-admin-api-docs-menu` | 实现管理端 `/admin/api-docs`、后端 `/api/v1/admin/api-docs`、Swagger 生产只读策略、OpenAPI/Orval 与测试；API 标准校验剩余失败为既有 tags 历史项 |
| 2026-07-01 00:40:14 | `/req-opsx REQ-0022` | 创建 OpenSpec Change `add-admin-api-docs-menu`；status=proposed |
| 2026-07-01 00:28:26 | `/sprint-propose REQ-0022 纳入 sprint-004` | 需求纳入 sprint-004；OpenSpec Change 待 `/req-opsx REQ-0022` 创建 |
| 2026-07-01 00:23:13 | `/req-review --approve` | 评审通过；status → approved |
| 2026-07-01 00:16:00 | `/req-complete` | 补齐 user-stories、business-flow、acceptance、trace 与 prototype；status → pending_review；knowledge-base gate=Pass |
| 2026-06-30 22:10:51 | `/req-generate` | 生成 requirement.md；status → draft |
| 2026-06-30 21:57:46 | `/capture` | 记录管理端系统设置下方新增接口文档菜单与管理员查看全部接口能力 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0051-api-docs-swagger-ui-link-wrong | high | done | fix-api-docs-swagger-ui-link-wrong | 接口文档页 Swagger UI 入口跳转到 Web 首页 |
| BUG-0052-api-docs-metric-cards-inconsistent | medium | done | fix-api-docs-metric-cards-inconsistent | 接口文档页指标卡样式与瓷砖 SKU 页不一致 |
| BUG-0053-api-docs-list-layout-pagination-inconsistent | medium | done | fix-api-docs-list-layout-pagination-inconsistent | 接口文档列表冗余系统接口信息且分页未与 SKU 页一致 |
