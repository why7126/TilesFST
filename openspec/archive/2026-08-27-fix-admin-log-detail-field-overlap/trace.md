---
change_id: fix-admin-log-detail-field-overlap
source_type: bug
source_id: BUG-0145-admin-log-detail-field-overlap
status: applied
sprint: sprint-026
created_at: 2026-08-27 00:00:00
updated_at: 2026-08-27 00:49:46
---

# 变更追溯

## 来源

| 类型 | 编号 | 说明 |
|---|---|---|
| BUG | BUG-0145-admin-log-detail-field-overlap | 管理端日志详情长字段名和值重叠，影响链路排障字段阅读。 |
| Sprint | sprint-026 | 已纳入正式范围，估算 1 人天。 |

## 状态

```yaml
change_id: fix-admin-log-detail-field-overlap
source_bug: BUG-0145-admin-log-detail-field-overlap
status: applied
sprint: sprint-026
```

## 证据入口

- `issues/bugs/archive/BUG-0145-admin-log-detail-field-overlap/bug.md`
- `issues/bugs/archive/BUG-0145-admin-log-detail-field-overlap/root-cause.md`
- `issues/bugs/archive/BUG-0145-admin-log-detail-field-overlap/acceptance.md`
- `issues/bugs/archive/BUG-0145-admin-log-detail-field-overlap/trace.md`

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-27 00:49:46 | `/opsx-apply` | 修复日志详情长字段名和值重叠；补充前端测试、桌面与窄宽度视觉证据，并回填验收结果。 |
| 2026-08-27 00:00:00 | `/bug-opsx` | 创建 BUG-0145 对应 OpenSpec 修复 Change。 |

## 实现证据

- `src/web/src/pages/admin/LogAuditPage.tsx`：为所有详情字段名统一包裹 `.field-help-text`，保留字段说明 tooltip 的 `aria-label`、hover/focus 行为。
- `src/web/src/features/admin/styles/log-audit.css`：将详情行和 Snapshot 行改为响应式安全列宽，字段名和值均允许在自身列内换行，抽屉主体禁止横向失控溢出。
- `src/web/src/pages/admin/LogAuditPage.test.tsx`：新增长字段名详情断言，覆盖 `parent_behavior_event_id`、`client_request_id`、`behavior_trace_id`、`task_trace_id` 和 tooltip 可访问名称。
- `openspec/archive/2026-08-27-fix-admin-log-detail-field-overlap/implementation/evidence/log-detail-field-overlap-desktop.png`：桌面视口视觉证据。
- `openspec/archive/2026-08-27-fix-admin-log-detail-field-overlap/implementation/evidence/log-detail-field-overlap-narrow.png`：窄宽度视口视觉证据。

## 横切门禁

```yaml
product_data_collection_observability:
  applicability: applicable
  affected_layers:
    - web_admin_log_audit_detail
  api: n/a
  database: n/a
  openapi_orval: n/a
  miniapp: n/a
  object_storage: n/a
  docker_compose: n/a
  validation:
    - python scripts/validate-product-data-observability-gates.py --change fix-admin-log-detail-field-overlap
admin_list_best_practices:
  applicability: applicable
  knowledge_base_refs:
    - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  admin_filter_dropdown: n/a
prototype_ui_gate:
  applicability: n/a
design_system:
  applicability: applicable
  note: 已运行全量校验；当前存在既有 baseline 违规。本次变更聚焦检查未新增裸 Hex。
incident_knowledge_base:
  applicability: n/a
  reason: 单页布局约束缺失，已通过测试和 Change trace 固化，无跨页面复用 incident 价值。
```
