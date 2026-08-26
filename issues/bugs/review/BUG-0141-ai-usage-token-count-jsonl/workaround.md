---
bug_id: BUG-0141-ai-usage-token-count-jsonl
created_at: 2026-08-25 15:13:14
updated_at: 2026-08-25 15:13:14
---

# 临时规避

## 可用规避

在修复提取器前，如必须生成某个 Sprint 的 AI usage snapshot，可采用以下临时方式：

1. 使用包含旧式字符串用户消息的 session JSONL 作为输入。
2. 或为历史 session 提供 `--manual-map`，手动映射 turn 到目标 BUG、REQ、Change 或 Sprint。
3. 对缺失 snapshot 的复盘输出保留 `estimated_fallback`，不得把全 0 token 统计当作真实成本矩阵。

## 不建议规避

- 不复制或提交 `~/.codex/sessions` 原始 JSONL。
- 不手工改写 `data/ai-usage/sprints/<sprint-id>.json` 为 `actual`。
- 不用虚构 token 数字填充 Sprint 复盘。

## 后续修复后处理

修复完成后，使用真实本地 session 重新运行：

```bash
python scripts/extract-ai-usage.py --session-jsonl <local-session.jsonl> --sprint sprint-025
python scripts/extract-ai-usage.py --check-snapshot --sprint sprint-025 --json
```

确认 snapshot 为 `present` / `actual` 且关键 token totals 非零后，再允许 `/sprint-exps` 输出真实成本矩阵。
