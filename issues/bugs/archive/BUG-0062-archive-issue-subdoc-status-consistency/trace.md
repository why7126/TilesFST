---
bug_id: BUG-0062-archive-issue-subdoc-status-consistency
status: done
lifecycle_stage: archive
created_at: 2026-07-11 13:19:58
updated_at: 2026-07-11 20:14:49
---

```yaml
status: done
lifecycle:
  captured: 2026-07-11 13:19:58
  draft: 2026-07-11 16:01:10
  enriching: 2026-07-11 16:05:13
  pending_review: 2026-07-11 16:05:13
  approved: 2026-07-11 16:08:19
openspec_changes:
  - change_id: fix-archive-issue-subdoc-status-consistency
    type: fix
    status: archived
related_requirement:
related_change: fix-archive-issue-subdoc-status-consistency
iteration: sprint-006
```

# Trace

## 变更记录

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-07-11 20:14:41 | lifecycle-stage-migrate | review → archive（/sprint-archive sprint-006） |
| 2026-07-11 20:12:27 | /opsx-archive | Change `fix-archive-issue-subdoc-status-consistency` 已归档，状态同步完成。 |
| 2026-07-11 18:06:21 | /opsx-apply | Change `fix-archive-issue-subdoc-status-consistency` apply 完成，待 archive。 |
| 2026-07-11 16:13:13 | bug-opsx | 创建 `fix-archive-issue-subdoc-status-consistency` |
| 2026-07-11 16:08:58 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-11 16:08:19 | bug-review | Approved，允许进入 OpenSpec fix 流程 |
| 2026-07-11 16:05:13 | bug-complete | 补齐 root-cause、workaround、acceptance，状态进入 pending_review |
| 2026-07-11 16:01:10 | bug-generate | 生成 `bug.md`，状态进入 draft |
| 2026-07-11 13:19:58 | bug-capture | 记录归档后 issue 子文档状态一致性检查缺失 |

- 2026-07-11 20:12:27 workflow-sync：状态同步为 done（Change archived）
