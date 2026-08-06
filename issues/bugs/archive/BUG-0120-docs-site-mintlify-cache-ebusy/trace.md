---
bug_id: BUG-0120-docs-site-mintlify-cache-ebusy
status: done
severity: medium
created_at: 2026-08-06 10:39:49
updated_at: 2026-08-06 11:49:50
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-06 10:39:49
  generated: 2026-08-06 10:53:38
  enriching: 2026-08-06 11:03:45
  pending_review: 2026-08-06 11:03:45
  approved: 2026-08-06 11:05:55
related_requirement: REQ-0094-mintlify-versioned-docs-directory
related_bug:
related_changes: []
openspec_changes:
  - change_id: fix-docs-site-mintlify-cache-ebusy
    type: fix
    status: archived
iteration: sprint-021
---

# BUG 追踪

```yaml
bug_id: BUG-0120-docs-site-mintlify-cache-ebusy
status: done
severity: medium
lifecycle_stage: review
related_requirement: REQ-0094-mintlify-versioned-docs-directory
related_bug:
related_changes: []
openspec_changes:
  - change_id: fix-docs-site-mintlify-cache-ebusy
    type: fix
    status: archived
iteration: sprint-021
```

## 基本信息

| 字段 | 值 |
|---|---|
| 标题 | tilesfst-docs-site Mintlify 缓存 volume 导致 EBUSY 启动失败 |
| 严重等级 | medium |
| 来源 | `/bug-capture` |
| 相关需求 | REQ-0094-mintlify-versioned-docs-directory |
| 相关 Sprint |  |
| 相关历史缺陷 |  |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-06 11:24:39 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-docs-site-mintlify-cache-ebusy） |
| 2026-08-06 11:24:20 | /opsx-archive | Change `fix-docs-site-mintlify-cache-ebusy` 已归档，状态同步完成。 |
| 2026-08-06 11:19:01 | /opsx-apply | Change `fix-docs-site-mintlify-cache-ebusy` 已完成实现验证，后续归档已闭环。 |
| 2026-08-06 11:06:17 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-06 10:39:49 | `/bug-capture` | 记录 tilesfst-docs-site 因 Mintlify 缓存 volume 挂载点重命名冲突导致 EBUSY 启动失败的问题。 |
| 2026-08-06 10:53:38 | `/bug-generate` | 生成 bug.md，缺陷记录初稿完成。 |
| 2026-08-06 11:03:45 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，评审前资料完成。 |
| 2026-08-06 11:05:55 | `/bug-review --approve` | 评审通过，确认修复。 |
| 2026-08-06 11:09:17 | `/bug-opsx` | 创建 OpenSpec Change `fix-docs-site-mintlify-cache-ebusy`，后续已归档闭环。 |
| 2026-08-06 11:13:44 | `/sprint-propose sprint-021` | 纳入 sprint-021 正式范围，并关联 Change `fix-docs-site-mintlify-cache-ebusy`。 |

- 2026-08-06 11:24:20 workflow-sync：状态同步为 done（Change archived）
