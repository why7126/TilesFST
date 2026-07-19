---
requirement_id: REQ-0047-product-list-common-component-application
status: done
priority: P1
created_at: 2026-07-19 01:02:16
updated_at: 2026-07-19 15:55:25
lifecycle:
  captured: 2026-07-19 01:02:16
  generated: 2026-07-19 01:21:11
  completed: 2026-07-19 01:25:41
  reviewed: 2026-07-19 01:37:13
  approved: 2026-07-19 01:37:13
iteration: sprint-008
openspec_changes:
  - change_id: add-miniapp-product-list-component
    type: add
    status: archived
related_requirements: []
knowledge_base_refs: []
cross_cutting_tags: []
retrospective_refs:
  - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
lifecycle_stage: archive
---

# Trace

```yaml
requirement_id: REQ-0047-product-list-common-component-application
status: done
priority: P1
created_at: 2026-07-19 01:02:16
updated_at: 2026-07-19 01:50:36
lifecycle:
  captured: 2026-07-19 01:02:16
  generated: 2026-07-19 01:21:11
  completed: 2026-07-19 01:25:41
  reviewed: 2026-07-19 01:37:13
  approved: 2026-07-19 01:37:13
iteration: sprint-008
openspec_changes:
  - change_id: add-miniapp-product-list-component
    type: add
    status: archived
related_requirements: []
knowledge_base_refs: []
cross_cutting_tags: []
retrospective_refs:
  - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
lifecycle_stage: review
```

## 关联需求

| REQ | 关系 | 说明 |
|---|---|---|
| REQ-0045-category-list-page | upstream | 分类列表页可能提供商品列表上下文或复用部分列表能力 |
| REQ-0046-search-component-application | upstream | 商品列表页可复用搜索通用组件作为查询入口 |

## Knowledge-base Cross-cutting

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 |
|---|---|---:|
| 无匹配标签 | 无横切 AC；本需求为微信小程序商品列表体验，不涉及管理端列表/表单/弹窗/上传 | 0 |

最近复盘参考：`docs/knowledge-base/retrospectives/sprint-007-retrospective.md`。与本 REQ 相关的复发预防点为列表类能力后续实现阶段应分层验收，且 Workflow Sync / AI usage hook 成功路径保持 compact summary。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 15:20:18 | lifecycle-stage-migrate | review → archive（/opsx-archive add-miniapp-product-list-component） |
| 2026-07-19 15:18:30 | /opsx-archive | Change `add-miniapp-product-list-component` 已归档，状态同步完成。 |
| 2026-07-19 02:23:56 | /opsx-apply | Change `add-miniapp-product-list-component` apply 完成，待 archive。 |
| 2026-07-19 01:50:36 | /req-opsx | 创建 OpenSpec Change：add-miniapp-product-list-component |
| 2026-07-19 01:42:28 | /sprint-propose | 纳入 sprint-008，状态进入 in_sprint；后续先 /req-opsx |
| 2026-07-19 01:38:06 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-19 01:37:13 | /req-review --approve | 需求评审通过，状态进入 approved，阶段 plan → review |
| 2026-07-19 01:25:41 | /req-complete | 补齐 user-stories、business-flow、acceptance 与小程序原型；Knowledge-base gate 为 N/A；状态进入 pending_review |
| 2026-07-19 01:21:11 | /req-generate | 生成 requirement.md，状态进入 draft；范围收敛为微信小程序商品列表页通用组件与应用 |
| 2026-07-19 01:02:16 | /req-capture | 捕获需求：新增商品列表页通用组件并应用 |

- 2026-07-19 15:18:30 workflow-sync：状态同步为 done（Change archived）

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0067-home-recommendation-list-entry-routing | medium | in_sprint | — | 首页推荐模块查看更多和榜单入口误跳搜索页 |
