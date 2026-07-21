---
requirement_id: REQ-0061-miniapp-share-add-guide
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-19 23:38:10
updated_at: 2026-07-20 18:32:38
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0061-miniapp-share-add-guide
requirement_name: miniapp-share-add-guide
requirement_type: 小程序留存引导 / 分享入口提示
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: false
  web_catalog: false
  wechat_miniapp: true
related_requirements: []
related_changes: []
lifecycle:
  captured: 2026-07-19 23:38:10
  generated: 2026-07-19 23:45:31
  completed: 2026-07-19 23:50:36
  reviewed: 2026-07-20 00:09:20
  approved: 2026-07-20 00:09:20
iteration: sprint-009
openspec_changes:
  - change_id: add-miniapp-share-add-guide
    type: add
    status: archived
readiness: Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance、prototype 与 trace；待 req-review 评审确认关闭记忆策略和展示频率后进入 OpenSpec。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - prototype/miniapp/context.md
  - prototype/miniapp/prototype.html
  - review.md
expected_openspec_change: add-miniapp-share-add-guide
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
cross_cutting_tags: []
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-20 18:32:30 | lifecycle-stage-migrate | review → archive（/opsx-archive add-miniapp-share-add-guide） |
| 2026-07-20 18:32:11 | /opsx-archive | Change `add-miniapp-share-add-guide` 已归档，状态同步完成。 |
| 2026-07-20 18:28:41 | 用户验收反馈 | 用户确认已完成真机验收；REQ-0061 剩余归档阻断仅为 DevTools 320/375/430 pt evidence 任务 |
| 2026-07-20 15:45:32 | 文档同步 | 记录当前实现形态：引导语固定两行，第一行含右上角小/大/小三点提示符，定位采用胶囊 bottom + 8px 与 right 52px fallback |
| 2026-07-20 09:52:07 | `/opsx-apply --sprint auto` | Change `add-miniapp-share-add-guide` 进入 in_progress，完成 19/22；剩余 DevTools 320/375/430 pt evidence |
| 2026-07-20 08:34:38 | `/sprint-propose sprint-009` | 纳入 sprint-009 正式范围，关联 Change `add-miniapp-share-add-guide` |
| 2026-07-20 08:11:32 | `/req-opsx` | 创建 OpenSpec Change `add-miniapp-share-add-guide`，状态 proposed |
| 2026-07-20 00:11:42 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-20 00:09:20 | `/req-review --approve` | 评审通过，状态更新为 approved，准备从 plan 迁入 review 阶段 |
| 2026-07-19 23:50:36 | `/req-complete` | 补齐用户故事、业务流程、验收标准与小程序原型上下文，状态更新为 pending_review；knowledge-base 管理端横切标签 N/A，引用小程序自定义导航最佳实践 |
| 2026-07-19 23:45:31 | `/req-generate` | 生成小程序添加到我的小程序引导语 requirement.md，状态更新为 draft |
| 2026-07-19 23:38:10 | `/req-capture` | 记录小程序右上角分享按钮附近展示“添加到我的小程序”引导语，并允许用户手工关闭 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-07-20 18:32:11 workflow-sync：状态同步为 done（Change archived）
