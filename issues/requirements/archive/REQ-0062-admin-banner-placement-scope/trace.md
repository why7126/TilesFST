---
requirement_id: REQ-0062-admin-banner-placement-scope
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-20 13:23:12
updated_at: 2026-07-20 23:30:55
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0062-admin-banner-placement-scope
requirement_name: admin-banner-placement-scope
requirement_type: 管理端 / Banner 配置优化
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 本期
related_requirements:
  - REQ-0016-banner-management
  - REQ-0060-brand-list-page
related_changes:
  - update-admin-banner-placement-scope
lifecycle:
  captured: 2026-07-20 13:23:12
  generated: 2026-07-20 18:25:03
  completed: 2026-07-20 18:40:54
  reviewed: 2026-07-20 18:46:39
  approved: 2026-07-20 18:46:39
iteration: sprint-009
openspec_changes:
  - change_id: update-admin-banner-placement-scope
    type: update
    status: archived
readiness: Ready
readiness_notes: 五件套已补齐；UI 原型策略已提供 prototype/web/context.md 与 prototype.html，PNG 待后续导出但不阻塞评审。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/web/context.md
  - prototype/web/prototype.html
knowledge_base_refs:
  - docs/knowledge-base/README.md
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
cross_cutting_tags:
  - admin-list
  - admin-modal
  - media-upload
expected_openspec_change: update-admin-banner-placement-scope
```

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 将写入 acceptance 的 AC 条数 |
|---|---|---|
| admin-list | docs/knowledge-base/best-practices/admin-list-page-consistency.md | 4 |
| admin-modal | docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md | 3 |
| media-upload | docs/knowledge-base/best-practices/admin-media-upload-chain.md | 3 |

说明：本需求涉及 Banner 管理列表、筛选、弹窗和 Banner 图片上传回归边界，因此横切 AC 已写入 `acceptance.md` 的 `## 横切 AC（knowledge-base）`。最近复盘读取 `sprint-008-retrospective.md`，其中继续强调管理端 best-practice 复用、手工 evidence 与上下文预算约束；本 REQ 已将列表/弹窗/上传 gate 纳入验收，后续 OpenSpec design 需引用 `knowledge_base_refs`。

## 关联需求

| REQ | 关系 | 说明 |
|---|---|---|
| REQ-0016-banner-management | parent | 已交付的 Banner 管理基础能力，包含展示端、展示位置、图片、跳转和上下线规则 |
| REQ-0060-brand-list-page | related | 品牌列表页需要品牌页轮播数据来源，与本次展示位置新增/收敛相关 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-20 23:08:41 | lifecycle-stage-migrate | review → archive（/opsx-archive update-admin-banner-placement-scope） |
| 2026-07-20 23:08:05 | /opsx-archive | Change `update-admin-banner-placement-scope` 已归档，状态同步完成。 |
| 2026-07-20 23:03:04 | 文档更新 | 补充 Banner 跳转类型“品牌详情”的 requirement、acceptance、user-stories 与 business-flow 描述。 |
| 2026-07-20 19:59:43 | /opsx-apply | Change `update-admin-banner-placement-scope` apply 完成，待 archive。 |
| 2026-07-20 19:11:31 | `/sprint-propose` | 纳入 `sprint-009` 正式范围，关联 Change `update-admin-banner-placement-scope`，容量估算更新为 36.0/30.0 人天 |
| 2026-07-20 19:08:26 | `/req-opsx` | 修正未纳入 Sprint 的状态语义：保留 approved，等待后续 /sprint-propose |
| 2026-07-20 18:55:00 | `/req-opsx` | 创建 OpenSpec Change `update-admin-banner-placement-scope`，状态 proposed |
| 2026-07-20 18:47:22 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-20 18:46:39 | `/req-review --approve` | 需求评审通过，状态更新为 approved，准备迁移至 review 阶段目录 |
| 2026-07-20 18:40:54 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 prototype/web；读取管理端列表、弹窗、上传 best-practice 和 sprint-008 复盘，状态更新为 pending_review |
| 2026-07-20 18:25:03 | `/req-generate` | 生成管理后台 Banner 投放范围配置优化 requirement.md，并明确旧数据删除策略 |
| 2026-07-20 13:23:12 | `/capture` | 记录管理后台 Banner 展示端与展示位置配置范围优化 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-07-20 23:08:05 workflow-sync：状态同步为 done（Change archived）
