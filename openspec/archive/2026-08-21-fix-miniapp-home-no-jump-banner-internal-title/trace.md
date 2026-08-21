---
change_id: fix-miniapp-home-no-jump-banner-internal-title
status: archived
created_at: 2026-08-21 08:45:32
updated_at: 2026-08-21 15:07:32
source_bug: BUG-0130-miniapp-home-no-jump-banner-internal-title
sprint: sprint-024
---

# 变更追踪

```yaml
change_id: fix-miniapp-home-no-jump-banner-internal-title
status: archived
created_at: 2026-08-21 08:45:32
updated_at: 2026-08-21 15:07:32
source_bug: BUG-0130-miniapp-home-no-jump-banner-internal-title
sprint: sprint-024
related_specs:
  - miniapp-home
  - banner-management
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-21 15:07:32 | `/release-prepare v1.1.2` | 修正归档 trace 状态一致性：归档目录、Sprint 与 BUG trace 均已记录 archived，本文件同步为 archived。 |
| 2026-08-21 13:45:41 | `/opsx-archive BUG-0130` | 归档前验收补证：用户补充首页运行截图，确认首屏 Banner 无内部标题、无遮挡、不透明化；BUG acceptance 更新为 passed。 |
| 2026-08-21 13:11:41 | `/opsx-modify BUG-0130` | 验收返修：无跳转首页 Banner 点击后保持静默，不显示“内容建设中”；同步首页点击逻辑、静态测试和验收文档。 |
| 2026-08-21 09:15:20 | `/opsx-modify BUG-0130` | 验收返修：移除首页首屏 Banner 图片从左深到右浅的渐变遮罩，并取消 Banner 图片透明化；同步 Change spec/design/test-plan、BUG acceptance 和 Sprint 验收/发布说明。 |
| 2026-08-21 08:54:22 | `/opsx-apply BUG-0130` | 实现公开 Banner 标题净化、小程序搜索跳转兜底防泄露、API 文档语义更新与回归测试；当前缺小程序 DevTools/真机 render evidence，已记录为发布前补证项。 |
| 2026-08-21 08:45:32 | `/bug-opsx` | 基于 BUG-0130 创建修复 Change，状态为 proposed。 |
