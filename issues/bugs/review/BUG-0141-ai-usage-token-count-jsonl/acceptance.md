---
bug_id: BUG-0141-ai-usage-token-count-jsonl
acceptance_status: pending
created_at: 2026-08-25 15:13:14
updated_at: 2026-08-25 18:21:51
---

# 验收标准

## AC-001 新版用户消息结构可建立 command run

给定脱敏 JSONL 中存在：

- `payload.type=message`
- `payload.role=user`
- `payload.content` 为文本片段列表

当调用 `parse_session_jsonl()` 时，应生成对应 command run，并正确解析用户命令中的 workflow event、BUG/REQ/Change/Sprint 归因。

## AC-002 token_count 事件可归属到新版 command run

给定同一 turn 后续存在 `payload.type=token_count`，且 token 用量位于 `payload.info.last_token_usage`，当调用 `parse_session_jsonl()` 时：

- `model_call_count` 应大于 0。
- `input_tokens`、`output_tokens`、`cached_input_tokens`、`reasoning_output_tokens`、`total_tokens` 应按 fixture 累计。
- 不应产生 `token-count-missing`。

## AC-003 Sprint snapshot 不再因 required metrics 为空失败

给定新版 JSONL 中包含目标 Sprint 或通过参数传入 `--sprint sprint-025`，当运行：

```bash
python scripts/extract-ai-usage.py --session-jsonl <local-session.jsonl> --sprint sprint-025
python scripts/extract-ai-usage.py --check-snapshot --sprint sprint-025 --json
```

则 snapshot 应满足：

- `snapshot_status` 为 `present`。
- `usage_mode` 为 `actual`。
- `fresh_gate.status` 为 `pass`。
- `model_call_count` 与 token totals 非零。

## AC-004 安全与隐私边界

修复和测试不得提交原始 `~/.codex/sessions` JSONL，不得持久化 prompt 原文、系统/开发者指令、工具输出正文、本机绝对路径、Authorization header、Cookie、`.env` 内容或密钥。测试必须使用脱敏最小 JSONL 夹具。

## AC-005 Sprint AI Usage 矩阵未观测阶段展示

给定 Sprint AI Usage snapshot 中部分 workflow 列没有任何 command run 覆盖，当运行：

```bash
python scripts/generate-sprint-fact-sheet.py --sprint <sprint-id> --ai-usage-markdown
```

则 Markdown 矩阵应满足：

- 未观测 workflow 阶段展示为 `-`。
- 已观测 workflow 列中的真实零消耗继续展示为数字 `0`。
- 矩阵口径说明 `-` 不等价于真实 `0`。

## 回归测试建议

- 在 `tests/test_ai_usage.py` 增加新版 message content 列表格式的解析测试。
- 在 `tests/test_generate_sprint_fact_sheet.py` 增加未观测 workflow 阶段展示为 `-` 的渲染测试。
- 聚焦运行 `python -m pytest tests/test_ai_usage.py`。

## 验收结果回填

```yaml
acceptance_status: pending
accepted_at: null
accepted_by: null
source_change: fix-ai-usage-message-content-token-count
source_sprint: sprint-026
evidence: []
failed_items: []
source_event: opsx.modify
notes: 待验收；由 opsx.apply 标记，后续 archive 时回填结论。
```

