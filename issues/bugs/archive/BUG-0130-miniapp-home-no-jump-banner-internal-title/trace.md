---
bug_id: BUG-0130-miniapp-home-no-jump-banner-internal-title
status: done
severity: medium
created_at: 2026-08-21 08:30:25
updated_at: 2026-08-21 14:44:50
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-21 08:30:25
  generated: 2026-08-21 08:33:49
  completed: 2026-08-21 08:37:23
  reviewed: 2026-08-21 08:39:53
  approved: 2026-08-21 08:39:53
iteration: sprint-024
openspec_changes:
  - change_id: fix-miniapp-home-no-jump-banner-internal-title
    type: fix
    status: archived
related_requirement: null
related_bug: null
---

# BUG Trace

```yaml
bug_id: BUG-0130-miniapp-home-no-jump-banner-internal-title
status: done
severity: medium
created_at: 2026-08-21 08:30:25
updated_at: 2026-08-21 08:54:22
lifecycle_stage: review
lifecycle:
  captured: 2026-08-21 08:30:25
  generated: 2026-08-21 08:33:49
  completed: 2026-08-21 08:37:23
  reviewed: 2026-08-21 08:39:53
  approved: 2026-08-21 08:39:53
iteration: sprint-024
openspec_changes:
  - change_id: fix-miniapp-home-no-jump-banner-internal-title
    type: fix
    status: archived
related_requirement: null
related_bug: null
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-21 14:39:15 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-home-no-jump-banner-internal-title） |
| 2026-08-21 14:39:12 | /opsx-archive | Change `fix-miniapp-home-no-jump-banner-internal-title` 已归档，状态同步完成。 |
| 2026-08-21 09:17:02 | /opsx-modify | Change `fix-miniapp-home-no-jump-banner-internal-title` 验收返修已同步，待复验或 archive。 |
| 2026-08-21 08:57:07 | /opsx-apply | Change `fix-miniapp-home-no-jump-banner-internal-title` apply 完成，待 archive。 |
| 2026-08-21 08:54:22 | `/opsx-apply BUG-0130` | 已实现 Change `fix-miniapp-home-no-jump-banner-internal-title`，完成后端 DTO 净化、小程序点击兜底、API 文档和回归测试；小程序 DevTools/真机 render evidence 待发布前补充。 |
| 2026-08-21 08:45:32 | `/bug-opsx` | 创建修复 Change `fix-miniapp-home-no-jump-banner-internal-title` 并回填 `sprint-024`。 |
| 2026-08-21 08:43:14 | `/sprint-propose sprint-024 --bug BUG-0130` | 纳入 `sprint-024` 正式范围，等待 `/bug-opsx` 创建修复 Change。 |
| 2026-08-21 08:40:24 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-21 08:39:53 | `/bug-review --approve` | 用户确认批准修复，状态推进为 `approved`，准备纳入 Sprint。 |
| 2026-08-21 08:37:23 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，根因状态为 probable，状态推进为 `pending_review`。 |
| 2026-08-21 08:33:49 | `/bug-generate` | 基于 capture 和探索结论生成正式 `bug.md`，状态推进为 `draft`。 |
| 2026-08-21 08:30:25 | `/bug-capture` | 记录小程序首页无跳转轮播图显示 `internal-MINIAPP_HOME_NO_JUMP-...` 内部标题的问题，用户截图显示内部标识覆盖在轮播图画面上。 |

- 2026-08-21 14:39:12 workflow-sync：状态同步为 done（Change archived）
