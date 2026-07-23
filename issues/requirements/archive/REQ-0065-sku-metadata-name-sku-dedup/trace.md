---
requirement_id: REQ-0065-sku-metadata-name-sku-dedup
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-21 16:30:18
updated_at: 2026-07-22 10:13:00
lifecycle:
  captured: 2026-07-21 16:30:18
  generated: 2026-07-21 17:47:43
  completed: 2026-07-21 17:50:00
  reviewed: 2026-07-21 17:57:47
  approved: 2026-07-21 17:57:47
iteration: sprint-010
openspec_changes:
  - change_id: refine-sku-metadata-name-code-display
    type: update
    status: archived
related_requirements:
  - REQ-0006-tile-sku-management
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/retrospectives/sprint-009-retrospective.md
cross_cutting_tags:
  - admin-list
  - admin-modal
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0065-sku-metadata-name-sku-dedup
requirement_name: sku-metadata-name-sku-dedup
requirement_type: SKU 主数据 / 字段模型优化
priority: P1
status: done
lifecycle_stage: review
owner: product
source: 用户输入
target_clients:
  web_admin: 可能涉及
  web_catalog: 可能涉及
  wechat_miniapp: 可能涉及
parent_requirement: REQ-0006-tile-sku-management
related_requirements:
  - REQ-0006-tile-sku-management
related_changes:
  - refine-sku-metadata-name-code-display
lifecycle:
  captured: 2026-07-21 16:30:18
  generated: 2026-07-21 17:47:43
  completed: 2026-07-21 17:50:00
  reviewed: 2026-07-21 17:57:47
  approved: 2026-07-21 17:57:47
iteration: sprint-010
openspec_changes:
  - change_id: refine-sku-metadata-name-code-display
    type: update
    status: archived
readiness: Ready
readiness_notes: 五件套已补齐；命中 admin-list、admin-modal 横切标签，acceptance.md 已写入 AC-XCUT；prototype/web 提供 HTML 与 context，PNG Golden Reference 可后续按需导出。
scope:
  backend_api: 可能涉及；若移除或重命名字段，必须同步 OpenAPI、Orval、docs 和接口测试。
  database: 可能涉及；若字段删除、重命名或迁移，必须同步 SQLite/MySQL schema、迁移脚本、数据库文档和测试。
  web_admin: 可能涉及；SKU 管理表单、列表、筛选和详情展示需要统一字段。
  web_storefront: 可能涉及；商品卡片、详情、搜索结果和分享标题需确认字段来源。
  wechat_miniapp: 可能涉及；SKU 详情页、列表卡片、搜索和分享需要统一展示标识。
  object_storage: 默认不涉及。
expected_openspec_change: refine-sku-metadata-name-code-display
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/retrospectives/sprint-009-retrospective.md
cross_cutting_tags:
  - admin-list
  - admin-modal
knowledge_base_gate: Pass
prototype:
  status: available
  paths:
    - prototype/web/sku-metadata-name-sku-dedup.html
    - prototype/web/sku-metadata-name-sku-dedup-context.md
  png: optional
```

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 将写入 acceptance 的 AC 条数 |
|---|---|---:|
| admin-list | docs/knowledge-base/best-practices/admin-list-page-consistency.md | 4 |
| admin-modal | docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md | 4 |
| retrospective | docs/knowledge-base/retrospectives/sprint-009-retrospective.md | 0 |

Sprint 009 复盘提示管理端横切 AC 应继续复用，避免列表、弹窗、media-upload 类回归在后续迭代重复发生；本 REQ 不涉及 media-upload，未写入上传横切 AC。

## Readiness Report

| 项 | 结论 |
|---|---|
| Readiness | Ready |
| Knowledge-base gate | Pass |
| Cross-cutting tags | admin-list, admin-modal |
| Requirement | 已生成 |
| User stories | 已生成 |
| Business flow | 已生成 |
| Acceptance | 已生成，含 AC-XCUT-001 ~ AC-XCUT-008 |
| Prototype strategy | HTML + context available；PNG optional |

## 分类分析

| 输入 | 类型倾向 | 归类理由 | 拆分 |
|---|---|---|---|
| 瓷砖 SKU 元数据中“瓷砖名称”和“瓷砖 SKU”只保留一个 | REQ | 属于 SKU 主数据字段模型与展示策略优化，未提供既有验收偏差或故障证据 | 不拆分；同一字段去重闭环 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 09:59:34 | lifecycle-stage-migrate | review → archive（/opsx-archive refine-sku-metadata-name-code-display） |
| 2026-07-22 09:59:16 | /opsx-archive | Change `refine-sku-metadata-name-code-display` 已归档，状态同步完成。 |
| 2026-07-22 09:31:24 | /opsx-apply | Change `refine-sku-metadata-name-code-display` apply 完成，待 archive。 |
| 2026-07-21 18:20:23 | /sprint-propose | 纳入 sprint-010，关联 OpenSpec Change `refine-sku-metadata-name-code-display` |
| 2026-07-21 18:14:27 | /req-opsx | 创建 OpenSpec Change `refine-sku-metadata-name-code-display`，状态 proposed |
| 2026-07-21 17:58:22 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-21 17:57:47 | /req-review --approve | 评审通过；状态更新为 approved；准备由 plan 迁入 review 阶段 |
| 2026-07-21 17:50:00 | /req-complete | 补齐 user-stories、business-flow、acceptance、prototype/web；写入 admin-list/admin-modal 横切 AC；状态更新为 pending_review |
| 2026-07-21 17:47:43 | /req-generate | 生成 requirement.md；明确 SKU 编码为系统自动生成的唯一识别字段，商品名称为用户填写与展示字段 |
| 2026-07-21 16:30:18 | /capture | 记录 SKU 元数据名称与 SKU 字段去重需求 |

- 2026-07-22 09:59:15 workflow-sync：状态同步为 done（Change archived）
