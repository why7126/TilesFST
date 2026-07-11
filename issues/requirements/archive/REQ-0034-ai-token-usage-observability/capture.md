---
req_id: REQ-0034-ai-token-usage-observability
status: archived
created_at: 2026-07-11 16:50:57
updated_at: 2026-07-11 20:10:50
recorded_by: product
source: /opsx-explore
priority_hint: P1
parent_requirement:
---

# 一句话

建立 AI 命令 Token 使用量观测事实源，将每个 REQ/BUG/Sprint 工作流环节的模型调用次数与 token 消耗可追溯地汇总到 Sprint 复盘。

# 原始描述

探索是否要新增规范，将每一个命令（本质是一轮对话）产生的 Token 消耗记录下来，以便于进行分析。比如在 `trace.md` 文档里面有一个变更记录，新增对应的字段（调用次数、Token 量、输入 Token 量、输出 Token 量、缓存 Token 量等），字段以及对应的 Token 消耗量数据应该是记录在 `~/.codex/sessions` 目录下。不一定要记录在 `trace.md` 文档里面，也可以记录在其他文档或新增文档下。但需要能够知道 BUG/REQ 在每个环节的消耗情况，`sprint-exps` 分析的时候需要用到。

# 待澄清

- [ ] Token 使用量事实源落在 `data/ai-usage/`、`docs/standards/` 还是其他目录；原始 `~/.codex/sessions` 是否仅作为本地输入，不纳入仓库。
- [ ] 是否在 REQ/BUG `trace.md` 中仅写轻量 `usage_ref`，还是完全通过独立事实表按时间、命令、Issue ID 关联。
- [ ] 命令运行边界如何定义：按用户一轮消息、`turn_id`、技能命令、Workflow Sync event，还是组合规则。
- [ ] 需要纳入哪些指标：模型调用次数、input/cached/output/reasoning/total tokens、工具调用次数、工具输出字符数、失败重跑次数。
- [ ] `sprint-exps` 的输出需要展示到 Issue 维度、命令环节维度、Change 维度还是只展示 Sprint 聚合。
- [ ] 是否需要脱敏策略，避免复盘文档泄露 `~/.codex/sessions` 中的原始 prompt、系统指令或本地绝对路径。

# 探索结论

- `~/.codex/sessions/**/rollout-*.jsonl` 中存在 `token_count` 事件，可读取 `last_token_usage` 与 `total_token_usage`。
- 可用字段包含 `input_tokens`、`cached_input_tokens`、`output_tokens`、`reasoning_output_tokens`、`total_tokens`。
- 建议采用后处理提取方式，生成独立 Token Usage Fact Sheet，再由 `sprint-exps` 引用；不建议把完整 token 明细直接写入 `trace.md`。
- 初步建议新增 Change：`add-ai-token-usage-observability`，范围包括规范、提取脚本、Sprint Fact Sheet 增强与 `sprint-exps` 接入。
