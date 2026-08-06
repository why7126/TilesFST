---
bug_id: BUG-0121-stale-scan-pending-business-word
status: done
severity: medium
created_at: 2026-08-06 11:13:56
updated_at: 2026-08-06 13:10:28
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-06 11:13:56
  generated: 2026-08-06 11:23:14
  enriching: 2026-08-06 11:41:11
  pending_review: 2026-08-06 11:41:11
  approved: 2026-08-06 11:50:49
related_requirement:
related_bug:
related_changes:
  - fix-stale-scan-pending-business-word
openspec_changes:
  - change_id: fix-stale-scan-pending-business-word
    type: fix
    status: archived
iteration: sprint-021
---

# BUG 追踪

```yaml
bug_id: BUG-0121-stale-scan-pending-business-word
status: done
severity: medium
lifecycle_stage: archive
related_requirement:
related_bug:
related_changes:
  - fix-stale-scan-pending-business-word
openspec_changes:
  - change_id: fix-stale-scan-pending-business-word
    type: fix
    status: archived
iteration: sprint-021
```

## 基本信息

| 字段 | 值 |
|---|---|
| 标题 | stale scan 对业务词 P-word 误判为流程中间态 |
| 严重等级 | medium |
| 来源 | `/bug-capture` |
| 相关需求 |  |
| 相关 Sprint |  |
| 相关历史缺陷 |  |

## 影响范围

- `scripts/check-sprint-close-stale-scan.py`
- Sprint archive readiness
- Issue 文档写作规范

## 建议验收或复现要点

- 普通正文中的业务词 英文 P 词 应按上下文判断，不应被直接视为 Issue 中间态残留。
- 状态字段、状态表格和流程说明仍应严格扫描流程中间态。
- Sprint archive readiness 调用 stale scan 时，应保留对真实中间态残留的阻断能力。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-06 13:08:40 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-stale-scan-pending-business-word） |
| 2026-08-06 13:08:31 | /opsx-archive | Change `fix-stale-scan-pending-business-word` 已归档，状态同步完成。 |
| 2026-08-06 12:48:10 | /opsx-apply | Change `fix-stale-scan-pending-business-word` 已完成实现验证，后续归档已闭环。 |
| 2026-08-06 11:51:15 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-06 11:13:56 | `/bug-capture` | 记录 stale scan 将业务正文中的 P-word 误判为流程中间态残留的问题。 |
| 2026-08-06 11:23:14 | `/bug-generate` | 生成 bug.md，缺陷记录初稿完成。 |
| 2026-08-06 11:41:11 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，评审前资料完成。 |
| 2026-08-06 11:50:49 | `/bug-review --approve` | 评审通过，确认修复。 |
| 2026-08-06 11:55:30 | `/sprint-propose sprint-021 --bug BUG-0121` | 纳入 sprint-021 正式范围，后续已交付闭环。 |
| 2026-08-06 12:07:29 | `/bug-opsx` | 创建 OpenSpec Change `fix-stale-scan-pending-business-word`，后续已归档闭环。 |

- 2026-08-06 13:08:26 workflow-sync：状态同步为 done（Change archived）
