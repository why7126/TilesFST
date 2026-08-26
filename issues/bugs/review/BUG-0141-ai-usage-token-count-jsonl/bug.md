---
bug_id: BUG-0141-ai-usage-token-count-jsonl
title: AI usage extractor 未识别新版 token_count JSONL 导致 Sprint snapshot 缺失
severity: medium
status: in_sprint
owner:
discovered_at: 2026-08-25 15:01:59
environment: local
related_requirement:
related_change: fix-ai-usage-message-content-token-count
updated_at: 2026-08-25 15:36:55
created_at: 2026-08-25 15:01:59
---

# 现象

AI usage extractor 处理 `~/.codex/sessions` 新版 JSONL 时，无法为包含 `payload.type=token_count` 的 session 生成有效 command run，导致 `sprint-025` AI usage snapshot 缺少真实 token 统计。

# 复现

1. 使用包含新版 Codex session JSONL 结构的本地文件，用户消息形态为 `payload.type=message`、`payload.role=user`、`payload.content` 为列表。
2. 同一 session 内包含 `payload.type=token_count` 事件，token 用量位于 `payload.info.last_token_usage`。
3. 运行 AI usage 提取或 post-command hook，例如：

```bash
python scripts/extract-ai-usage.py --post-command-hook --workflow-event <event> --sprint sprint-025 --json
```

4. 检查 `data/ai-usage/sprints/sprint-025.json` 或 `--check-snapshot --sprint sprint-025` 输出。

# 期望结果

- 提取器能够识别新版用户消息结构，并以该用户消息创建 command run。
- 后续 `payload.type=token_count` 事件应归属到对应 command run。
- `sprint-025` snapshot 应在存在真实 token 事件时生成 `actual` usage，并包含非零 `model_call_count` 与 token totals。

# 实际结果

- 当前解析新版 session 时 command run 数为 0。
- `payload.type=token_count` 事件虽然可被事件类型识别，但因为没有当前 command run，无法累计 token 用量。
- `sprint-025` snapshot 当前表现为 `failed` / `estimated_fallback`，并出现 `required-metrics-empty`。

# 影响范围

- 影响 `scripts/extract-ai-usage.py`、`scripts/ai_usage.py` 的 session JSONL 解析与 post-command hook。
- 影响 Sprint AI usage snapshot、Fact Sheet 与 `/sprint-exps` 中真实 token 成本矩阵。
- 不影响业务 API、数据库、Web、小程序、管理端运行时功能。
- 原始 `~/.codex/sessions` 文件为本机私有输入，不得复制入仓库；回归测试应使用脱敏最小 JSONL 夹具。

# 严重等级说明

严重等级为 `medium`。该缺陷不会阻断业务功能，但会让研发治理链路中的 AI usage 事实源降级为 `estimated_fallback` 或 failed snapshot，影响 Sprint 复盘和成本统计可信度。

# OpenSpec 关联

```yaml
openspec_changes:
  - change_id: fix-ai-usage-message-content-token-count
    type: fix
    status: applied
```
