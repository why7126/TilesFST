---
requirement_id: REQ-0049-miniapp-product-card-component
status: in_sprint
priority: P1
created_at: 2026-07-19 12:04:38
updated_at: 2026-07-19 12:50:12
lifecycle:
  captured: 2026-07-19 12:04:38
  generated: 2026-07-19 12:30:20
  completed: 2026-07-19 12:36:55
  reviewed: 2026-07-19 12:43:14
  approved: 2026-07-19 12:43:14
iteration: sprint-009
openspec_changes: []
related_requirements:
  - REQ-0047-product-list-common-component-application
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
cross_cutting_tags: []
lifecycle_stage: review
---

# Trace

```yaml
requirement_id: REQ-0049-miniapp-product-card-component
status: in_sprint
priority: P1
created_at: 2026-07-19 12:04:38
updated_at: 2026-07-19 12:50:12
lifecycle:
  captured: 2026-07-19 12:04:38
  generated: 2026-07-19 12:30:20
  completed: 2026-07-19 12:36:55
  reviewed: 2026-07-19 12:43:14
  approved: 2026-07-19 12:43:14
iteration: sprint-009
openspec_changes: []
related_requirements:
  - REQ-0047-product-list-common-component-application
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
cross_cutting_tags: []
lifecycle_stage: review
```

## 关联需求

| REQ | 关系 | 说明 |
|---|---|---|
| REQ-0047-product-list-common-component-application | parent | 商品卡片组件是微信小程序商品列表通用能力的子需求，面向各类列表页复用 |

## Knowledge-base Cross-cutting

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 |
|---|---|---:|
| 无匹配标签 | 无横切 AC；本需求为微信小程序商品卡片组件，不涉及管理端列表/表单/弹窗或媒体上传 | 0 |

最近复盘参考：`docs/knowledge-base/retrospectives/sprint-007-retrospective.md`。与本 REQ 直接相关的复发预防点为命令输出保持 compact summary、UI/业务能力后续实现阶段注意分层验收；管理端列表/弹窗/上传横切 gate 不适用。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 12:50:12 | /sprint-propose | 纳入 sprint-009，状态进入 in_sprint；后续先 /req-opsx |
| 2026-07-19 12:44:21 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-19 12:43:14 | /req-review --approve | 需求评审通过，状态进入 approved，阶段 plan → review |
| 2026-07-19 12:36:55 | /req-complete | 补齐 user-stories、business-flow、acceptance 与小程序原型；Knowledge-base gate 为 N/A；状态进入 pending_review |
| 2026-07-19 12:30:20 | /req-generate | 生成 requirement.md，状态进入 draft；范围收敛为微信小程序商品卡片组件 |
| 2026-07-19 12:04:38 | /req-capture | 捕获需求：微信小程序商品卡片组件 |
