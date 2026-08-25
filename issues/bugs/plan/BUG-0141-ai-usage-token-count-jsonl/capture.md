---
bug_id: BUG-0141-ai-usage-token-count-jsonl
status: captured
created_at: 2026-08-25 15:01:59
updated_at: 2026-08-25 15:01:59
severity_hint: medium
environment: local
related_requirement:
related_bug:
---

# 现象

AI usage extractor 无法从 `~/.codex/sessions` 新版 JSONL 中识别 `payload.type=token_count` 事件，导致 `sprint-025` 的 AI usage snapshot 缺失。

# 复现步骤

1. 准备包含新版 JSONL 事件的本地 Codex session 文件，其中 token 统计事件位于 `payload.type=token_count`。
2. 运行 AI usage 提取或 post-command hook，例如 `python scripts/extract-ai-usage.py --post-command-hook --workflow-event <event> --json`。
3. 检查生成结果中的 Sprint snapshot。

# 期望 vs 实际

- 期望：提取器能够识别新版 JSONL 的 `payload.type=token_count`，并为关联的 `sprint-025` 生成或更新 AI usage snapshot。
- 实际：提取器未识别该事件格式，导致 `sprint-025` snapshot 缺失。

# 附件

暂无。涉及本机 `~/.codex/sessions` 原始 JSONL，仅用于本地复现，不复制入仓库。
