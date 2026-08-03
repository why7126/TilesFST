---
requirement_id: REQ-0085-miniapp-global-home-floating-button
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-30 22:53:04
updated_at: 2026-07-31 00:17:51
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0085-miniapp-global-home-floating-button
requirement_name: miniapp-global-home-floating-button
requirement_type: 小程序 / 全局导航
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 不涉及
  web_catalog: 不涉及
  wechat_miniapp: 本期
related_requirements: []
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
  - docs/knowledge-base/retrospectives/sprint-013-retrospective.md
related_changes: []
lifecycle:
  captured: 2026-07-30 22:53:04
  generated: 2026-07-30 23:03:26
  completed: 2026-07-30 23:12:00
  reviewed: 2026-07-30 23:12:47
  approved: 2026-07-30 23:12:47
iteration: sprint-014
openspec_changes:
  - change_id: add-miniapp-global-home-floating-button
    type: add
    status: archived
readiness: Ready
readiness_notes: 五件套已补齐，并已提供小程序原型策略；管理端横切 AC 不适用，小程序导航 best-practice 已写入验收。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/miniapp/context.md
  - prototype/miniapp/home-floating-button.html
expected_openspec_change: add-miniapp-global-home-floating-button
cross_cutting_tags:
  - miniapp
  - navigation
  - floating-button
  - miniapp-custom-navigation
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 00:14:39 | lifecycle-stage-migrate | review → archive（/opsx-archive add-miniapp-global-home-floating-button） |
| 2026-07-31 00:14:16 | /opsx-archive | Change `add-miniapp-global-home-floating-button` 已归档，状态同步完成。 |
| 2026-07-31 00:09:00 | /opsx-modify | Change `add-miniapp-global-home-floating-button` 验收返修已同步，待复验或 archive。 |
| 2026-07-30 23:49:27 | /opsx-apply | Change `add-miniapp-global-home-floating-button` apply 完成，待 archive。 |
| 2026-07-30 23:26:20 | `/sprint-propose sprint-014` | 纳入 Sprint 014 正式范围，关联 Change `add-miniapp-global-home-floating-button`。 |
| 2026-07-30 23:20:00 | `/req-opsx` | 创建 OpenSpec Change `add-miniapp-global-home-floating-button`，状态 proposed。 |
| 2026-07-30 23:13:23 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-30 23:12:47 | `/req-review --approve` | 评审通过小程序非首页返回首页悬浮按钮需求；后续可执行 /req-opsx。 |
| 2026-07-30 23:12:00 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与小程序原型策略；引用 miniapp-custom-navigation best-practice 与 sprint-013 小程序 evidence 复盘，状态进入 pending_review。 |
| 2026-07-30 23:03:26 | `/req-generate` | 生成小程序非首页返回首页全局悬浮按钮 requirement.md，状态进入 draft。 |
| 2026-07-30 22:53:04 | `/capture` | 记录小程序非首页新增全局返回首页悬浮按钮的导航需求。 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-07-31 00:13:57 workflow-sync：状态同步为 done（Change archived）
