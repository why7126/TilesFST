---
bug_id: BUG-0067-home-recommendation-list-entry-routing
status: done
lifecycle_stage: archive
severity: medium
created_at: 2026-07-19 15:26:47
updated_at: 2026-07-19 19:33:13
lifecycle:
  captured: 2026-07-19 15:26:47
  generated: 2026-07-19 15:39:21
  completed: 2026-07-19 15:43:52
  reviewed: 2026-07-19 15:47:09
  approved: 2026-07-19 15:47:09
iteration: sprint-009
related_requirement: REQ-0047-product-list-common-component-application
related_change: null
source_change: add-miniapp-product-list-component
openspec_changes:
  - change_id: fix-miniapp-home-recommendation-routing
    type: fix
    status: archived
related_bugs: []
---

```yaml
bug_id: BUG-0067-home-recommendation-list-entry-routing
status: done
severity: medium
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-19 15:26:47
  generated: 2026-07-19 15:39:21
  completed: 2026-07-19 15:43:52
  reviewed: 2026-07-19 15:47:09
  approved: 2026-07-19 15:47:09
iteration: sprint-009
related_requirement: REQ-0047-product-list-common-component-application
related_change: null
source_change: add-miniapp-product-list-component
openspec_changes:
  - change_id: fix-miniapp-home-recommendation-routing
    type: fix
    status: archived
related_bugs: []
evidence: []
scope:
  component: home_recommendation_entry
  terminal: to_be_confirmed
  page: home
  suspected_areas:
    - recommendation list routing
    - ranking entry routing
    - search page fallback
readiness:
  bug: done
  root_cause: done
  workaround: done
  acceptance: done
  review: approved
  trace: done
  next: /opsx-archive fix-miniapp-home-recommendation-routing completed
```

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| 用户反馈 | 当前会话 | 首页新品推荐/热销推荐「查看更多」以及新品榜/热销榜入口当前全部进入搜索页，期望进入对应推荐商品列表页 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 19:31:40 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-home-recommendation-routing） |
| 2026-07-19 19:30:39 | /opsx-archive | Change `fix-miniapp-home-recommendation-routing` 已归档，状态同步完成。 |
| 2026-07-19 18:26:06 | /bug-opsx | 创建 OpenSpec Change：fix-miniapp-home-recommendation-routing |
| 2026-07-19 15:52:45 | /sprint-propose | 纳入 sprint-009 正式范围，容量估算 9.0/30.0 人天 |
| 2026-07-19 15:47:58 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-19 15:47:09 | /bug-review --approve | 评审通过，状态更新为 approved，准备迁入 review 阶段 |
| 2026-07-19 15:43:52 | /bug-complete | 补齐 root-cause、workaround、acceptance；状态更新为 pending_review |
| 2026-07-19 15:39:21 | /bug-generate | 生成 bug.md，关联 REQ-0047 与 add-miniapp-product-list-component，状态更新为 draft |
| 2026-07-19 15:26:47 | /capture | 记录首页推荐模块查看更多和榜单入口误跳搜索页的缺陷 |

- 2026-07-19 19:30:39 workflow-sync：状态同步为 done（Change archived）
