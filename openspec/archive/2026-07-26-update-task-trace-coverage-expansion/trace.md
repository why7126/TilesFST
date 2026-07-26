---
change_id: update-task-trace-coverage-expansion
type: update
status: implemented
created_at: 2026-07-26 13:34:21
updated_at: 2026-07-26 15:57:22
source_requirement: REQ-0074-task-trace-coverage-expansion
related_requirements:
  - REQ-0069-upload-observability-trace-logs
iteration: sprint-012
---

# Trace

```yaml
change_id: update-task-trace-coverage-expansion
type: update
status: implemented
created_at: 2026-07-26 13:34:21
updated_at: 2026-07-26 15:57:22
source_requirement: REQ-0074-task-trace-coverage-expansion
related_requirements:
  - REQ-0069-upload-observability-trace-logs
iteration: sprint-012
```

## 来源

| 类型 | 路径 | 说明 |
|---|---|---|
| requirement | `issues/requirements/archive/REQ-0074-task-trace-coverage-expansion/requirement.md` | PRD |
| acceptance | `issues/requirements/archive/REQ-0074-task-trace-coverage-expansion/acceptance.md` | 验收标准 |
| business-flow | `issues/requirements/archive/REQ-0074-task-trace-coverage-expansion/business-flow.md` | 业务流程 |
| prototype | `issues/requirements/archive/REQ-0074-task-trace-coverage-expansion/prototype/web/task-trace-feedback.html` | 管理端复杂任务反馈原型 |

## Requirement Readiness Report

| 项 | 状态 | 说明 |
|---|---|---|
| review gate | pass | REQ-0074 status = in_sprint |
| readiness | Ready | 五件套齐全，含 HTML/context 原型策略 |
| knowledge-base gate | N/A | 未命中固定 UI 横切标签；已引用 Sprint 010 复盘 |
| change type | update | 扩展既有 `product-usage-logging` Task Trace 能力 |

## Impact

```yaml
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: true
  storage: true
  api: true
capabilities:
  new: []
  modified:
    - product-usage-logging
```

## Conflict Report

| 来源 | 结论 |
|---|---|
| HTML prototype | 确认复杂任务反馈的信息层级和复制入口 |
| prototype context | 确认 processing / success / failed / partial_success / no_trace 状态 |
| acceptance.md | 与原型一致，要求无 trace 时保持旧交互 |
| ui-design.md | 实现必须使用 semantic token，HTML 裸色值不可 CSS Port |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-26 15:57:22 | /opsx-apply | 接入 SKU 创建、更新、上架、下架 Task Trace；响应返回 `task_trace_id/task_type`；Web SKU 弹窗展示并可复制追踪 ID；OpenAPI/Orval 与 API/DB 文档已同步。 |
| 2026-07-26 15:34:18 | /sprint-propose | 按用户要求从 `sprint-011` 改纳入 `sprint-012`。 |
| 2026-07-26 15:17:02 | /sprint-propose | 纳入 `sprint-011`，满足来源于 REQ 的 Change 在 `/opsx-apply` 前必须入 Sprint 的门禁。 |
| 2026-07-26 13:34:21 | /req-opsx | 基于 REQ-0074 创建 OpenSpec Change，状态 proposed。 |

## Apply Verification

| 项 | 结论 |
|---|---|
| Sprint 门禁 | `sync-workflow-status --event opsx.apply --dry-run --sprint auto` 解析为 `sprint-012`，REQ-0074 与 Change 均在 sprint 正式范围内。 |
| 横切最佳实践 | 已补读 `admin-form-page-consistency.md` 与 `admin-modal-width-css-cascade.md`；SKU 弹窗继续使用单一 `sku-modal-card`，不挂载通用 `modal-card`。 |
| API / DB | 不新增任务状态查询接口、不新增错误码、不新增 Task Trace 存储表；复用 `task_traces`、`task_trace_spans`、日志审计 `task_trace_id` 查询能力。 |
| 测试 | `uv run pytest src/backend/tests/test_admin_tile_skus.py src/backend/tests/test_product_usage_logging.py -q` 通过；`pnpm --dir src/web exec vitest run src/features/admin/components/TileSkuFormModal.test.tsx` 通过。 |
| 门禁 | `openspec validate update-task-trace-coverage-expansion --strict` 通过；`python scripts/validate-directory-structure.py` 通过；workflow sync apply 后 dry-run 无 delta。 |
| 生产 DB / 对象存储 / 异步 smoke | N/A。本期不新增 schema 字段、不触发对象存储写入、不新增 worker；仅复用既有上传链路和日志审计。 |
