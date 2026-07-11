---
requirement_id: REQ-0034-ai-token-usage-observability
title: AI 命令 Token 使用量观测与 Sprint 复盘接入
terminal: multi
version: v1
status: archived
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-07-11 16:59:45
updated_at: 2026-07-11 20:10:50
---

# REQ-0034 AI 命令 Token 使用量观测与 Sprint 复盘接入

## 1. 需求背景

项目已经通过 OpenSpec、REQ/BUG、Sprint 和 Workflow Sync 建立了较完整的研发流程事实源，但 AI 执行各类命令时的模型 Token 消耗仍主要依赖人工感知或复盘估算。`/sprint-exps` 已要求输出“模型 Token 使用分析”，但当前缺少可追溯的真实用量数据，难以回答以下问题：

- 一个 REQ 从 capture 到 opsx/apply/archive 各环节分别消耗多少 Token；
- 哪类命令最容易产生高输入、高输出、缓存命中或失败重跑；
- 哪些读取策略、脚本摘要或 Workflow Sync 输出会显著影响上下文成本；
- Sprint 复盘中应优先优化哪个命令环节，而不是只给出笼统建议。

Codex 本地会话文件 `~/.codex/sessions/**/rollout-*.jsonl` 中存在 `token_count` 事件，包含 `last_token_usage` 与 `total_token_usage`。本需求用于建立独立的 AI Token 使用量事实源，将原始本地会话数据转换为脱敏、可聚合、可被 `/sprint-exps` 使用的命令环节统计。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 产品 / 项目负责人 | 知道每个 REQ/BUG 在各流程环节的 AI 成本，辅助 Sprint 容量和流程优化判断。 |
| 开发负责人 | 识别高消耗命令、失败重跑和大输出来源，改进脚本、规则和技能读取边界。 |
| AI / Codex Agent | 在 `sprint-exps` 时读取结构化 Token Fact Sheet，减少人工估算和重复读取。 |
| 复盘读者 | 在不暴露原始会话内容的前提下，理解本 Sprint 的 AI Token 使用模式和优化项。 |
| 安全 / 治理负责人 | 确保 `~/.codex/sessions` 的原始 prompt、系统指令、本地绝对路径不会进入长期文档。 |

## 3. 需求目标

- 建立 `data/ai-usage/` 作为 AI 命令 Token 使用量事实源目录。
- 原始 `~/.codex/sessions` 仅作为本机输入，不纳入仓库、不直接进入复盘文档。
- 使用独立事实表按时间、命令、Issue ID 关联 REQ/BUG/Sprint，不把完整 Token 明细写入 `trace.md`。
- 以“用户一轮消息”定义命令运行边界，聚合该轮内模型调用、工具调用和失败重跑。
- `/sprint-exps` 必须能按命令环节维度展示 Token 使用分析。
- 输出必须脱敏，避免泄露原始 prompt、系统指令、`~/.codex/sessions` 原文和本机绝对路径。

## 4. 范围

### 4.1 包含

| 范围 | 说明 |
|---|---|
| Token 使用量事实源 | 在 `data/ai-usage/` 下沉淀脱敏后的 command run 记录和 Sprint 聚合快照。 |
| 本地会话解析 | 从 `~/.codex/sessions/**/rollout-*.jsonl` 读取 `token_count`、`turn_context`、用户消息和工具事件等必要元数据。 |
| 命令边界识别 | 按用户一轮消息聚合为一个 command run。 |
| 指标聚合 | 聚合模型调用次数、input/cached/output/reasoning/total tokens、工具调用次数、工具输出字符数、失败重跑次数。 |
| Issue / Sprint 关联 | 通过命令文本、REQ/BUG ID、Change ID、Sprint ID、Workflow Sync event 或时间窗口建立关联。 |
| sprint-exps 接入 | Sprint 复盘按命令环节维度展示 Token 使用分析。 |
| 脱敏策略 | 输出事实源和复盘文档不得包含原始 prompt、系统指令或本机绝对路径。 |

### 4.2 不包含

| 不包含 | 说明 |
|---|---|
| 提交原始 `~/.codex/sessions` | 原始 session JSONL 只作为本机输入，不进入仓库。 |
| 改造 Codex 客户端 | 不修改 Codex Desktop 或模型 API 的底层记录方式，只做后处理解析。 |
| 实时写入每个命令 | 第一版采用后处理提取，不要求命令执行中实时更新事实表。 |
| 修改 `trace.md` 变更记录结构 | `trace.md` 仍作为流程事实源；Token usage 通过独立事实表关联。 |
| 精确计费系统 | 本需求关注 Token 使用分析，不承担价格、账单或额度扣费核算。 |
| Web / 小程序 UI | 不新增可见产品页面或管理端交互。 |

## 5. 功能要求

### FR-001 `data/ai-usage/` 事实源目录

系统 MUST 使用 `data/ai-usage/` 作为脱敏后的 AI 使用量事实源目录。

该目录 SHOULD 至少支持两类输出：

| 文件类型 | 用途 |
|---|---|
| command run 明细 | 记录每个用户一轮消息对应的命令运行统计。 |
| Sprint 聚合快照 | 按 Sprint 聚合命令环节维度，供 `/sprint-exps` 读取。 |

原始 `~/.codex/sessions` 路径 MAY 出现在本地命令参数或本地日志中，但 MUST NOT 原样写入长期文档、Sprint 复盘或仓库事实源。

### FR-002 本地会话解析

解析能力 MUST 能读取 `~/.codex/sessions/**/rollout-*.jsonl` 中的结构化事件，并识别以下信息：

- `session_meta` 中的 session id、cwd、模型提供方等必要元数据；
- `turn_context` 中的 `turn_id`、模型、工作目录和时间；
- `response_item` / 用户消息中的命令文本和 REQ/BUG/Change/Sprint 编号；
- `event_msg` 且 `payload.type == token_count` 的 Token 使用量事件；
- 工具调用和工具结果事件，用于估算工具调用次数、工具输出字符数和失败重跑。

解析器 MUST 对未知事件类型保持兼容，不得因单个异常事件导致整个 Sprint 提取失败。

### FR-003 命令运行边界

命令运行边界 MUST 定义为“用户一轮消息”。

一个 command run 包含该轮用户消息触发后的所有模型调用、工具调用和中间输出，直到下一轮用户消息或会话结束。若同一轮用户消息中显式处理多个 REQ/BUG，command run MAY 关联多个 Issue，并标记归因置信度。

command run MUST 至少包含：

```yaml
command_run_id: tokenrun-YYYYMMDD-...
started_at: YYYY-MM-DD HH:mm:ss
ended_at: YYYY-MM-DD HH:mm:ss
command: /req-generate
workflow_event: req.generate
requirements: []
bugs: []
changes: []
sprint_id: null
attribution_confidence: high | medium | low
```

### FR-004 Token 指标

每个 command run MUST 聚合以下模型指标：

| 指标 | 说明 |
|---|---|
| `model_call_count` | 该轮内 `token_count` 事件数量。 |
| `input_tokens` | `last_token_usage.input_tokens` 求和。 |
| `cached_input_tokens` | `last_token_usage.cached_input_tokens` 求和。 |
| `output_tokens` | `last_token_usage.output_tokens` 求和。 |
| `reasoning_output_tokens` | `last_token_usage.reasoning_output_tokens` 求和。 |
| `total_tokens` | `last_token_usage.total_tokens` 求和。 |

MUST 使用 `last_token_usage` 聚合单次模型调用，不得直接把整个 session 的 `total_token_usage` 当作单个命令成本。

### FR-005 工具与重跑指标

每个 command run MUST 聚合以下执行指标：

| 指标 | 说明 |
|---|---|
| `tool_call_count` | 工具调用次数。 |
| `tool_output_chars` | 工具结果输出字符数，按脱敏后的文本长度或原始输出长度统计。 |
| `retry_count` | 失败后重试、同类命令/工具重复执行或明确 retry 事件的估算次数。 |

失败重跑第一版 MAY 采用近似规则，例如同一 command run 内出现失败工具结果后再次调用同类工具，或同一命令因校验失败再次执行。事实源 MUST 标记 `retry_count_method`，避免误认为完全精确。

### FR-006 Issue / Change / Sprint 关联

事实源 MUST 通过独立字段关联工作流对象：

- `requirements[]`：关联 `REQ-*`；
- `bugs[]`：关联 `BUG-*`；
- `changes[]`：关联 OpenSpec Change ID；
- `sprint_id`：关联 `sprint-xxx`；
- `workflow_event`：关联 `req.*`、`bug.*`、`opsx.*`、`sprint.*`。

关联规则 SHOULD 按优先级使用：

1. 用户命令文本中的显式 ID；
2. Workflow Sync 命令参数；
3. 当前工作目录和 trace 变更记录时间窗口；
4. Sprint `sprint.yaml` 的 scope 反查；
5. 人工补录或低置信度推断。

当归因不唯一时，MUST 支持多值关联，并设置 `attribution_confidence: medium|low`。

### FR-007 sprint-exps 命令环节展示

`/sprint-exps` MUST 优先读取 `data/ai-usage/` 的 Sprint 聚合快照，并按命令环节维度展示 Token 使用分析。

报告 SHOULD 至少展示：

| 维度 | 示例 |
|---|---|
| 命令环节 | `/req-capture`、`/req-generate`、`/req-complete`、`/req-review`、`/req-opsx`、`/opsx-apply`、`/sprint-archive`、`/sprint-exps` |
| 调用统计 | command run 数、模型调用次数、工具调用次数、失败重跑次数 |
| Token 统计 | input/cached/output/reasoning/total tokens |
| 高消耗原因 | 大规则读取、archive 搜索、测试日志、Workflow Sync 输出、生成物 diff |
| 优化建议 | 收敛读取边界、脚本摘要、输出截断、拆分命令或补充 fact sheet |

若没有真实聚合数据，`sprint-exps` MAY 回退到估算模式，但 MUST 明确标注“无精确 token 计量”。

### FR-008 脱敏与安全

Token 使用量事实源和复盘输出 MUST 遵守以下脱敏规则：

- 不保存原始 prompt 全文；
- 不保存系统指令、developer 指令、AGENTS 全文或技能全文；
- 不保存 `~/.codex/sessions` 原始 JSONL 内容；
- 不保存本机绝对路径；路径应转为仓库相对路径、`~/.codex/sessions/<redacted>` 或 hash；
- 不保存工具输出全文，仅保存字符数、行数、命令类型或短摘要；
- 不保存密钥、Cookie、Authorization、真实客户数据或 `.env` 内容。

若无法确认内容是否安全，MUST 默认不写入长期事实源，只记录统计数字和低风险元数据。

### FR-009 可复盘与可校验

事实源 SHOULD 支持校验和复跑：

- 同一 session 文件重复提取应尽量幂等；
- command run 记录应包含来源摘要，例如 session id hash、turn id hash、时间范围；
- 聚合快照应能由明细重新生成；
- 提取脚本应输出 warnings，例如无法归因、缺少 token_count、发现本地绝对路径、疑似敏感内容被跳过。

## 6. UI 约束

本需求不涉及 Web、管理端、小程序或店主端 UI。

Markdown 复盘输出应保持可扫描：

- 命令环节维度使用表格展示；
- 高消耗来源使用短摘要，不复制原始日志；
- 证据引用优先使用相对路径、hash 或统计行，不使用本机绝对路径；
- 数字口径必须标明真实统计或估算。

## 7. 数据与目录约束

| 项 | 约束 |
|---|---|
| `data/ai-usage/` | 存放脱敏后的使用量事实源和 Sprint 聚合快照。 |
| `~/.codex/sessions` | 仅作为本地输入，不纳入仓库，不在复盘中原样引用。 |
| `trace.md` | 不写完整 Token 明细；必要时未来 MAY 写轻量 `usage_ref`，但本期不要求。 |
| `docs/knowledge-base/retrospectives/` | 只展示聚合结果、趋势和优化建议。 |

若 `data/ai-usage/` 中存在可能包含本机或敏感信息的明细文件，后续实现 MUST 明确提交边界，例如 `.gitignore`、README 或仅提交聚合快照。

## 8. 关联需求与文档

| 类型 | 关联项 | 说明 |
|---|---|---|
| 相关规则 | `rules/agent-context-budget.md` | 定义上下文预算和高消耗来源控制。 |
| 相关流程 | `/sprint-exps` | 使用 Token Usage Fact Sheet 做 Sprint 复盘。 |
| 相关脚本 | `scripts/generate-sprint-fact-sheet.py` | 后续可接入 AI usage 聚合快照。 |
| 相关文档 | `docs/knowledge-base/retrospectives/sprint-005-retrospective.md` | 已提出模型 Token 使用分析和 fact sheet 优化方向。 |
| 本地输入 | `~/.codex/sessions/**/rollout-*.jsonl` | Codex session JSONL，仅本地读取。 |

## 9. 风险与约束

| 风险 | 说明 | 缓解 |
|---|---|---|
| 归因不准确 | 一轮用户消息可能处理多个 Issue，或命令文本缺少明确 ID。 | 支持多值关联和 `attribution_confidence`。 |
| 泄露敏感上下文 | session JSONL 包含原始 prompt、系统指令、工具输出和本机路径。 | 事实源只写统计和脱敏元数据，默认不保存原文。 |
| Token 口径误用 | `total_token_usage` 是 session 累计，直接使用会夸大单命令成本。 | 明确使用 `last_token_usage` 聚合 command run。 |
| 重跑统计不精确 | 工具失败与重试的边界不总是明确。 | 第一版记录近似方法和置信度，后续迭代优化。 |
| data 目录提交边界 | `data/` 可能被误放入本地运行产物或敏感数据。 | 后续实现必须同步 README / `.gitignore` / 目录说明。 |
| sprint-exps 输出过重 | Token 分析本身可能增加复盘 token 消耗。 | 优先读取聚合快照，只展示命令环节摘要和 top sources。 |

## 10. 状态

```yaml
status: archived
lifecycle_stage: plan
next: /req-opsx REQ-0034-ai-token-usage-observability
readiness: Ready
needs_prototype: false
needs_api_change: false
needs_database_change: false
needs_orval: false
needs_docker_validation: false
```
