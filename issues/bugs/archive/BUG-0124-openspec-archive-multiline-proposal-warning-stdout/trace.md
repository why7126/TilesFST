---
bug_id: BUG-0124-openspec-archive-multiline-proposal-warning-stdout
status: done
severity: medium
created_at: 2026-08-06 14:02:15
updated_at: 2026-08-06 15:09:19
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-06 14:02:15
  generated: 2026-08-06 14:09:46
  enriching: 2026-08-06 14:30:16
  pending_review: 2026-08-06 14:30:16
  approved: 2026-08-06 14:46:53
related_requirement:
related_bug: BUG-0123-openspec-archive-proposal-warning-stdout
related_changes:
  - fix-openspec-archive-multiline-proposal-warning-stdout
openspec_changes:
  - change_id: fix-openspec-archive-multiline-proposal-warning-stdout
    type: fix
    status: archived
iteration: sprint-021
---

# BUG 追踪

```yaml
bug_id: BUG-0124-openspec-archive-multiline-proposal-warning-stdout
status: done
severity: medium
lifecycle_stage: archive
related_requirement:
related_bug: BUG-0123-openspec-archive-proposal-warning-stdout
related_changes:
  - fix-openspec-archive-multiline-proposal-warning-stdout
openspec_changes:
  - change_id: fix-openspec-archive-multiline-proposal-warning-stdout
    type: fix
    status: archived
iteration: sprint-021
```

## 基本信息

| 字段 | 值 |
|---|---|
| 标题 | OpenSpec CLI 多行 proposal warning stdout 块仍出现在归档成功输出中 |
| 严重等级 | medium |
| 来源 | `/capture` |
| 相关需求 |  |
| 相关 Sprint | sprint-021 |
| 相关历史缺陷 | BUG-0123-openspec-archive-proposal-warning-stdout |

## 影响范围

- `scripts/archive-change.sh` 成功路径输出
- `/opsx-archive` 验收体验
- OpenSpec CLI stdout/stderr 多行 warning 过滤策略

## 建议验收或复现要点

- 真实 OpenSpec CLI 多行 proposal warning 块应被整体吸收。
- 未知 stdout/stderr 仍需保留并展示，避免吞掉真实异常或诊断信息。
- 当前单行 warning 回归测试不应失效。

## 来源 Change/Sprint/命令

- 来源 Change：`fix-openspec-archive-proposal-warning-stdout`
- 来源 Sprint：`sprint-021`
- 来源命令：`/opsx-archive`

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-06 15:08:58 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-openspec-archive-multiline-proposal-warning-stdout） |
| 2026-08-06 15:08:49 | /opsx-archive | Change `fix-openspec-archive-multiline-proposal-warning-stdout` 已归档，状态同步完成。 |
| 2026-08-06 15:03:32 | /opsx-apply | Change `fix-openspec-archive-multiline-proposal-warning-stdout` 已完成实现验证，后续归档已闭环。 |
| 2026-08-06 14:56:07 | `/bug-opsx` | 创建 OpenSpec Change `fix-openspec-archive-multiline-proposal-warning-stdout`，后续已归档闭环。 |
| 2026-08-06 14:52:33 | `/sprint-propose sprint-021 --bug BUG-0124` | 纳入 sprint-021 正式范围，后续已交付闭环。 |
| 2026-08-06 14:47:27 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-06 14:46:53 | `/bug-review --approve` | 评审通过，确认需要修复。 |
| 2026-08-06 14:30:16 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，评审前资料完成。 |
| 2026-08-06 14:09:46 | `/bug-generate` | 生成 bug.md，缺陷记录初稿完成。 |
| 2026-08-06 14:02:15 | `/capture` | 记录归档成功输出仍展示 OpenSpec CLI 多行 proposal warning stdout 块的问题。 |

- 2026-08-06 15:08:49 workflow-sync：状态同步为 done（Change archived）
