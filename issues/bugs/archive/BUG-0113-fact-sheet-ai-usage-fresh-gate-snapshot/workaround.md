---
bug_id: BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot
created_at: 2026-08-04 08:22:00
updated_at: 2026-08-04 08:22:00
workaround_status: available
---

# Workaround

## 临时规避

在修复前，遇到 Fact Sheet AI usage fresh gate 与 snapshot 刷新状态不一致时，先不要直接采信 gate 的 stale 结论，应人工复核 snapshot 本身：

1. 确认 snapshot 文件或输出记录确实由当前命令刷新生成。
2. 核对 snapshot 内部时间戳、状态字段和 usage mode。
3. 如 gate 仍误判 stale，重新执行生成 snapshot 的命令或 AI usage hook，再重新运行 gate。
4. 在发布、验收或 Fact Sheet 输出中记录该次人工复核结论和命令输出摘要。

## 限制

- 该规避只能降低误拦截风险，不能修复状态契约不一致。
- 人工复核不应替代后续自动化回归测试。
- 若 snapshot 确实缺失、过期或 mode 为 unavailable，仍应按 gate 阻断处理。

## 是否需要数据修复

暂不确认需要数据修复。若后续定位发现历史 snapshot 已被错误持久化为 stale 或 unavailable，需要在修复 Change 中补充一次性审计或重建步骤。
