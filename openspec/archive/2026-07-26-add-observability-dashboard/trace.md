---
change_id: add-observability-dashboard
source_requirement: REQ-0076-observability-dashboard
status: applying
type: add
created_at: 2026-07-26 13:35:51
updated_at: 2026-07-26 16:56:31
owner: product
sprint: sprint-012
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: true
capabilities:
  new: []
  modified:
    - product-usage-logging
strategy: tailwind-ds
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags:
  - admin-list
prototype_refs:
  - issues/requirements/archive/REQ-0076-observability-dashboard/prototype/web/observability-dashboard.html
  - issues/requirements/archive/REQ-0076-observability-dashboard/prototype/web/observability-dashboard-context.md
png_checklist:
  required: false
  status: pending_export
  note: REQ prototype context marks PNG Golden Reference as later export; implementation MUST use HTML/context first.
---

# Change Trace

## 来源

| 类型 | 路径 |
|---|---|
| requirement | `issues/requirements/archive/REQ-0076-observability-dashboard/requirement.md` |
| user-stories | `issues/requirements/archive/REQ-0076-observability-dashboard/user-stories.md` |
| business-flow | `issues/requirements/archive/REQ-0076-observability-dashboard/business-flow.md` |
| acceptance | `issues/requirements/archive/REQ-0076-observability-dashboard/acceptance.md` |
| review | `issues/requirements/archive/REQ-0076-observability-dashboard/review.md` |
| prototype | `issues/requirements/archive/REQ-0076-observability-dashboard/prototype/web/observability-dashboard.html` |

## Readiness Report

| 项 | 结论 |
|---|---|
| REQ status | approved |
| Readiness | Ready |
| Knowledge-base gate | Pass |
| Cross-cutting tags | admin-list |
| Change type | add |
| UI strategy | tailwind-ds |

## Impact

```yaml
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: true
capabilities:
  new: []
  modified:
    - product-usage-logging
```

## Conflict Report

| 检查项 | 结论 |
|---|---|
| HTML vs context | 一致，均要求“日志审计 + 链路观测”仪表、筛选、排行、追踪 ID 和明细下钻。 |
| prototype vs acceptance | 一致，acceptance 的 AC-001 ~ AC-030 均可映射到原型结构或实现约束。 |
| acceptance vs existing spec | 无冲突，是 `product-usage-logging` 的增量扩展。 |
| UI strategy | 采用 `tailwind-ds`，不做 CSS Port；HTML 作为结构参考。 |

## Workflow

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-26 16:56:31 | /opsx-archive add-observability-dashboard | 归档前一致性修正：delta spec 移除已撤回的管理端链路观测仪表页面 Requirement，仅保留后端聚合 API 与契约同步；5.4 页面截图 smoke 因页面模块移除标记为不适用。 |
| 2026-07-26 16:46:18 | 用户要求删除日志审计页链路观测模块 | 已从 `/admin/logs` 前端移除链路观测面板、样式、额外接口请求和对应测试；后端聚合 API 与 Orval 类型暂保留。 |
| 2026-07-26 16:00:30 | /opsx-apply add-observability-dashboard | 实现后端观测聚合 API、管理端日志页观测面板、Orval 类型、文档和测试；浏览器截图 smoke 因 Playwright 浏览器二进制缺失且系统 Chrome 在 sandbox 内启动受限，保留 5.4 未完成。 |
| 2026-07-26 15:33:09 | /sprint-propose sprint-012 | 按用户要求从 sprint-011 改纳入 sprint-012；后续 /opsx-apply 前需通过 Workflow Sync sprint scope dry-run。 |
| 2026-07-26 13:55:43 | /sprint-propose sprint-011 | 纳入 sprint-011 正式范围；后续 /opsx-apply 前需通过 Workflow Sync sprint scope dry-run。 |
| 2026-07-26 13:35:51 | /req-opsx REQ-0076 | 创建 OpenSpec Change `add-observability-dashboard`，生成 proposal、design、delta spec、tasks 与 trace。 |

## Implementation Notes

| 项 | 结论 |
|---|---|
| 接口形态 | 新增 `GET /api/v1/admin/logs/observability`，避免扩大日志列表分页响应，也便于观测面板独立刷新与失败降级。 |
| 查询口径 | 复用日志列表筛选字段，新增 `request_id` 精确定位；`path_or_request_id` 继续支持 path、request_id、client_request_id、task_trace_id 模糊匹配。 |
| 指标口径 | 慢请求阈值 1000ms，慢任务阈值 1000ms；默认时间范围由管理端 `/admin/logs` 保持最近 1 天。 |
| 数据访问 | 聚合在 `LogRepository` 通过 SQL 统计完成，未在过滤前加载全量日志到内存；Task Trace 聚合直接读取 `task_traces` 与 `task_trace_spans`。 |
| UI 策略 | 曾在 `/admin/logs` 增加链路观测面板；2026-07-26 按用户要求已移除页面模块，当前仅保留日志列表、筛选、详情抽屉和 Task Trace 时间线。 |
| 数据库 | 不新增业务表、字段或索引；补强 SQLite 旧表初始化时 schema index 与后续迁移的兼容顺序。 |
| Orval | 已运行 `scripts/generate-openapi-client.sh`，生成 `getLogObservabilityApiV1AdminLogsObservabilityGet` 及相关类型。 |

## Verification

| 命令 | 结果 |
|---|---|
| `uv run pytest src/backend/tests/test_product_usage_logging.py -q` | 17 passed，47 warnings |
| `pnpm --dir src/web exec vitest run src/pages/admin/LogAuditPage.test.tsx` | 16 passed |
| `pnpm --dir src/web build` | passed；保留既有 Tailwind at-rule 与 chunk-size warning |
| `openspec validate add-observability-dashboard --strict` | passed |
| `pnpm --dir src/web exec vitest run src/pages/admin/LogAuditPage.test.tsx` | 删除页面模块后 15 passed |
| `pnpm --dir src/web build` | 删除页面模块后 passed；保留既有 Tailwind at-rule 与 chunk-size warning |

## Known Limitations

| 项 | 说明 |
|---|---|
| 1440 / mobile screenshot smoke | 未完成。Playwright 包可用但浏览器二进制缺失；系统 Chrome 在当前 sandbox 内 headless 启动失败，脱离 sandbox 的普通 Node 又无法解析 REPL 内置 Playwright。 |
| Docker Compose smoke | 本次仅涉及后端 API、Web 页面与文档，未启动完整 Docker Compose。 |
| 前端观测入口 | 已按用户要求从日志审计页移除；`GET /api/v1/admin/logs/observability` 后端接口仍存在，当前没有管理端页面入口消费。 |
