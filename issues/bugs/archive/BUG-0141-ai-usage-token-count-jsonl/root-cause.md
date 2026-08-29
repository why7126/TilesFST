---
bug_id: BUG-0141-ai-usage-token-count-jsonl
root_cause_status: confirmed
created_at: 2026-08-25 15:13:14
updated_at: 2026-08-25 15:13:14
category: code
---

# 根因分析

## 根因状态

`confirmed`

## 直接原因

`scripts/ai_usage.py` 的 `user_text()` 只能从字符串型 `text`、`content`、`message`、`cmd`、`command` 字段提取用户输入。新版 Codex session JSONL 的用户消息为 `payload.type=message`、`payload.role=user`，且 `payload.content` 是包含文本片段的列表，不是字符串。

因此解析器读到新版用户消息时无法创建 `CommandRun`。后续 `payload.type=token_count` 事件虽然能被 `event_type()` / `is_token_event()` 识别，但因为 `current is None`，在 `parse_session_jsonl()` 中被跳过，无法累计到 command run 与 Sprint snapshot。

## 根本原因

AI usage extractor 的 session JSONL 兼容测试覆盖停留在旧格式和中间格式：

- 旧格式：`type=user_message` 且用户文本位于顶层 `text`。
- token 中间格式：`payload.type=token_count` 且 token 用量位于 `payload.info.last_token_usage`。

缺少新版用户消息格式的最小回归夹具：`payload.type=message`、`payload.role=user`、`payload.content=[{"type":"text","text":"..."}]`。这使得 token 事件识别看似可用，但用户 turn 边界无法建立，最终 snapshot 仍然缺失。

## 触发条件

- session JSONL 使用新版 `message` 事件结构承载用户输入。
- 用户文本位于 `payload.content` 列表中的文本片段。
- token 统计位于同一 turn 后续 `payload.type=token_count` 事件。
- 提取器未显式传入 manual map，依赖自动从用户消息推导 command run、workflow event、BUG/REQ/Change/Sprint 归因。

## 证据链

| 证据类型 | 证据入口 | 摘要 |
|---|---|---|
| 代码定位 | `scripts/ai_usage.py` `safe_text()` / `user_text()` / `parse_session_jsonl()` | `safe_text()` 只返回字符串字段；`payload.content` 为列表时返回空字符串；`parse_session_jsonl()` 在没有 current command run 时跳过后续事件。 |
| 测试覆盖定位 | `tests/test_ai_usage.py` `test_parse_token_count_groups_by_user_turn_and_warns_on_malformed_rows`、`test_parse_token_count_supports_payload_info_last_token_usage` | 已覆盖 `payload.type=token_count` 与 `payload.info.last_token_usage`，但用户消息仍是字符串型输入，未覆盖新版 `payload.content` 列表。 |
| 脱敏本地复现 | 只读统计本机新版 session 的事件形态 | session 内存在 `payload.type=token_count` 事件，token 用量位于 `payload.info.last_token_usage`；用户消息为 `payload.type=message`、`payload.role=user`、`payload.content` 列表。 |
| 行为复现 | 调用 `parse_session_jsonl()` 解析同一新版 session | 返回 `records=0`、`warnings=[]`，说明 token 事件存在但没有 command run 可归属。 |
| Snapshot 证据 | `python scripts/extract-ai-usage.py --check-snapshot --sprint sprint-025 --json` | `snapshot_status=failed`、`usage_mode=estimated_fallback`、`required-metrics-empty`、token totals 与 `model_call_count` 均为 0。 |

## 验证方式

修复前：

1. 构造脱敏 JSONL：用户消息使用 `payload.type=message`、`payload.role=user`、`payload.content` 文本片段列表。
2. 在后续行加入 `payload.type=token_count`，token 用量放在 `payload.info.last_token_usage`。
3. 调用 `parse_session_jsonl()`，应复现 `records=0` 或 `token-count-missing`。

修复后：

1. 同一最小 JSONL 应解析出 1 条 command run。
2. command run 应正确识别 workflow event、BUG/REQ/Change/Sprint 归因。
3. `model_call_count` 与 token totals 应来自 `payload.info.last_token_usage`。
4. 对 `sprint-025` 使用真实本地 session 重新生成 snapshot 后，snapshot 不应再因 `required-metrics-empty` 失败。

## 人工补证

当前根因已确认。若评审前需要补充非本机证据，可由测试人员在不提交原始 session 的前提下执行：

1. 从本机 Codex session 中抽取字段形态统计，只输出事件类型计数、字段名集合和 token 用量字段位置。
2. 运行 `parse_session_jsonl()` 的脱敏摘要，记录 records 数量、model_call_count、total_tokens，不输出用户原文、工具输出或本机绝对路径。
3. 将摘要贴入后续 OpenSpec Change 的验收证据。
