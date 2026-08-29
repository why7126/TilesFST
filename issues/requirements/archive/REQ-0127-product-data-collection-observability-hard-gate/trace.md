---
requirement_id: REQ-0127-product-data-collection-observability-hard-gate
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-08-26 19:48:35
updated_at: 2026-08-28 16:15:59
lifecycle:
  captured: 2026-08-26 19:48:35
  generated: 2026-08-26 19:52:14
  completed: 2026-08-26 19:55:31
  reviewed: 2026-08-26 20:01:37
  approved: 2026-08-26 20:01:37
iteration: sprint-026
openspec_changes:
  - change_id: add-product-data-collection-observability-hard-gate
    type: update
    status: archived
related_requirements:
  - REQ-0126-product-data-collection-observability-standard
related_changes:
  - add-product-data-collection-observability-hard-gate
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0127-product-data-collection-observability-hard-gate
requirement_name: product-data-collection-observability-hard-gate
requirement_type: 治理门禁 / 产品数据采集 / 链路观测
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 门禁覆盖
  web_catalog: 门禁覆盖
  wechat_miniapp: 门禁覆盖
  app: 门禁覆盖
  backend_api: 门禁覆盖
related_requirements:
  - REQ-0126-product-data-collection-observability-standard
lifecycle:
  captured: 2026-08-26 19:48:35
  generated: 2026-08-26 19:52:14
  completed: 2026-08-26 19:55:31
  reviewed: 2026-08-26 20:01:37
  approved: 2026-08-26 20:01:37
iteration: sprint-026
openspec_changes:
  - change_id: add-product-data-collection-observability-hard-gate
    type: update
    status: archived
readiness: Ready
readiness_notes: 五件套已补齐；本 REQ 为治理门禁类，不新增具体 UI 页面，Knowledge-base UI 横切 gate 为 N/A。
cross_cutting_tags:
  - product-data
  - observability
  - request-logs
  - usage-events
  - task-trace
  - governance-gate
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-025-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-023-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-022-retrospective.md
  - docs/standards/product-data-collection-observability.md
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
  reason: 本 REQ 直接要求将产品数据采集与链路观测规范接入流程硬门禁。
  validation: 后续 OpenSpec Change 必须提供门禁校验脚本摘要和 N/A 声明检查结果。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
expected_openspec_change: add-product-data-collection-observability-hard-gate
related_changes:
  - add-product-data-collection-observability-hard-gate
```

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 将写入 acceptance 的 AC 条数 | 结论 |
|---|---|---:|---|
| 无匹配 UI 标签 | - | 0 | 本 REQ 为治理门禁和流程规范，不新增具体管理端列表页、表单页、弹窗或媒体上传 UI；knowledge-base UI gate 为 N/A。 |

## 复盘参考摘要

- `sprint-025` 复盘指出 Workflow Sync、OpenSpec、stale scan、residual gate 与 AI usage fresh gate 需要脚本化闭环；本 REQ 将产品数据采集规范纳入脚本化门禁。
- `sprint-023` 复盘指出观测类页面和治理命令容易遗漏 API、Orval、验收和 Sprint scope；本 REQ 要求相关 Change 在设计与归档前声明采集规范影响。
- `sprint-022` 复盘指出治理 Change 不触碰业务 `src/` 时仍要走 Sprint Inclusion Gate；本 REQ 后续实现同样必须先评审并纳入 Sprint。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-27 23:13:16 | lifecycle-stage-migrate | review → archive（/opsx-archive add-product-data-collection-observability-hard-gate） |
| 2026-08-27 23:13:09 | /opsx-archive | Change `add-product-data-collection-observability-hard-gate` 已归档，状态同步完成。 |
| 2026-08-26 21:03:51 | /opsx-apply | Change `add-product-data-collection-observability-hard-gate` apply 完成，后续已归档。 |
| 2026-08-26 21:03:12 | /opsx-apply | Change `add-product-data-collection-observability-hard-gate` apply 过程记录，后续已补齐验收并归档。 |
| 2026-08-26 20:13:20 | `/req-opsx` | 创建 OpenSpec Change `add-product-data-collection-observability-hard-gate`，后续已回填 sprint-026 scope 并归档。 |
| 2026-08-26 20:07:45 | `/sprint-propose` | 纳入 sprint-026 正式范围，后续已创建并归档 OpenSpec Change。 |
| 2026-08-26 20:02:09 | lifecycle-stage-migrate | plan → review（/req-review） |
| 2026-08-26 20:01:37 | `/req-review` | 需求评审通过，状态更新为 approved，准备迁移到 review 阶段并纳入 Sprint。 |
| 2026-08-26 19:55:31 | `/req-complete` | 补齐用户故事、业务流程、验收标准和 trace 扩展；本 REQ 为治理门禁类，Knowledge-base UI 横切 gate 为 N/A。 |
| 2026-08-26 19:52:14 | `/req-generate` | 根据 capture 生成产品数据采集与链路观测规范硬门禁 PRD，状态更新为 draft。 |
| 2026-08-26 19:48:35 | `/req-capture` | 记录“产品数据采集与链路观测规范硬门禁”需求，作为 REQ-0126 的门禁化 refinement。 |

- 2026-08-27 23:13:09 workflow-sync：状态同步为 done（Change archived）
