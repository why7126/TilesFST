---
requirement_id: REQ-0035-ai-usage-snapshot-sprint-close-exps
title: AI usage snapshot 纳入 Sprint close / exps 默认流程 - 用户故事
status: done
created_at: 2026-07-11 23:46:16
updated_at: 2026-07-15 13:14:04
---

# 用户故事

## US-001 Sprint 收尾时检查 AI usage snapshot

作为项目负责人，我希望 Sprint close / archive 默认检查目标 Sprint 是否已有 AI usage snapshot，以便在归档或复盘前知道 AI 使用量事实源是否完整。

验收要点：

- 能识别目标 Sprint 的 snapshot 状态：`present`、`missing`、`stale`、`failed`。
- 能输出 snapshot 路径、生成时间、覆盖范围和使用口径。
- 缺失或异常时必须给出明确 warning 和补救命令。

## US-002 Sprint close 默认生成或刷新 snapshot

作为 AI / Codex Agent，我希望在 Sprint close / archive 阶段按默认步骤生成或刷新 AI usage snapshot，以便 `/sprint-exps` 不再依赖人工临时估算。

验收要点：

- 生成入口复用 REQ-0034 定义的 `data/ai-usage/` 事实源。
- 生成摘要只展示统计和 warning，不展示原始 prompt、session JSONL 或工具输出全文。
- 生成失败时不得继续宣称复盘使用了真实统计。

## US-003 sprint-exps 优先消费真实 snapshot

作为复盘读者，我希望 `/sprint-exps` 优先读取真实 snapshot，并在复盘中清楚标记 `actual` 或 `estimated_fallback`，以便正确理解 AI 使用量分析的可靠性。

验收要点：

- snapshot 可用时，Token 使用分析使用 `actual` 口径。
- snapshot 不可用时，估算 fallback 必须显式标注原因。
- 复盘必须列出补跑 snapshot 的建议动作。

## US-004 防止过期 snapshot 被误用

作为流程维护者，我希望系统能识别过期或覆盖不足的 snapshot，以便 Sprint scope 或 trace 更新后不会误用旧统计。

验收要点：

- 校验 snapshot 是否晚于最近一次 Sprint scope / close / trace 关键更新。
- 校验 snapshot 是否覆盖目标 Sprint 的主要 REQ/BUG/Change。
- 无法判断时降级为 warning，而不是伪装为完整真实统计。

## US-005 保持 AI usage 数据安全

作为安全 / 治理负责人，我希望 snapshot 默认流程继承 REQ-0034 的脱敏规则，以便不把本地 session、绝对路径或敏感上下文写入仓库。

验收要点：

- 不写入原始 prompt、系统指令、developer 指令或技能全文。
- 不写入 `~/.codex/sessions` 原始 JSONL 或本机绝对路径。
- 工具输出只保留统计或短摘要，不保存全文。
