---
requirement_id: REQ-0034-ai-token-usage-observability
title: AI 命令 Token 使用量观测与 Sprint 复盘接入 - 用户故事
status: archived
created_at: 2026-07-11 17:06:13
updated_at: 2026-07-11 20:10:50
---

# 用户故事

## US-001 项目负责人查看 REQ/BUG 流程成本

作为项目负责人，我希望在 Sprint 复盘时看到各命令环节的 Token 使用统计，以便判断一个 REQ/BUG 从 capture 到 archive 的 AI 成本分布。

验收要点：

- 复盘能按命令环节展示 Token 使用量，而不是只展示 Sprint 总量。
- 统计能关联到 REQ/BUG/Sprint。
- 无真实统计时必须明确标注估算或无数据。

## US-002 开发负责人定位高消耗命令

作为开发负责人，我希望看到每个命令环节的模型调用次数、工具调用次数、工具输出字符数和失败重跑次数，以便优化脚本摘要、读取边界和失败处理。

验收要点：

- command run 记录包含模型调用和工具调用指标。
- 高消耗命令可以按 total tokens 或 tool output chars 排序分析。
- 失败重跑采用可解释口径，并记录统计方法。

## US-003 AI Agent 使用事实表完成 sprint-exps

作为 AI Agent，我希望 `/sprint-exps` 优先读取 `data/ai-usage/` 中的聚合快照，以便基于真实统计生成 Token 使用分析，减少对原始 session 和长文档的重复读取。

验收要点：

- `sprint-exps` 能读取 Sprint 聚合快照。
- 聚合快照缺失时可以回退到估算模式。
- 复盘输出按命令环节展示，而不是复制原始会话内容。

## US-004 治理负责人控制敏感信息泄露

作为治理负责人，我希望 Token 使用量事实源只保存脱敏统计和低风险元数据，以便避免 `~/.codex/sessions` 中的原始 prompt、系统指令、本机路径或工具输出进入仓库和长期文档。

验收要点：

- 事实源不保存原始 prompt、系统指令和工具输出全文。
- 本机绝对路径必须被脱敏、hash 或转为仓库相对路径。
- 发现疑似敏感内容时默认跳过原文，只保留统计数字和 warning。

## US-005 复盘读者理解优化建议来源

作为复盘读者，我希望看到 Token 消耗数据对应的证据口径和归因置信度，以便理解优化建议是来自真实统计、低置信度推断还是估算。

验收要点：

- command run 记录包含 `attribution_confidence`。
- 多 Issue 归因时可以表达多个 REQ/BUG。
- Sprint 复盘能区分真实统计、估算和缺失数据。
