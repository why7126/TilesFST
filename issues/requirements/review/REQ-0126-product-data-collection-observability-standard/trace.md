---
requirement_id: REQ-0126-product-data-collection-observability-standard
status: in_sprint
lifecycle_stage: review
priority: P1
created_at: 2026-08-26 09:56:28
updated_at: 2026-08-26 19:39:49
lifecycle:
  captured: 2026-08-26 09:56:28
  generated: 2026-08-26 10:02:25
  completed: 2026-08-26 10:20:20
  reviewed: 2026-08-26 10:27:00
  approved: 2026-08-26 10:27:00
iteration: sprint-026
openspec_changes:
  - change_id: add-product-data-collection-observability-standard
    type: add
    status: applied
related_requirements:
  - REQ-0124-log-audit-behavior-trace-model
related_changes:
  - add-product-data-collection-observability-standard
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0126-product-data-collection-observability-standard
requirement_name: product-data-collection-observability-standard
requirement_type: 治理规范 / 数据采集 / 链路观测
priority: P1
status: in_sprint
owner: product
source: 用户反馈
target_clients:
  web_admin: 本规范覆盖
  web_catalog: 本规范覆盖
  wechat_miniapp: 本规范覆盖
  app: 本规范覆盖
  backend_api: 本规范覆盖
related_requirements:
  - REQ-0124-log-audit-behavior-trace-model
lifecycle:
  captured: 2026-08-26 09:56:28
  generated: 2026-08-26 10:02:25
  completed: 2026-08-26 10:20:20
  reviewed: 2026-08-26 10:27:00
  approved: 2026-08-26 10:27:00
iteration: sprint-026
openspec_changes:
  - change_id: add-product-data-collection-observability-standard
    type: add
    status: applied
readiness: Ready
readiness_notes: 五件套已补齐；本 REQ 为治理规范类，不新增具体 UI 页面，Knowledge-base UI 横切 gate 为 N/A。
cross_cutting_tags:
  - product-data
  - usage-events
  - request-logs
  - task-trace
  - observability
  - governance
knowledge_base_refs:
  - docs/standards/task-trace-coverage.md
  - docs/standards/api-governance.md
  - docs/knowledge-base/retrospectives/sprint-022-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-023-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-025-retrospective.md
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
expected_openspec_change: add-product-data-collection-observability-standard
related_changes:
  - add-product-data-collection-observability-standard
```

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 将写入 acceptance 的 AC 条数 | 结论 |
|---|---|---:|---|
| 无匹配 UI 标签 | - | 0 | 本 REQ 为通用治理规范，不新增具体管理端列表页、表单页、弹窗或上传 UI；knowledge-base gate 为 N/A。 |

## 复盘参考摘要

- `sprint-022` 复盘指出 RUM / 日志类观测页需要在 PRD 阶段明确主列表、样本页、敏感字段和分页方式；本 REQ 将该经验上升为跨产品采集规范的验收口径。
- `sprint-023` 复盘指出性能观测能力需要同时覆盖 API、Orval、筛选区、列表字段和失败态；本 REQ 将 API / Orval / 测试同步作为规范要求。
- `sprint-025` 复盘指出治理脚本、AI usage 和复杂链路证据需要事实源分层；本 REQ 将明细数据、聚合数据、保留周期和证据消费分层纳入规范。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-26 19:39:49 | /opsx-modify | Change `add-product-data-collection-observability-standard` 验收返修已同步，待复验或 archive。 |
| 2026-08-26 11:01:35 | /opsx-apply | Change `add-product-data-collection-observability-standard` apply 完成，待 archive。 |
| 2026-08-26 11:01:03 | `/opsx-apply` | 落地通用规范文档、docs 索引、Task Trace/API 治理交叉引用和轻量校验；本 Change 不直接修改 API、DB、Web、小程序或 App 代码 |
| 2026-08-26 10:48:56 | `/req-opsx` | 创建 OpenSpec Change `add-product-data-collection-observability-standard`，状态 proposed，等待 `/opsx-apply REQ-0126-product-data-collection-observability-standard` |
| 2026-08-26 10:33:29 | `/sprint-propose` | 纳入 sprint-026 正式范围，状态更新为 in_sprint，下一步创建 OpenSpec Change |
| 2026-08-26 10:27:36 | lifecycle-stage-migrate | plan → review（/req-review） |
| 2026-08-26 10:27:00 | `/req-review` | 需求评审通过，状态更新为 approved，准备迁移到 review 阶段并纳入 Sprint |
| 2026-08-26 10:20:20 | `/req-complete` | 补齐用户故事、业务流程、验收标准和 trace 扩展；本 REQ 为治理规范类，Knowledge-base UI 横切 gate 为 N/A |
| 2026-08-26 10:02:25 | `/req-generate` | 根据 capture 生成通用产品数据采集与链路观测规范 PRD，状态更新为 draft |
| 2026-08-26 09:56:28 | `/req-capture` | 记录“建立通用产品数据采集与链路观测规范”需求，确认 Task Trace 分级覆盖和默认日志保留周期 |
