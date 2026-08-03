---
bug_id: BUG-0109-miniapp-home-button-one-time-failure
status: done
severity: high
created_at: 2026-08-03 08:13:39
updated_at: 2026-08-03 10:22:09
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-03 08:13:39
  generated: 2026-08-03 08:19:58
  completed: 2026-08-03 08:22:19
  reviewed: 2026-08-03 08:26:07
  approved: 2026-08-03 08:26:07
iteration: sprint-018
openspec_changes:
  - change_id: fix-miniapp-home-navigation-repeat-click
    type: fix
    status: archived
related_requirement: null
related_bug: null
---

# BUG Trace

```yaml
bug_id: BUG-0109-miniapp-home-button-one-time-failure
status: done
severity: high
created_at: 2026-08-03 08:13:39
updated_at: 2026-08-03 08:39:19
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-03 08:13:39
  generated: 2026-08-03 08:19:58
  completed: 2026-08-03 08:22:19
  reviewed: 2026-08-03 08:26:07
  approved: 2026-08-03 08:26:07
iteration: sprint-018
openspec_changes:
  - change_id: fix-miniapp-home-navigation-repeat-click
    type: fix
    status: archived
related_requirement: null
related_bug: null
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-03 10:22:09 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-home-navigation-repeat-click） |
| 2026-08-03 10:21:23 | /opsx-archive | Change `fix-miniapp-home-navigation-repeat-click` 已归档，状态同步完成。 |
| 2026-08-03 08:59:57 | /opsx-apply | Change `fix-miniapp-home-navigation-repeat-click` apply 执行；后续已补齐验收并归档。 |
| 2026-08-03 08:39:19 | `/sprint-propose sprint-018` | 纳入 Sprint 018 正式范围，关联 Change `fix-miniapp-home-navigation-repeat-click`；后续已完成归档。 |
| 2026-08-03 08:34:05 | `/bug-opsx` | 创建 OpenSpec Change `fix-miniapp-home-navigation-repeat-click`；后续已纳入 sprint-018 并归档。 |
| 2026-08-03 08:26:36 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-03 08:26:07 | `/bug-review --approve` | 评审通过，确认修复；准备迁入 review 阶段并允许后续 bug-opsx 与 Sprint 规划。 |
| 2026-08-03 08:22:19 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，状态推进为 pending_review，等待评审确认是否修复。 |
| 2026-08-03 08:19:58 | `/bug-generate` | 生成正式缺陷稿 bug.md，补充现象、复现、期望/实际、影响范围和严重等级说明。 |
| 2026-08-03 08:13:39 | `/capture` | 记录小程序返回首页按钮每个页面点击一次后失效的问题，分类为 BUG。 |

- 2026-08-03 10:21:23 workflow-sync：状态同步为 done（Change archived）
