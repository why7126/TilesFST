---
bug_id: BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot
status: done
severity: medium
priority: P2
created_at: 2026-08-04 08:18:50
updated_at: 2026-08-04 09:17:11
lifecycle:
  captured: 2026-08-04 08:18:50
  generated: 2026-08-04 08:20:35
  completed: 2026-08-04 08:22:00
  reviewed: 2026-08-04 08:24:19
  approved: 2026-08-04 08:24:19
  sprint_joined: 2026-08-04 08:35:57
  done: 2026-08-04 09:16:43
iteration: sprint-019
openspec_changes:
  - change_id: fix-fact-sheet-ai-usage-fresh-gate-snapshot
    type: fix
    status: archived
related_requirement: null
related_bug: null
lifecycle_stage: archive
---

# BUG-0113 Fact Sheet AI usage fresh gate 与已刷新 snapshot 状态不一致

```yaml
bug_id: BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot
status: done
severity: medium
priority: P2
created_at: 2026-08-04 08:18:50
updated_at: 2026-08-04 09:17:11
lifecycle:
  captured: 2026-08-04 08:18:50
  generated: 2026-08-04 08:20:35
  completed: 2026-08-04 08:22:00
  reviewed: 2026-08-04 08:24:19
  approved: 2026-08-04 08:24:19
  sprint_joined: 2026-08-04 08:35:57
  done: 2026-08-04 09:16:43
iteration: sprint-019
openspec_changes:
  - change_id: fix-fact-sheet-ai-usage-fresh-gate-snapshot
    type: fix
    status: archived
related_requirement: null
related_bug: null
lifecycle_stage: archive
```

## 摘要

Fact Sheet AI usage fresh gate 与已刷新 snapshot 状态不一致，疑似 stale 判定或 snapshot 状态到 usage mode 的映射存在偏差，可能导致已刷新证据仍被误判为过期或不可用。

## 影响范围

- Fact Sheet AI usage 证据生成与校验。
- snapshot freshness gate。
- usage mode 映射与报告展示。
- 依赖 AI usage snapshot 的发布、验收和 workflow 追踪判断。

## 完善状态

- root-cause.md：已补齐，根因状态为待代码定位确认。
- workaround.md：已补齐，提供人工复核与重新刷新规避。
- acceptance.md：已补齐，验收状态为 passed。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-04 09:17:09 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-fact-sheet-ai-usage-fresh-gate-snapshot） |
| 2026-08-04 09:16:43 | /opsx-archive | Change `fix-fact-sheet-ai-usage-fresh-gate-snapshot` 已归档，状态同步完成。 |
| 2026-08-04 08:51:35 | /opsx-apply | Change `fix-fact-sheet-ai-usage-fresh-gate-snapshot` apply 完成，已 archive。 |
| 2026-08-04 08:42:47 | /bug-opsx BUG-0113 | 创建 `fix-fact-sheet-ai-usage-fresh-gate-snapshot`，关联状态 archived。 |
| 2026-08-04 08:35:57 | /sprint-propose sprint-019 | 纳入 sprint-019 正式范围，状态已闭环。 |
| 2026-08-04 08:24:44 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-04 08:24:19 | /bug-review --approve | 评审通过，状态推进为 approved，准备迁入 review 阶段目录。 |
| 2026-08-04 08:22:00 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态曾推进为 review_ready，现已闭环。 |
| 2026-08-04 08:20:35 | /bug-generate | 生成 bug.md，完成初稿生成，现已闭环。 |
| 2026-08-04 08:18:50 | /bug-capture | 记录 Fact Sheet AI usage fresh gate 与已刷新 snapshot 状态不一致的缺陷。 |

- 2026-08-04 09:16:19 workflow-sync：状态同步为 done（Change archived）
