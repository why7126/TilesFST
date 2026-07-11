---
requirement_id: REQ-0028-admin-list-page-contract
status: done
priority: P1
created_at: 2026-07-04 15:17:26
updated_at: 2026-07-11 08:52:57
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-04 15:17:26
  generated: 2026-07-05 07:56:30
  completed: 2026-07-05 10:18:38
  reviewed: 2026-07-05 14:36:29
  approved: 2026-07-05 14:36:29
iteration: sprint-005
openspec_changes:
  - change_id: add-admin-list-page-contract
    type: add
    status: archived
related_requirements:
  - REQ-0000-build-design-system
  - REQ-0029-admin-list-foundation-components
related_bugs:
  - BUG-0055-admin-list-layout-unification
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-004-retrospective.md
cross_cutting_tags:
  - admin-list
readiness: Partially Ready
readiness_notes:
  - 五件套已补齐，UI prototype HTML/context 已生成。
  - acceptance.md 已写入 admin-list 横切 AC。
  - PNG Golden Reference 待后续人工或实现阶段导出，因此标记为 Partially Ready。
---

# Trace

## 当前状态

- 状态：done
- 阶段：archive
- 优先级：P1
- 来源：Sprint 004 复盘行动项 / 用户输入
- 父需求：REQ-0000-build-design-system
- 子需求：REQ-0029-admin-list-foundation-components
- 关联 BUG：BUG-0055-admin-list-layout-unification
- 横切标签：admin-list

## 文档完整性

| 文件 | 状态 | 说明 |
|---|---|---|
| capture.md | 完成 | 初始需求记录 |
| requirement.md | 完成 | PRD，状态已同步为 approved |
| user-stories.md | 完成 | 管理员、开发、QA、产品、运营用户故事 |
| business-flow.md | 完成 | 当前问题流、目标流程、父/子需求差异 |
| acceptance.md | 完成 | 功能 AC、UI AC、安全 AC、文档 AC、横切 AC |
| prototype/web/admin-list-page-contract.html | 完成 | AdminListPage 静态验收样例 |
| prototype/web/admin-list-page-contract-context.md | 完成 | 原型说明与后续 design 优先级 |
| trace.md | 完成 | 关联、knowledge_base_refs、cross_cutting_tags |

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 |
|---|---|---:|
| admin-list | docs/knowledge-base/best-practices/admin-list-page-consistency.md | 8 |

复盘参考：`docs/knowledge-base/retrospectives/sprint-004-retrospective.md` §5/§6 指出 AdminListPage 模板、MetricCard / PaginationWindow 抽象是 BUG-0055 后续治理行动项。本需求已将 A-002 收敛为模板契约，并把 A-003 作为 `REQ-0029` 子需求边界。

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0055-admin-list-layout-unification | medium | done | fix-admin-list-layout-unification | 管理端 8 个列表页模块顺序、筛选、sticky 操作列与分页一致性经验来源 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-11 08:52:43 | lifecycle-stage-migrate | review → archive（/opsx-archive add-admin-list-page-contract） |
| 2026-07-11 08:52:36 | /opsx-archive | Change `add-admin-list-page-contract` 已归档，状态同步完成。 |
| 2026-07-11 08:52:36 | workflow-sync | 状态同步为 done（Change archived）。 |
| 2026-07-10 23:51:18 | /opsx-apply | Change `add-admin-list-page-contract` apply 完成，待 archive。 |
| 2026-07-10 20:40:55 | /req-opsx | 创建 OpenSpec Change `add-admin-list-page-contract`，状态 proposed。 |
| 2026-07-05 14:37:59 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-10 20:26:45 | /sprint-propose | 纳入 sprint-005 正式范围；当时下一步为创建 OpenSpec Change。 |
| 2026-07-04 15:17:26 | /req-capture | 创建需求记录，作为单一交付单元记录 AdminListPage 模板、管理端列表页契约与验收页需求。 |
| 2026-07-05 07:56:30 | /req-generate | 生成 requirement.md，明确 AdminListPage 模板、管理端列表页契约、设计验收页与 BUG-0055 经验吸收范围。 |
| 2026-07-05 10:18:38 | /req-complete | 补齐 user-stories、business-flow、acceptance、prototype，并写入 admin-list knowledge-base 横切 AC。 |
| 2026-07-05 14:36:29 | /req-review --approve | 评审通过，允许进入 /req-opsx 与后续 Sprint 编排。 |
