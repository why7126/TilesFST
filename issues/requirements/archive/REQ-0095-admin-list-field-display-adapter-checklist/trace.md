---
requirement_id: REQ-0095-admin-list-field-display-adapter-checklist
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-08-04 08:20:03
updated_at: 2026-08-04 09:29:59
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0095-admin-list-field-display-adapter-checklist
requirement_name: admin-list-field-display-adapter-checklist
requirement_type: 管理端 / 列表展示治理
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
related_requirements: []
related_changes:
  - standardize-admin-list-field-display-adapters
lifecycle:
  captured: 2026-08-04 08:20:03
  generated: 2026-08-04 08:27:12
  completed: 2026-08-04 08:35:48
  reviewed: 2026-08-04 08:41:09
  approved: 2026-08-04 08:41:09
iteration: sprint-019
openspec_changes:
  - change_id: standardize-admin-list-field-display-adapters
    type: update
    status: archived
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-018-retrospective.md
cross_cutting_tags:
  - admin-list
readiness: Ready
readiness_notes: 已补齐 user-stories、business-flow、acceptance、trace 与 Web prototype 策略；admin-list 横切 AC 已写入 acceptance.md。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/web/context.md
  - prototype/web/admin-list-field-adapter-checklist.html
expected_openspec_change: standardize-admin-list-field-display-adapters
```

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 |
|---|---|---:|
| admin-list | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 4 |

## 复盘来源摘要

- `docs/knowledge-base/retrospectives/sprint-018-retrospective.md` 指出管理端和小程序均暴露“字段存在但展示策略不一致”的问题，并建议建立 UI 展示字段映射检查表。
- 同一复盘的可复用抽象中明确提出 `Admin display cell adapters`，建议为管理端列表列渲染建立 image/name/status/fallback 的统一 adapter 或组件约束。

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-08-04 09:29:59 | lifecycle-stage-migrate | review → archive（/opsx-archive standardize-admin-list-field-display-adapters） |
| 2026-08-04 09:29:38 | /opsx-archive | Change `standardize-admin-list-field-display-adapters` 已归档，状态同步完成。 |
| 2026-08-04 08:59:11 | /opsx-apply | Change `standardize-admin-list-field-display-adapters` apply 完成，待 archive。 |
| 2026-08-04 08:41:44 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-08-04 08:20:03 | `/req-capture` | 记录管理端列表字段展示统一 image/name/fallback adapter 检查表需求 |
| 2026-08-04 08:27:12 | `/req-generate` | 生成 requirement.md，状态更新为 draft |
| 2026-08-04 08:35:48 | `/req-complete` | 补齐用户故事、业务流程、验收标准、trace 与 Web prototype 策略；状态更新为 pending_review |
| 2026-08-04 08:41:09 | `/req-review --approve` | 需求评审通过，状态更新为 approved |
| 2026-08-04 08:45:39 | `/req-opsx` | 创建 OpenSpec Change `standardize-admin-list-field-display-adapters` |
| 2026-08-04 08:50:00 | `/sprint-propose` | 纳入 sprint-019 正式范围 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-08-04 09:29:38 workflow-sync：状态同步为 done（Change archived）
