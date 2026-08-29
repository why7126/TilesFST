---
bug_id: BUG-0141-ai-usage-token-count-jsonl
status: done
lifecycle_stage: archive
created_at: 2026-08-25 15:01:59
updated_at: 2026-08-28 16:15:59
severity: medium
root_cause_status: confirmed
related_requirement:
related_bug:
iteration: sprint-026
openspec_changes:
  - change_id: fix-ai-usage-message-content-token-count
    type: fix
    status: archived
lifecycle:
  generated: 2026-08-25 15:06:35
  completed: 2026-08-25 15:13:14
  reviewed: 2026-08-25 15:19:02
related_change: fix-ai-usage-message-content-token-count
---

# BUG-0141 AI usage extractor 未识别新版 token_count JSONL

```yaml
bug_id: BUG-0141-ai-usage-token-count-jsonl
status: done
lifecycle_stage: archive
severity: medium
root_cause_status: confirmed
related_requirement:
related_bug:
iteration: sprint-026
openspec_changes:
  - change_id: fix-ai-usage-message-content-token-count
    type: fix
    status: archived
lifecycle:
  generated: 2026-08-25 15:06:35
  completed: 2026-08-25 15:13:14
  reviewed: 2026-08-25 15:19:02
related_change: fix-ai-usage-message-content-token-count
```

## 摘要

AI usage extractor 对新版 Codex session JSONL 事件兼容不足，未识别 `payload.type=token_count`，导致 `sprint-025` AI usage snapshot 缺失。

## 影响范围

- 影响 AI usage command run 与 Sprint snapshot 的自动提取链路。
- 已知影响 `sprint-025` snapshot 完整性。
- 不影响业务 API、数据库、Web、小程序或管理端运行时功能。

## 复现与验收要点

- 使用包含 `payload.type=token_count` 的新版 `~/.codex/sessions` JSONL 作为输入时，提取器应能读取 token 统计。
- post-command hook 应在存在 Sprint 上下文时生成或更新对应 Sprint snapshot。
- 原始 session JSONL 不得复制入仓库，测试应使用脱敏最小夹具。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-27 23:13:49 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-ai-usage-message-content-token-count） |
| 2026-08-27 23:13:40 | /opsx-archive | Change `fix-ai-usage-message-content-token-count` 已归档，状态同步完成。 |
| 2026-08-25 18:21:51 | /opsx-modify | Change `fix-ai-usage-message-content-token-count` 验收返修已同步，待复验或 archive。 |
| 2026-08-25 15:36:55 | /opsx-apply | Change `fix-ai-usage-message-content-token-count` apply 完成，后续已归档。 |
| 2026-08-25 15:19:30 | lifecycle-stage-migrate | plan → review（/bug-review） |
| 2026-08-25 15:01:59 | /bug-capture | 记录 AI usage extractor 未识别新版 `payload.type=token_count` JSONL 导致 sprint-025 snapshot 缺失。 |
| 2026-08-25 15:06:35 | /bug-generate | 生成 `bug.md`，状态推进为 draft。 |
| 2026-08-25 15:13:14 | /bug-complete | 补齐 root-cause、workaround、acceptance，根因状态 confirmed，状态推进为 pending_review。 |
| 2026-08-25 15:19:02 | /bug-review | 根因 confirmed 门禁通过，评审结论为 approved。 |
| 2026-08-25 15:22:34 | /sprint-propose | 纳入 sprint-026，后续已创建并归档修复 Change。 |

- 2026-08-27 23:13:40 workflow-sync：状态同步为 done（Change archived）
