---
bug_id: BUG-0147-miniapp-certificate-list-images-missing
status: done
severity: high
created_at: 2026-08-30 10:23:23
updated_at: 2026-08-30 14:38:12
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-30 10:23:23
  generated: 2026-08-30 10:27:21
  completed: 2026-08-30 10:28:24
  reviewed: 2026-08-30 10:31:55
  approved: 2026-08-30 10:31:55
iteration: sprint-028
openspec_changes:
  - change_id: fix-miniapp-certificate-media-urls
    type: fix
    status: archived
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0135-miniapp-certificate-card-file-url-fallback
related_change: fix-miniapp-certificate-media-urls
---

# BUG Trace

```yaml
bug_id: BUG-0147-miniapp-certificate-list-images-missing
status: done
severity: high
created_at: 2026-08-30 10:23:23
updated_at: 2026-08-30 11:49:41
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-30 10:23:23
  generated: 2026-08-30 10:27:21
  completed: 2026-08-30 10:28:24
  reviewed: 2026-08-30 10:31:55
  approved: 2026-08-30 10:31:55
iteration: sprint-028
openspec_changes:
  - change_id: fix-miniapp-certificate-media-urls
    type: fix
    status: archived
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0135-miniapp-certificate-card-file-url-fallback
related_change: fix-miniapp-certificate-media-urls
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-30 11:49:41 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-certificate-media-urls） |
| 2026-08-30 11:49:33 | /opsx-archive | Change `fix-miniapp-certificate-media-urls` 已归档，状态同步完成。 |
| 2026-08-30 11:15:56 | /opsx-apply | Change `fix-miniapp-certificate-media-urls` 进入实现阶段；最终验收与归档结果见后续 `/opsx-archive` 记录。 |
| 2026-08-30 10:48:49 | `/bug-opsx` | 创建 OpenSpec Change `fix-miniapp-certificate-media-urls` 并回填 sprint-028。 |
| 2026-08-30 10:40:32 | `/sprint-propose` | 已纳入 sprint-028 正式范围；后续已创建并归档 OpenSpec Change。 |
| 2026-08-30 10:33:35 | `/bug-review` | 根因 confirmed 门禁通过，评审结果 approved，等待纳入 Sprint。 |
| 2026-08-30 10:32:29 | lifecycle-stage-migrate | plan → review（/bug-review） |
| 2026-08-30 10:28:24 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，根因状态为 confirmed，BUG 进入待评审。 |
| 2026-08-30 10:23:23 | `/bug-capture` | 记录生产小程序证书列表页图片类证书缺少 `thumbnail_url`，导致卡片全部显示“证书”占位的问题。 |

- 2026-08-30 11:49:33 workflow-sync：状态同步为 done（Change archived）
