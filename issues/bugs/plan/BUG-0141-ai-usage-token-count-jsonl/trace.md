---
bug_id: BUG-0141-ai-usage-token-count-jsonl
status: draft
lifecycle_stage: plan
created_at: 2026-08-25 15:01:59
updated_at: 2026-08-25 15:06:35
severity: medium
related_requirement:
related_bug:
iteration:
openspec_changes: []
lifecycle:
  generated: 2026-08-25 15:06:35
---

# BUG-0141 AI usage extractor 未识别新版 token_count JSONL

```yaml
bug_id: BUG-0141-ai-usage-token-count-jsonl
status: draft
lifecycle_stage: plan
severity: medium
related_requirement:
related_bug:
iteration:
openspec_changes: []
lifecycle:
  generated: 2026-08-25 15:06:35
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
| 2026-08-25 15:01:59 | /bug-capture | 记录 AI usage extractor 未识别新版 `payload.type=token_count` JSONL 导致 sprint-025 snapshot 缺失。 |
