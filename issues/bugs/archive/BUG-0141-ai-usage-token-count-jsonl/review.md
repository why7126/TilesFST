---
bug_id: BUG-0141-ai-usage-token-count-jsonl
review_result: approved
reviewed_at: 2026-08-25 15:19:02
created_at: 2026-08-25 15:19:02
updated_at: 2026-08-25 15:19:02
reviewer:
---

# 评审结论

确认修复。

## 评审清单

- [x] `root_cause_status: confirmed` 且证据链可定位。
- [x] 严重等级 `medium` 合理：不阻断业务运行，但影响 Sprint AI usage 事实源与复盘成本矩阵可信度。
- [x] 回归验收明确：覆盖新版 `payload.content` 列表用户消息、`payload.type=token_count` 归属、Sprint snapshot 和隐私边界。
- [x] 不需要 hotfix：属于研发治理统计链路缺陷，可走常规 Sprint 修复。

## 依据

- `root-cause.md` 已确认根因：新版用户消息为 `payload.type=message`、`payload.role=user`、`payload.content` 列表，当前 `user_text()` 无法抽取文本，导致 `CommandRun` 不创建，后续 token_count 无法归属。
- 根因证据门禁已通过：`python scripts/validate-root-cause-evidence.py --bug BUG-0141-ai-usage-token-count-jsonl --require-confirmed`。

## 后续建议

先纳入 Sprint，再创建修复 Change。修复时应补充 `tests/test_ai_usage.py` 的脱敏最小 JSONL 夹具，并验证 `sprint-025` snapshot 可恢复为 `actual`。
