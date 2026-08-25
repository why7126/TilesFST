---
bug_id: BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml
status: done
severity: medium
created_at: 2026-08-25 09:28:29
updated_at: 2026-08-25 10:22:38
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-25 09:28:29
  generated: null
  completed: 2026-08-25 09:44:00
  reviewed: 2026-08-25 09:46:24
  approved: 2026-08-25 09:46:24
iteration: sprint-025
openspec_changes:
  - change_id: fix-workflow-sync-trace-frontmatter-invalid-yaml
    type: update
    status: archived
related_requirement: null
related_bug: null
related_change: fix-workflow-sync-trace-frontmatter-invalid-yaml
---

# BUG Trace

```yaml
bug_id: BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml
status: done
severity: medium
created_at: 2026-08-25 09:28:29
updated_at: 2026-08-25 09:46:56
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-25 09:28:29
  generated: null
  completed: 2026-08-25 09:44:00
  reviewed: 2026-08-25 09:46:24
  approved: 2026-08-25 09:46:24
iteration: sprint-025
openspec_changes:
  - change_id: fix-workflow-sync-trace-frontmatter-invalid-yaml
    type: update
    status: archived
related_requirement: null
related_bug: null
related_change: fix-workflow-sync-trace-frontmatter-invalid-yaml
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-25 10:21:57 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-workflow-sync-trace-frontmatter-invalid-yaml） |
| 2026-08-25 10:21:52 | /opsx-archive | Change `fix-workflow-sync-trace-frontmatter-invalid-yaml` 已归档，状态同步完成。 |
| 2026-08-25 10:12:49 | /opsx-apply | Change `fix-workflow-sync-trace-frontmatter-invalid-yaml` apply 完成，待 archive。 |
| 2026-08-25 09:46:50 | lifecycle-stage-migrate | plan → review（/bug-review） |
| 2026-08-25 09:46:24 | `/bug-review` | 根因 confirmed 门禁通过，评审通过，建议纳入 Sprint 后创建修复 Change。 |
| 2026-08-25 09:44:00 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；根因状态为 confirmed，待评审。 |
| 2026-08-25 09:28:29 | `/bug-capture` | 记录 Workflow Sync 写入 REQ trace frontmatter 可能生成非法 YAML 结构的问题；来源为 `/explore` 对脚本与现场 REQ trace 的只读调查。 |
