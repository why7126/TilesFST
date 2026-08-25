---
bug_id: BUG-0134-miniapp-certificate-detail-display-url
status: done
severity: high
created_at: 2026-08-22 20:38:13
updated_at: 2026-08-24 18:03:05
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-22 20:38:13
  generated: 2026-08-22 21:06:04
  completed: 2026-08-22 21:08:06
  reviewed: 2026-08-22 21:13:19
  approved: 2026-08-22 21:13:19
iteration: sprint-025
openspec_changes:
  - change_id: fix-miniapp-certificate-detail-display-url
    type: fix
    status: archived
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0112-certificate-image-object-key-prefix
related_change: fix-miniapp-certificate-detail-display-url
---

# BUG Trace

```yaml
bug_id: BUG-0134-miniapp-certificate-detail-display-url
status: done
severity: high
created_at: 2026-08-22 20:38:13
updated_at: 2026-08-22 21:13:19
lifecycle_stage: review
lifecycle:
  captured: 2026-08-22 20:38:13
  generated: 2026-08-22 21:06:04
  completed: 2026-08-22 21:08:06
  reviewed: 2026-08-22 21:13:19
  approved: 2026-08-22 21:13:19
iteration: sprint-025
openspec_changes:
  - change_id: fix-miniapp-certificate-detail-display-url
    type: fix
    status: archived
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0112-certificate-image-object-key-prefix
related_change: fix-miniapp-certificate-detail-display-url
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-24 17:15:12 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-certificate-detail-display-url） |
| 2026-08-24 17:15:07 | /opsx-archive | Change `fix-miniapp-certificate-detail-display-url` 已归档，状态同步完成。 |
| 2026-08-23 08:33:53 | /opsx-modify | Change `fix-miniapp-certificate-detail-display-url` 验收返修已同步，待复验或 archive。 |
| 2026-08-22 21:50:48 | /opsx-apply | Change `fix-miniapp-certificate-detail-display-url` apply 完成，待 archive。 |
| 2026-08-22 21:41:50 | /opsx-apply | Change `fix-miniapp-certificate-detail-display-url` apply 进行中，待补齐剩余验收。 |
| 2026-08-22 21:14:54 | lifecycle-stage-migrate | plan → review（/bug-review） |
| 2026-08-22 20:38:13 | `/capture` | 记录证书详情页顶部展示缺少 `display_url`，导致详情展示可能直接退回原图的问题。 |
| 2026-08-22 21:06:04 | `/bug-generate` | 根据 capture 生成 `bug.md`，状态更新为 draft。 |
| 2026-08-22 21:08:06 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，状态更新为 pending_review。 |
| 2026-08-22 21:13:19 | `/bug-review` | 评审通过，状态更新为 approved。 |
| 2026-08-22 21:20:13 | `/sprint-propose` | 纳入 sprint-025，完成迭代范围登记。 |
| 2026-08-22 21:26:55 | `/bug-opsx` | 创建 OpenSpec Change `fix-miniapp-certificate-detail-display-url` 并完成初始追踪登记。 |

- 2026-08-24 17:15:07 workflow-sync：状态同步为 done（Change archived）
