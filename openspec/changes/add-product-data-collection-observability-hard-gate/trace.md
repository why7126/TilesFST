---
change_id: add-product-data-collection-observability-hard-gate
source_requirement: REQ-0127-product-data-collection-observability-hard-gate
source_sprint: sprint-026
status: applied
created_at: 2026-08-26 20:12:00
updated_at: 2026-08-26 21:02:07
---

# Change 追踪

## 来源

| 项 | 值 |
|---|---|
| REQ | `REQ-0127-product-data-collection-observability-hard-gate` |
| Sprint | `sprint-026` |
| 父需求 | `REQ-0126-product-data-collection-observability-standard` |
| Change 类型 | `update` |
| Capability | `product-data-collection-observability-standard` |

## 产品数据采集与链路观测声明

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - api
    - database
    - request_logs
    - usage_events
    - task_trace
    - web_request_wrapper
    - miniapp_request_wrapper
    - app_request_wrapper
    - workflow_governance
  reason: 本 Change 直接建立采集规范硬门禁，覆盖入口路由、规则、技能和实现级校验脚本。
  validation: /opsx-apply 已运行采集规范门禁聚焦校验、OpenSpec strict 校验、语言校验、相关 pytest 和 Sprint scope 校验；Workflow Sync 将回填 linked REQ/Sprint applied 状态。
```

## 影响声明

| 范围 | 影响 |
|---|---|
| API | 不直接修改业务 API；后续 API contract、请求头、错误码、响应字段、请求日志变更受门禁约束。 |
| DB | 不直接修改 SQLite/MySQL schema；后续 `usage_events`、`request_logs`、`task_traces`、`task_trace_spans`、索引、迁移、保留周期变更受门禁约束。 |
| Orval | 本 Change 不需要生成 Orval；后续 API contract 变更必须同步或声明 N/A。 |
| Web / 小程序 / App | 不直接修改端侧代码；后续请求封装、行为埋点、链路 ID 透传和离线重试变更受门禁约束。 |
| 测试 | 实现阶段需要新增或更新治理校验脚本测试。 |

## 验证摘要

| 命令 | 结果 |
|---|---|
| `python scripts/validate-product-data-observability-gates.py --change add-product-data-collection-observability-hard-gate` | pass |
| `python scripts/validate-product-data-observability-gates.py --req REQ-0127-product-data-collection-observability-hard-gate` | pass |
| `python scripts/validate-product-data-observability-gates.py --sprint sprint-026` | pass |
| `python scripts/validate-product-data-observability-standard.py` | pass |
| `python scripts/validate-openspec-language.py` | pass |
| `openspec validate add-product-data-collection-observability-hard-gate --strict` | pass |
| `python -m pytest tests/test_validate_product_data_observability_gates.py tests/test_validate_agent_context_budget.py tests/test_validate_openspec_language.py` | 14 passed |
| `python scripts/validate-sprint-scope.py sprint-026 --item REQ-0127-product-data-collection-observability-hard-gate --item add-product-data-collection-observability-hard-gate` | pass |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-26 21:02:07 | `/opsx-apply` | 完成 AGENTS、rules、req/opsx/sprint 技能、采集规范门禁校验脚本和测试接入，并记录验证摘要。 |
| 2026-08-26 20:12:00 | `/req-opsx` | 创建 OpenSpec Change，并建立 proposal、design、spec delta、tasks、trace、acceptance 与 test-plan。 |
