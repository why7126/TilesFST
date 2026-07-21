---
requirement_id: REQ-0050-miniapp-brand-header-page-title-rules
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-19 14:14:10
updated_at: 2026-07-19 21:00:32
lifecycle:
  captured: 2026-07-19 14:14:10
  generated: 2026-07-19 14:23:10
  completed: 2026-07-19 14:26:30
  reviewed: 2026-07-19 14:30:27
  approved: 2026-07-19 14:30:27
iteration: sprint-009
openspec_changes:
  - change_id: update-miniapp-brand-header-title-rules
    type: update
    status: archived
related_requirements:
  - REQ-0048-miniapp-global-custom-navigation-bar
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
cross_cutting_tags:
  - miniapp
  - navigation
readiness: Ready
---

# Trace

```yaml
requirement_id: REQ-0050-miniapp-brand-header-page-title-rules
status: done
priority: P1
created_at: 2026-07-19 14:14:10
updated_at: 2026-07-19 18:14:48
lifecycle_stage: review
lifecycle:
  captured: 2026-07-19 14:14:10
  generated: 2026-07-19 14:23:10
  completed: 2026-07-19 14:26:30
  reviewed: 2026-07-19 14:30:27
  approved: 2026-07-19 14:30:27
iteration: sprint-009
openspec_changes:
  - change_id: update-miniapp-brand-header-title-rules
    type: update
    status: archived
related_requirements:
  - REQ-0048-miniapp-global-custom-navigation-bar
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
cross_cutting_tags:
  - miniapp
  - navigation
readiness: Ready
```

## 关联需求

| 需求 | 关系 | 说明 |
|---|---|---|
| REQ-0048-miniapp-global-custom-navigation-bar | parent | 本需求细化父需求的首页 / 非首页文案规则。 |
| REQ-0042-custom-navigation-bar | upstream | 首页品牌自定义导航栏和原生胶囊避让基础。 |
| REQ-0044-miniapp-sku-detail-page | covered-page | 商品详情页标题固定为 `商品详情`。 |
| REQ-0046-search-component-application | covered-page | 搜索页标题固定为 `搜索`。 |
| REQ-0047-product-list-common-component-application | covered-page | 商品列表页使用一行列表标题。 |

## 文档清单

| 文档 | 状态 |
|---|---|
| capture.md | done |
| requirement.md | approved |
| user-stories.md | pending_review |
| business-flow.md | pending_review |
| acceptance.md | pending_review |
| review.md | approved |
| prototype/miniapp/context.md | pending_review |
| prototype/miniapp/brand-header-title-rules.html | pending_review |

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 将写入 acceptance 的 AC 条数 |
|---|---|---|
| 无管理端横切标签 | N/A | 0 |

说明：本 REQ 为小程序导航 UI，不命中 `admin-list`、`admin-form`、`admin-modal`、`media-upload`。已参考 `docs/knowledge-base/retrospectives/sprint-007-retrospective.md` 的分层验收、compact 输出和范围控制经验，转化为功能 AC、范围 AC 与测试 AC。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 20:51:50 | lifecycle-stage-migrate | review → archive（/opsx-archive update-miniapp-brand-header-title-rules） |
| 2026-07-19 20:50:44 | /opsx-archive | Change `update-miniapp-brand-header-title-rules` 已归档，状态同步完成。 |
| 2026-07-19 20:48:01 | /opsx-apply | Change `update-miniapp-brand-header-title-rules` apply 完成，待 archive。 |
| 2026-07-19 18:14:48 | /req-opsx REQ-0050 | 创建 OpenSpec Change `update-miniapp-brand-header-title-rules`，状态为 proposed。 |
| 2026-07-19 14:40:17 | /sprint-propose sprint-009 | 纳入 sprint-009 正式范围，状态更新为 in_sprint；待 `/req-opsx` 创建 OpenSpec Change 后进入实现。 |
| 2026-07-19 14:32:03 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-19 14:30:27 | /req-review --approve | 需求评审通过，状态更新为 approved，准备迁入 review 阶段目录。 |
| 2026-07-19 14:26:30 | /req-complete | 补齐 user-stories、business-flow、acceptance 与 miniapp prototype；未命中管理端横切 AC，参考 sprint-007 复盘的分层验收与范围控制经验，状态更新为 pending_review。 |
| 2026-07-19 14:23:10 | /req-generate | 生成 requirement.md，需求状态由 captured 更新为 draft。 |
| 2026-07-19 14:14:10 | /req-capture | 捕获小程序 brand-header 页面标题规则需求，作为 REQ-0048 全局自定义导航栏的文案与交互细化。 |

- 2026-07-19 20:50:44 workflow-sync：状态同步为 done（Change archived）
