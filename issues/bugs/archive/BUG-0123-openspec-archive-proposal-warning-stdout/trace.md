---
bug_id: BUG-0123-openspec-archive-proposal-warning-stdout
status: done
severity: medium
created_at: 2026-08-06 12:10:56
updated_at: 2026-08-06 13:57:51
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-06 12:10:56
  generated: 2026-08-06 13:16:09
  enriching: 2026-08-06 13:18:13
  pending_review: 2026-08-06 13:18:13
  approved: 2026-08-06 13:34:43
related_requirement:
related_bug: BUG-0119-openspec-archive-scaffold-warning-noise
related_changes:
  - fix-openspec-archive-proposal-warning-stdout
openspec_changes:
  - change_id: fix-openspec-archive-proposal-warning-stdout
    type: fix
    status: archived
iteration: sprint-021
---

# BUG 追踪

```yaml
bug_id: BUG-0123-openspec-archive-proposal-warning-stdout
status: done
severity: medium
lifecycle_stage: archive
related_requirement:
related_bug: BUG-0119-openspec-archive-scaffold-warning-noise
related_changes:
  - fix-openspec-archive-proposal-warning-stdout
openspec_changes:
  - change_id: fix-openspec-archive-proposal-warning-stdout
    type: fix
    status: archived
iteration: sprint-021
```

## 基本信息

| 字段 | 值 |
|---|---|
| 标题 | OpenSpec CLI proposal warning 仍通过 stdout 出现在归档成功输出中 |
| 严重等级 | medium |
| 来源 | `/capture` |
| 相关需求 |  |
| 相关 Sprint |  |
| 相关历史缺陷 | BUG-0119-openspec-archive-scaffold-warning-noise |

## 影响范围

- `scripts/archive-change.sh` 成功路径输出
- `/opsx-archive` 验收体验
- OpenSpec CLI stdout/stderr 噪音过滤策略

## 建议验收或复现要点

- 归档中文优先 Change 时，stdout 不应展示已知 proposal scaffold warning。
- 未知 stdout/stderr 仍需保留并展示，避免吞掉真实异常或诊断信息。
- BUG-0119 已修复的自定义固定说明噪音不应回归。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-06 13:57:20 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-openspec-archive-proposal-warning-stdout） |
| 2026-08-06 13:57:15 | /opsx-archive | Change `fix-openspec-archive-proposal-warning-stdout` 已归档，状态同步完成。 |
| 2026-08-06 13:54:50 | /opsx-apply | Change `fix-openspec-archive-proposal-warning-stdout` 已完成实现验证，后续归档已闭环。 |
| 2026-08-06 13:45:35 | `/bug-opsx` | 创建 OpenSpec Change `fix-openspec-archive-proposal-warning-stdout`，后续已归档闭环。 |
| 2026-08-06 13:42:06 | `/sprint-propose sprint-021 --bug BUG-0123` | 纳入 sprint-021 正式范围，后续已交付闭环。 |
| 2026-08-06 13:35:02 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-06 13:34:43 | `/bug-review --approve` | 评审通过，确认修复。 |
| 2026-08-06 13:18:13 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，评审前资料完成。 |
| 2026-08-06 13:16:09 | `/bug-generate` | 生成 bug.md，缺陷记录初稿完成。 |
| 2026-08-06 12:10:56 | `/capture` | 记录 OpenSpec CLI proposal warning 仍通过 stdout 出现在归档成功输出中的问题。 |
