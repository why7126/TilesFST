---
requirement_id: REQ-0034-ai-token-usage-observability
title: AI 命令 Token 使用量观测与 Sprint 复盘接入 - 验收标准
status: archived
created_at: 2026-07-11 17:06:13
updated_at: 2026-07-11 20:10:50
---

# 验收标准

## 事实源与目录

- [ ] AC-001 系统 MUST 使用 `data/ai-usage/` 作为脱敏后的 AI Token 使用量事实源目录。
- [ ] AC-002 原始 `~/.codex/sessions/**/rollout-*.jsonl` MUST 仅作为本地输入，不得提交到仓库。
- [ ] AC-003 Token 使用量事实源 MUST 独立于 REQ/BUG `trace.md`，不得把完整 Token 明细写入 trace 变更记录。
- [ ] AC-004 若 `data/ai-usage/` 存放明细文件，MUST 明确提交边界，例如 README、`.gitignore` 或仅提交聚合快照。

## Session 解析

- [ ] AC-010 解析能力 MUST 能读取 Codex session JSONL 中的 `session_meta`、`turn_context`、用户消息、工具事件和 `token_count` 事件。
- [ ] AC-011 解析能力 MUST 从 `payload.type == token_count` 的事件中读取 `last_token_usage`。
- [ ] AC-012 解析能力 MUST 对未知事件类型保持兼容，不得因单个未知事件中断整个 Sprint 提取。
- [ ] AC-013 JSONL 单行解析失败时 SHOULD 跳过该行并记录 warning，而不是终止全部提取。

## 命令运行边界

- [ ] AC-020 command run MUST 按“用户一轮消息”定义边界。
- [ ] AC-021 一个 command run MUST 聚合该轮用户消息触发后的所有模型调用、工具调用和中间输出，直到下一轮用户消息或会话结束。
- [ ] AC-022 同一轮用户消息显式处理多个 REQ/BUG 时，command run MUST 支持多值 Issue 关联。
- [ ] AC-023 command run MUST 包含 `started_at`、`ended_at`、`command`、`workflow_event`、`requirements[]`、`bugs[]`、`changes[]`、`sprint_id` 和 `attribution_confidence` 或等价字段。

## Token 指标

- [ ] AC-030 每个 command run MUST 统计 `model_call_count`，且口径为该轮内 `token_count` 事件数量。
- [ ] AC-031 每个 command run MUST 聚合 `input_tokens`。
- [ ] AC-032 每个 command run MUST 聚合 `cached_input_tokens`。
- [ ] AC-033 每个 command run MUST 聚合 `output_tokens`。
- [ ] AC-034 每个 command run MUST 聚合 `reasoning_output_tokens`。
- [ ] AC-035 每个 command run MUST 聚合 `total_tokens`。
- [ ] AC-036 Token 聚合 MUST 使用 `last_token_usage` 求和，不得直接把 session 级 `total_token_usage` 当作单命令成本。

## 工具与失败重跑指标

- [ ] AC-040 每个 command run MUST 统计 `tool_call_count`。
- [ ] AC-041 每个 command run MUST 统计 `tool_output_chars`，且不得保存工具输出全文。
- [ ] AC-042 每个 command run MUST 统计 `retry_count` 或等价失败重跑指标。
- [ ] AC-043 若 `retry_count` 为近似统计，事实源 MUST 标记 `retry_count_method` 或等价说明。

## 关联归因

- [ ] AC-050 事实源 MUST 通过独立字段关联 `requirements[]`、`bugs[]`、`changes[]`、`sprint_id` 和 `workflow_event`。
- [ ] AC-051 关联规则 SHOULD 优先使用用户命令文本中的显式 ID。
- [ ] AC-052 关联规则 SHOULD 使用 Workflow Sync 命令参数作为高置信度证据。
- [ ] AC-053 关联规则 MAY 使用 trace 变更记录时间窗口、Sprint scope 反查或人工补录作为辅助证据。
- [ ] AC-054 当归因不唯一或证据不足时，MUST 设置 `attribution_confidence: medium` 或 `low`。

## sprint-exps 接入

- [ ] AC-060 `/sprint-exps` MUST 优先读取 `data/ai-usage/` 中的 Sprint 聚合快照。
- [ ] AC-061 `/sprint-exps` MUST 按命令环节维度展示 Token 使用分析。
- [ ] AC-062 命令环节分析 SHOULD 展示 command run 数、模型调用次数、工具调用次数和失败重跑次数。
- [ ] AC-063 命令环节分析 SHOULD 展示 input/cached/output/reasoning/total tokens。
- [ ] AC-064 命令环节分析 SHOULD 给出高消耗原因和优化建议。
- [ ] AC-065 若没有真实聚合数据，`/sprint-exps` MAY 回退估算模式，但 MUST 明确标注“无精确 token 计量”。

## 脱敏与安全

- [ ] AC-070 事实源和复盘输出 MUST NOT 保存原始 prompt 全文。
- [ ] AC-071 事实源和复盘输出 MUST NOT 保存系统指令、developer 指令、AGENTS 全文或技能全文。
- [ ] AC-072 事实源和复盘输出 MUST NOT 保存 `~/.codex/sessions` 原始 JSONL 内容。
- [ ] AC-073 事实源和复盘输出 MUST NOT 保存本机绝对路径；必须转为仓库相对路径、hash 或 `<local-path-redacted>`。
- [ ] AC-074 事实源和复盘输出 MUST NOT 保存密钥、Cookie、Authorization、真实客户数据或 `.env` 内容。
- [ ] AC-075 无法确认内容是否安全时，MUST 默认不写入原文，只记录统计数字和 warning。

## 可复跑与校验

- [ ] AC-080 同一 session 文件重复提取 SHOULD 幂等，不得重复累计 command run。
- [ ] AC-081 Sprint 聚合快照 SHOULD 能由 command run 明细重新生成。
- [ ] AC-082 提取脚本 SHOULD 输出 warnings，包括无法归因、缺少 token_count、发现本机绝对路径、疑似敏感内容被跳过。
- [ ] AC-083 聚合结果 SHOULD 支持按 total tokens、tool output chars 或 retry count 找出高消耗命令环节。

## 范围约束

- [ ] AC-090 本需求 MUST NOT 修改 Codex Desktop 或模型 API 底层记录方式。
- [ ] AC-091 本需求 MUST NOT 新增 Web、管理端、小程序或店主端 UI。
- [ ] AC-092 本需求 MUST NOT 修改后端业务 API、数据库表结构或 Orval 生成物。
- [ ] AC-093 本需求 MUST NOT 创建 OpenSpec Change；必须待评审通过后再 `/req-opsx`。

## 横切 AC（knowledge-base）

本需求为流程治理、脚本事实源与 Sprint 复盘能力，不涉及 `admin-list`、`admin-form`、`admin-modal`、`media-upload` UI 场景标签，因此无 AC-XCUT。
