---
requirement_id: REQ-0037-auto-token-fact-source-for-workflow-commands
title: 工作流命令自动构建 AI Token 事实源 - 验收标准
status: done
created_at: 2026-07-12 09:56:48
updated_at: 2026-07-15 13:14:09
---

# 验收标准

## 自动触发

- [ ] AC-001 每个 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 命令技能 MUST 在主命令成功且 Workflow Sync 成功后触发统一 AI usage fact source hook，或明确引用同一后置流程。
- [ ] AC-002 当主命令失败或 Workflow Sync 失败时，usage hook MAY 跳过，但最终输出 MUST 说明本次未构建 Token 事实源。
- [ ] AC-003 usage hook 成功路径 MUST 输出短摘要，包含 `status`、`usage_mode`、command run 数、snapshot 路径或 skipped 原因、warning 数量。
- [ ] AC-004 自动构建失败默认 MUST NOT 阻断主工作流命令；除非后续设计明确 Sprint close 等收尾命令需要强门禁。

## 统一 hook

- [ ] AC-010 系统 MUST 提供统一脚本、函数或等价封装，集中处理 session 输入、提取、归因、脱敏、写入和摘要输出。
- [ ] AC-011 命令技能 MUST NOT 复制大段 `extract-ai-usage` 解析逻辑；只允许声明调用时机、关键参数和输出要求。
- [ ] AC-012 统一 hook MUST 支持 workflow event、REQ ID、BUG ID、Change ID、Sprint ID、session 输入和 manual map 等参数或等价能力。
- [ ] AC-013 统一 hook MUST 支持 check/dry-run 或 recommended-action 模式，以便在无法写入事实源时输出可执行下一步。

## command run 明细

- [ ] AC-020 当本地 session 输入可用且解析成功时，系统 MUST 生成或刷新 `data/ai-usage/command-runs/` 脱敏 command run 明细。
- [ ] AC-021 command run MUST 通过 `requirements[]`、`bugs[]`、`changes[]`、`sprint_id`、`workflow_event` 或等价字段进行归因。
- [ ] AC-022 尚未纳入 Sprint 的 REQ/BUG 命令 MUST NOT 伪造 Sprint snapshot；应至少写 command run 明细或输出无法写入的原因。
- [ ] AC-023 重复执行同一 session 提取 SHOULD 通过 session hash、turn hash 或 command run id 避免重复累计。

## Sprint snapshot

- [ ] AC-030 当命令可明确关联到 `sprint-xxx` 时，系统 SHOULD 生成或刷新 `data/ai-usage/sprints/<sprint-id>.json`。
- [ ] AC-031 Sprint snapshot MUST 包含 `sprint_id`、`generated_at`、coverage、totals、warnings 和 usage mode 所需字段。
- [ ] AC-032 snapshot 覆盖不足、过期、指标为空或解析失败时 MUST NOT 标记为完整 `actual`。
- [ ] AC-033 `/sprint-exps` 或 Fact Sheet 消费 snapshot 时，若不是 `actual`，MUST 显式输出 `estimated_fallback`、reason 和 recommended action。

## 脱敏与安全

- [ ] AC-040 自动构建 MUST NOT 持久化原始 prompt、系统指令、developer 指令、AGENTS 全文或技能全文。
- [ ] AC-041 自动构建 MUST NOT 持久化原始 `~/.codex/sessions` JSONL 内容、本机绝对路径或工具输出正文。
- [ ] AC-042 自动构建 MUST NOT 持久化 `.env` 内容、密钥、Cookie、Authorization、Token、真实客户数据或真实联系方式。
- [ ] AC-043 当内容安全性不确定时，系统 MUST 默认不写入文本，仅保留数字指标、hash、时间范围、工作流 ID 或 redaction warning。
- [ ] AC-044 命令输出 MUST NOT 打印完整 session、prompt、工具日志、OpenAPI/Orval 大 diff 或测试日志全文。

## 失败降级

- [ ] AC-050 本地 session 不存在、不可访问或无法定位时，hook MUST 输出 `usage_mode: unavailable` 或等价状态，并给出 recommended action。
- [ ] AC-051 JSONL 解析失败、缺少 `token_count`、无法归因或敏感内容被跳过时，hook MUST 输出 warning。
- [ ] AC-052 失败降级输出 MUST 包含 reason，且不得声称本次已使用真实 Token 统计。
- [ ] AC-053 无 Sprint 归属时，hook 摘要 MUST 明确 `sprint_snapshot: skipped` 或等价说明。

## 技能与规则同步

- [ ] AC-060 实现 MUST 更新相关命令技能或共享工作流规则，使 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 的后置 Token 事实源构建行为有统一说明。
- [ ] AC-061 实现 SHOULD 更新 `data/ai-usage/README.md`，说明自动构建触发场景、提交边界和 failure fallback。
- [ ] AC-062 如新增环境变量、本地配置或 hook 脚本参数，MUST 同步文档说明用途、默认值和安全边界。
- [ ] AC-063 实现 MUST 遵守 `rules/agent-context-budget.md`，成功路径只输出摘要，失败路径只展开必要诊断。

## 测试与校验

- [ ] AC-070 MUST 增加或更新测试覆盖：成功生成 command run、无 Sprint 归属、Sprint snapshot 刷新、session 缺失、snapshot stale、coverage missing、敏感内容跳过。
- [ ] AC-071 MUST 增加或更新脚本级测试，验证重复提取不会重复累计同一 command run。
- [ ] AC-072 MUST 验证命令技能或共享规则中没有复制原始 session、prompt、工具输出正文的要求。
- [ ] AC-073 MUST 运行 AI usage 相关测试和必要的 workflow sync / context budget 校验。

## 横切 AC（knowledge-base）

本 REQ 为 Agent 工作流 / 脚本治理能力，不涉及管理端列表页、表单页、弹窗或媒体上传 UI 场景。

- [ ] AC-XCUT-N/A 无 UI 横切 AC；knowledge-base gate 为 N/A。
