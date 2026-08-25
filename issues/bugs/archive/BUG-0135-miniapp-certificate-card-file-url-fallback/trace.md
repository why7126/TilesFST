---
bug_id: BUG-0135-miniapp-certificate-card-file-url-fallback
status: done
severity: high
created_at: 2026-08-22 20:38:13
updated_at: 2026-08-22 22:01:19
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-22 20:38:13
  generated: 2026-08-22 21:06:57
  completed: 2026-08-22 21:11:44
  reviewed: 2026-08-22 21:15:46
  approved: 2026-08-22 21:15:46
iteration: sprint-025
openspec_changes:
  - change_id: fix-miniapp-certificate-card-file-url-fallback
    type: fix
    status: archived
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0112-certificate-image-object-key-prefix
related_change: fix-miniapp-certificate-card-file-url-fallback
---

# BUG Trace

```yaml
bug_id: BUG-0135-miniapp-certificate-card-file-url-fallback
status: done
severity: high
created_at: 2026-08-22 20:38:13
updated_at: 2026-08-22 21:30:50
lifecycle_stage: review
lifecycle:
  captured: 2026-08-22 20:38:13
  generated: 2026-08-22 21:06:57
  completed: 2026-08-22 21:11:44
  reviewed: 2026-08-22 21:15:46
  approved: 2026-08-22 21:15:46
iteration: sprint-025
openspec_changes:
  - change_id: fix-miniapp-certificate-card-file-url-fallback
    type: fix
    status: archived
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0112-certificate-image-object-key-prefix
related_change: fix-miniapp-certificate-card-file-url-fallback
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-22 21:59:33 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-certificate-card-file-url-fallback） |
| 2026-08-22 21:59:26 | /opsx-archive | Change `fix-miniapp-certificate-card-file-url-fallback` 已归档，状态同步完成。 |
| 2026-08-22 21:51:54 | /opsx-apply | Change `fix-miniapp-certificate-card-file-url-fallback` apply 完成，待 archive。 |
| 2026-08-22 21:44:39 | /opsx-apply | Change `fix-miniapp-certificate-card-file-url-fallback` apply 进行中，待补齐剩余验收。 |
| 2026-08-22 21:30:50 | `/bug-opsx` | 创建修复 Change `fix-miniapp-certificate-card-file-url-fallback`，等待 `/opsx-apply BUG-0135`。 |
| 2026-08-22 21:22:34 | `/sprint-propose --bug BUG-0135` | 纳入 `sprint-025` 正式范围，等待 `/bug-opsx` 创建修复 Change。 |
| 2026-08-22 21:16:33 | lifecycle-stage-migrate | plan → review（/bug-review） |
| 2026-08-22 21:15:46 | `/bug-review` | 默认评审通过，状态更新为 approved，准备迁入 review 阶段。 |
| 2026-08-22 21:11:44 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，状态进入 pending_review。 |
| 2026-08-22 21:06:57 | `/bug-generate` | 根据 capture 生成正式 `bug.md`，状态更新为 draft。 |
| 2026-08-22 20:38:13 | `/capture` | 记录证书卡缺缩略图时 fallback 到 `file_url` 原文件，而非优先占位的问题。 |

- 2026-08-22 21:59:26 workflow-sync：状态同步为 done（Change archived）
