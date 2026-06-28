---
requirement_id: REQ-0010-product-version-display
status: done
lifecycle_stage: archive
priority: P2
created_at: 2026-06-27 09:06:02
updated_at: 2026-06-27 22:33:15
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0010-product-version-display
requirement_name: product-version-display
requirement_type: 前端 / 体验
priority: P2
status: done
owner: product
source: 产品反馈
target_clients:
  web_admin: 本期
  web_catalog: 本期
  wechat_miniapp: 不涉及
related_requirements:
  - REQ-0004-admin-home
lifecycle:
  captured: 2026-06-27 09:06:02
  generated: 2026-06-27 10:18:13
  completed: 2026-06-27 10:21:38
  reviewed: 2026-06-27 10:24:50
  approved: 2026-06-27 10:24:50
iteration: sprint-002
openspec_changes:
  - change_id: add-product-version-display
    type: add
    status: archived
documents:
  capture: issues/requirements/archive/REQ-0010-product-version-display/capture.md
  requirement: issues/requirements/archive/REQ-0010-product-version-display/requirement.md
  user_stories: issues/requirements/archive/REQ-0010-product-version-display/user-stories.md
  business_flow: issues/requirements/archive/REQ-0010-product-version-display/business-flow.md
  acceptance: issues/requirements/archive/REQ-0010-product-version-display/acceptance.md
  review: issues/requirements/archive/REQ-0010-product-version-display/review.md
  prototype:
    admin: prototype/web/product-version-sidebar-admin.html
    catalog: prototype/web/product-version-sidebar-catalog.html
    context: prototype/web/product-version-display-context.md
    reference_png: prototype/web/images/sidebar-version-reference.png```

## Readiness

| 级别 | 说明 |
|------|------|
| **Ready** | 评审通过；五件套 + review 齐；HTML 原型 + 参考 PNG 已决；实现 PNG 为 apply 阶段条件项 |

## 变更记录

| 2026-06-27 22:33:15 | lifecycle-stage-migrate | 迁入 `archive/`（status → stage 映射） |
| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 09:06:02 | `/req-capture` | 创建 capture.md 与 trace 壳；status → captured |
| 2026-06-27 10:18:13 | `/req-generate` | 生成 requirement.md；探索结论纳入 PRD；status → draft |
| 2026-06-27 10:21:38 | `/req-complete` | 补齐 user-stories、business-flow、acceptance、prototype；status → pending_review |
| 2026-06-27 10:24:50 | `/req-review --approve` | 评审通过；status → approved |
| 2026-06-27 10:30:22 | `/sprint-propose` | 纳入 sprint-002；status → in_sprint |
| 2026-06-27 10:32:54 | `/req-opsx` | 创建 OpenSpec `add-product-version-display`；status proposed |
| 2026-06-27 10:49:48 | `/opsx-apply` | 实现双端 version pill；openspec status → applied |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0013-product-version-ui-inconsistency | medium | done | fix-product-version-ui-inconsistency | 产品版本号 UI 与原型及 Design System 不一致 |
