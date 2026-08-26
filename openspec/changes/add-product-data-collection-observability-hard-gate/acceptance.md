---
change_id: add-product-data-collection-observability-hard-gate
source_requirement: REQ-0127-product-data-collection-observability-hard-gate
source_sprint: sprint-026
acceptance_status: pending
created_at: 2026-08-26 20:12:00
updated_at: 2026-08-26 21:02:07
---

# 验收

## 产品数据采集与链路观测门禁

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
  reason: 本 Change 实现采集规范硬门禁本身，必须覆盖必读、必声明、必验收和实现级校验。
  validation: 已运行采集规范门禁聚焦校验、OpenSpec strict 校验、语言校验和相关自动化测试；Workflow Sync 待最终 applied 同步。
```

## 验收清单

- [x] `AGENTS.md` 已接入 `docs/standards/product-data-collection-observability.md` 读取路由和完成检查。
- [x] 相关 `rules/` 已声明采集规范触发范围、固定声明字段、N/A 原因和归档验收要求。
- [x] req / opsx / sprint 技能已接入采集规范必读、必声明、必验收检查清单。
- [x] 实现级校验脚本能检查入口、规则、技能和 active Change 声明。
- [x] 校验脚本支持聚焦参数，默认不扫描全部历史 archive。
- [x] 校验脚本失败路径输出缺失文件、缺失字段、触发依据和修复建议。
- [x] 校验脚本不读取或输出真实客户数据、密钥、`.env`、Authorization header、Cookie、本机绝对路径或完整工具输出正文。
- [x] 本 Change 不直接修改业务 API、DB、Web、小程序或 App 代码；如实现阶段发现必须修改业务代码，必须先回到 Change 设计说明并保持 Sprint scope 一致。

## 验证摘要

| 命令 | 结果 |
|---|---|
| `python scripts/validate-product-data-observability-gates.py --change add-product-data-collection-observability-hard-gate` | pass；entry_files=7，skill_files=11，Change 声明存在。 |
| `python scripts/validate-product-data-observability-gates.py --req REQ-0127-product-data-collection-observability-hard-gate` | pass；REQ 文档包声明存在。 |
| `python scripts/validate-product-data-observability-gates.py --sprint sprint-026` | pass；Sprint 聚焦扫描扩展到关联 REQ/BUG/Change，不扫描历史 archive。 |
| `python scripts/validate-product-data-observability-standard.py` | pass。 |
| `python scripts/validate-openspec-language.py` | pass。 |
| `openspec validate add-product-data-collection-observability-hard-gate --strict` | pass。 |
| `python -m pytest tests/test_validate_product_data_observability_gates.py tests/test_validate_agent_context_budget.py tests/test_validate_openspec_language.py` | 14 passed。 |
| `python scripts/validate-sprint-scope.py sprint-026 --item REQ-0127-product-data-collection-observability-hard-gate --item add-product-data-collection-observability-hard-gate` | pass。 |

## 验收结果回填

```yaml
acceptance_status: pending
accepted_at: null
accepted_by: null
evidence:
  - scripts/validate-product-data-observability-gates.py
  - tests/test_validate_product_data_observability_gates.py
  - openspec/changes/add-product-data-collection-observability-hard-gate/tasks.md
failed_items: []
notes: /opsx-apply 已完成实现与聚焦验证，待 /opsx-archive 归档复核。
```
