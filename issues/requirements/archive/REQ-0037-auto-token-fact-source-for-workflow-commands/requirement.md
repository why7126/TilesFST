---
requirement_id: REQ-0037-auto-token-fact-source-for-workflow-commands
title: 工作流命令自动构建 AI Token 事实源
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0034-ai-token-usage-observability
created_at: 2026-07-12 09:54:10
updated_at: 2026-07-15 13:14:09
---

# REQ-0037 工作流命令自动构建 AI Token 事实源

## 1. 需求背景

REQ-0034 已建立 `data/ai-usage/` 作为 AI 命令 Token 使用量事实源，并提供从本地 Codex session JSONL 后处理生成 command run 明细和 Sprint 聚合快照的能力。REQ-0035 进一步把 AI usage snapshot 纳入 Sprint close / `/sprint-exps` 默认流程，避免复盘阶段静默使用估算。

当前仍存在一个流程缺口：多数 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 命令执行后，不会自动构建或刷新 Token 事实源。真实使用量仍依赖操作者事后记得运行 `scripts/extract-ai-usage.py`，这会带来以下问题：

- 命令刚执行完时上下文最清楚，但事实源生成被推迟到 Sprint close 或复盘阶段，容易遗漏。
- `/req-capture`、`/bug-capture`、`/req-generate`、`/bug-complete` 等尚未纳入 Sprint 的命令成本难以稳定沉淀。
- Sprint 聚合快照即使在收尾时生成，也可能缺少早期流程命令的明细或归因。
- 每个技能若手工追加相同提取逻辑，容易造成维护成本高、脱敏边界不一致、输出过重。

本需求用于把“工作流命令执行后自动构建 AI Token 事实源”提升为统一的 Agent 工作流能力，让每个相关命令在完成主流程后，尽可能自动记录或刷新脱敏使用量事实。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 项目负责人 | 看到 REQ/BUG/Change/Sprint 全链路命令的真实 AI Token 消耗，辅助容量和流程优化判断。 |
| 开发负责人 | 识别哪些命令族、规则读取、测试输出或 Workflow Sync 环节最容易造成高消耗。 |
| AI / Codex Agent | 在每个工作流命令结束时自动执行统一 post-command usage hook，减少手工步骤和遗漏。 |
| 复盘读者 | 在 Sprint 复盘中看到更完整的命令级用量，而不是只看到收尾阶段估算。 |
| 流程维护者 | 用统一脚本和规则维护事实源构建逻辑，避免所有命令技能重复粘贴实现细节。 |
| 安全 / 治理负责人 | 确保自动构建过程仍遵守 REQ-0034 的脱敏与本地 session 边界，不把敏感上下文写入仓库。 |

## 3. 需求目标

- 每个 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 工作流命令完成后，SHOULD 自动构建或刷新 AI Token 使用量事实源。
- 自动构建 MUST 复用 REQ-0034 的 `data/ai-usage/` 目录、字段口径、脱敏边界和 snapshot 校验规则。
- 自动构建 SHOULD 通过统一 post-command hook 或脚本封装完成，避免在每个 skill 中复制长逻辑。
- 当本地 session 输入不可用、无法归因或生成失败时，命令 MUST 输出明确 warning 和 recommended action，但默认不得阻断主业务命令。
- 自动构建 MUST 支持尚未纳入 Sprint 的 REQ/BUG 命令，至少沉淀 command run 明细；具备 Sprint 归属时再刷新 Sprint 聚合快照。
- 自动构建输出必须短摘要化，不得打印原始 session JSONL、prompt、系统/developer 指令或工具输出正文。

## 4. 范围

### 4.1 包含

| 范围 | 说明 |
|---|---|
| 工作流命令族 | 覆盖 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 命令技能。 |
| 自动构建触发点 | 在主命令完成且 Workflow Sync 成功后触发 usage fact source hook；若命令不改变状态，也可在最终输出前触发只读检查或记录 recommended action。 |
| 统一 post-command hook | 新增或复用脚本封装 `extract-ai-usage`、snapshot check、归因参数和安全摘要输出。 |
| command run 明细 | 对每个可解析用户命令轮次生成或刷新 `data/ai-usage/command-runs/` 脱敏明细。 |
| Sprint 聚合快照 | 当可解析到 `sprint_id` 或 Sprint scope 时，生成或刷新 `data/ai-usage/sprints/<sprint-id>.json`。 |
| Issue / Change 归因 | 使用命令参数、Workflow Sync event、REQ/BUG/Change ID、Sprint scope 和人工映射辅助归因。 |
| 失败降级 | session 不可访问、snapshot 过期、覆盖不足、敏感内容跳过等情况输出 warning，不静默伪装为 actual。 |
| 技能与规则同步 | 更新相关命令技能、`data/ai-usage/README.md`、必要时更新 `rules/agent-context-budget.md` 或工作流规则。 |

### 4.2 不包含

| 不包含 | 说明 |
|---|---|
| 修改 Codex Desktop 底层记录 | 不改造 Codex 客户端或模型 API 记录机制，仍基于本地 session 后处理或可用元数据。 |
| 提交原始 session | 原始 `~/.codex/sessions/**/*.jsonl` 仍只作为本机输入，不进入仓库。 |
| 精确账单系统 | 本需求只处理 Token 使用量事实源，不做价格、额度、成本中心或发票核算。 |
| Web / 小程序 UI | 不新增管理端、店主端、小程序可见页面。 |
| 阻断所有工作流命令 | 自动构建失败默认不阻断主命令，除非后续设计明确某些收尾命令需要强门禁。 |
| 回填所有历史会话 | 可支持人工补跑历史 session，但本需求不要求一次性回填所有历史命令。 |

## 5. 功能要求

### FR-001 工作流命令完成后触发 usage hook

系统 SHOULD 在每个 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 命令完成主流程后触发统一 AI usage fact source hook。

触发顺序 SHOULD 为：

1. 主命令完成文件写入或校验；
2. 按命令要求运行 Workflow Sync；
3. Workflow Sync 成功后触发 usage hook；
4. 输出 usage hook 的短摘要、warning 和 recommended action；
5. 输出最终命令摘要。

若主命令失败或 Workflow Sync 失败，usage hook MAY 跳过，并在最终输出中说明未构建事实源。

### FR-002 统一 post-command hook

系统 MUST 通过统一脚本、函数或等价封装执行自动构建逻辑，避免在每个命令技能中复制 `extract-ai-usage` 的长命令与判断分支。

统一 hook SHOULD 支持以下输入：

```yaml
workflow_event: req.generate
requirement_id: REQ-0037-auto-token-fact-source-for-workflow-commands
bug_id: null
change_id: null
sprint_id: auto | sprint-xxx | null
session_jsonl: <local-session-jsonl-or-auto>
manual_map: optional
mode: build | check | recommended-action
```

统一 hook SHOULD 输出以下摘要：

```yaml
ai_usage_fact_source:
  status: generated | refreshed | skipped | failed
  usage_mode: actual | estimated_fallback | unavailable
  command_runs: 0
  sprint_snapshot: null
  warnings: []
  recommended_action: null
```

### FR-003 本地 session 输入发现与安全边界

自动构建 MUST 明确本地 session 输入来源，不得盲目读取或持久化原始 session 内容。

输入来源优先级 SHOULD 为：

1. 用户显式传入或配置的本地 session JSONL；
2. 环境变量或本地配置指定的 session JSONL；
3. 可安全定位的当前 Codex session 文件；
4. 无法定位时输出 recommended action，不构建 actual 事实源。

无论使用哪种输入来源，系统 MUST NOT 将原始 session 路径、原始 JSONL 内容、prompt、系统/developer 指令或工具输出正文写入仓库事实源。

### FR-004 命令族覆盖范围

自动构建 SHOULD 覆盖以下命令族：

| 命令族 | 示例 | 归因重点 |
|---|---|---|
| `/req-*` | `/req-capture`、`/req-generate`、`/req-complete`、`/req-review`、`/req-opsx` | `requirements[]`、`workflow_event`、可选 `changes[]` |
| `/bug-*` | `/bug-capture`、`/bug-generate`、`/bug-complete`、`/bug-review`、`/bug-opsx` | `bugs[]`、`workflow_event`、可选 `changes[]` |
| `/opsx-*` | `/opsx-propose`、`/opsx-apply`、`/opsx-archive`、`/opsx-explore` | `changes[]`、关联 REQ/BUG、Sprint scope |
| `/sprint-*` | `/sprint-propose`、`/sprint-apply`、`/sprint-archive`、`/sprint-exps` | `sprint_id`、Sprint scope、聚合 snapshot |

探索类命令若不产生文件状态变化，MAY 只记录 command run 明细或输出 recommended action；不得为了构建事实源强制改变 REQ/BUG/Sprint 状态。

### FR-005 尚未纳入 Sprint 的命令处理

对于尚未纳入 Sprint 的 REQ/BUG 命令，系统 SHOULD 至少生成 command run 明细，并通过 `requirements[]` 或 `bugs[]` 归因。

当 `sprint_id` 不存在或 `--sprint auto` 无法解析时：

- MUST NOT 伪造 Sprint 聚合快照；
- SHOULD 写入 command run 明细；
- SHOULD 在摘要中标注 `sprint_snapshot: skipped`；
- MAY 提示后续纳入 Sprint 后可重新聚合或刷新 snapshot。

### FR-006 Sprint 聚合快照刷新

当命令可明确关联到某个 `sprint-xxx` 时，系统 SHOULD 生成或刷新 `data/ai-usage/sprints/<sprint-id>.json`。

刷新逻辑 SHOULD：

- 复用已有 command run 明细；
- 使用 Sprint scope 中的 REQ/BUG/Change 辅助 coverage 校验；
- 更新 `generated_at`；
- 保留 warning；
- 确保 `totals` 中 command run、模型调用、工具调用和 token 指标不为空时才标记为 `actual`。

若覆盖不足、指标为空或 snapshot 过期，MUST 标记为 `estimated_fallback` 或输出对应 warning。

### FR-007 自动构建失败降级

自动构建失败默认不得阻断主工作流命令。

以下情况 SHOULD 降级为 warning：

- 本地 session JSONL 不存在或不可访问；
- 当前命令无法定位 session 输入；
- JSONL 解析失败或缺少 `token_count`；
- 归因到多个 REQ/BUG/Change，置信度不足；
- snapshot coverage 缺失或过期；
- 检测到敏感文本并跳过持久化；
- 写入 `data/ai-usage/` 失败。

降级输出 MUST 包含：

```yaml
ai_usage_mode: estimated_fallback | unavailable
reason: ...
recommended_action: ...
```

### FR-008 脱敏与持久化边界

自动构建 MUST 沿用 REQ-0034 的安全边界。

允许持久化：

- 数字指标；
- REQ/BUG/Change/Sprint/workflow event；
- session hash、turn hash、时间范围、源行号范围；
- snapshot `generated_at`、coverage、warning；
- 短安全标签。

禁止持久化：

- 原始 prompt；
- 系统指令、developer 指令、AGENTS 全文、技能全文；
- 原始 `~/.codex/sessions` JSONL；
- 本机绝对路径；
- `.env` 内容、密钥、Cookie、Authorization、Token；
- 工具输出正文、测试日志全文、OpenAPI/Orval 生成物 diff 全文；
- 真实客户数据或联系方式。

### FR-009 技能文件最小改造

命令技能 SHOULD 只声明统一 usage hook 的调用时机和输出要求，不应粘贴复杂解析逻辑。

候选改造方式：

- 在通用规则中定义 `Final Step — AI Usage Fact Source`；
- 或在每个命令技能的 Final Step 中引用同一个脚本命令；
- 或扩展 Workflow Sync 后置流程，但不得让 Workflow Sync 直接持久化敏感 session 内容。

无论采用哪种方式，技能输出 MUST 保持短摘要，避免因为自动构建事实源反过来造成过高 Token 消耗。

### FR-010 可校验与可复跑

自动构建 MUST 支持复跑和校验。

系统 SHOULD 提供：

- 检查某个 REQ/BUG/Change/Sprint 是否已有对应 command run 的能力；
- 检查 Sprint snapshot 是否覆盖当前 scope 的能力；
- 重复执行同一 session 提取时避免重复累计的能力；
- `--dry-run` 或 check 模式，用于在不写入事实源的情况下预览可构建状态；
- 测试覆盖成功生成、session 缺失、snapshot stale、coverage missing、敏感内容跳过等路径。

## 6. UI 约束

本需求不涉及 Web 管理端、店主 Web、小程序或可见产品 UI。

命令行和 Markdown 输出应遵守以下约束：

- 使用短摘要和表格展示 usage hook 结果；
- 不输出原始 session、prompt、工具日志或大段 diff；
- 对 `actual`、`estimated_fallback`、`unavailable` 明确标识；
- recommended action 使用可执行命令或下一步 workflow 命令；
- 不因展示 Token 分析而重复读取大规则、大目录或生成物全文。

## 7. 数据与目录约束

| 项 | 约束 |
|---|---|
| `data/ai-usage/command-runs/` | 保存脱敏 command run 明细；提交前必须人工确认安全。 |
| `data/ai-usage/sprints/` | 保存 Sprint 聚合快照，供 Fact Sheet、`/sprint-archive`、`/sprint-exps` 消费。 |
| `data/ai-usage/local/` | 可保存本地临时映射或中间文件；不得提交敏感内容。 |
| `~/.codex/sessions` | 仅作为本机输入，不进入仓库事实源。 |
| `trace.md` | 不写完整 Token 明细；必要时未来 MAY 写轻量 usage ref，但本需求不强制。 |

## 8. 关联需求与文档

| 类型 | 关联项 | 说明 |
|---|---|---|
| 父需求 | `REQ-0034-ai-token-usage-observability` | 定义 AI Token 使用量事实源、脱敏策略和聚合口径。 |
| 相关需求 | `REQ-0035-ai-usage-snapshot-sprint-close-exps` | 已将 snapshot 检查纳入 Sprint close / exps 默认流程。 |
| 相关规则 | `rules/agent-context-budget.md` | 约束读取边界、输出截断和高消耗来源。 |
| 相关目录 | `data/ai-usage/` | command run 明细与 Sprint snapshot 存放位置。 |
| 相关脚本 | `scripts/extract-ai-usage.py`、`scripts/generate-sprint-fact-sheet.py` | 可复用或封装为 post-command hook。 |
| 相关技能 | `.agents/skills/{req,bug,opsx,sprint,build}-*`、`.agents/skills/capture`、`.agents/skills/initialize-project` | 本需求涉及其 Final Step 或统一后置步骤。 |

## 9. 风险与约束

| 风险 | 说明 | 缓解 |
|---|---|---|
| 自动构建找不到当前 session | Codex session 路径可能无法从命令内部稳定发现。 | 支持显式参数、环境变量、本地配置和 recommended action fallback。 |
| 自动构建拖慢每个命令 | 每个工作流命令结束都运行提取可能增加耗时。 | 使用增量、摘要、check-first 和可跳过策略。 |
| 重复累计 | 同一 session 多次提取可能重复写入 totals。 | 依赖 session hash、turn hash、command run id 做幂等。 |
| 敏感信息泄露 | session 包含 prompt、系统指令、本机路径和工具输出。 | 沿用 REQ-0034 脱敏边界，默认不持久化不确定文本。 |
| skill 维护成本上升 | 每个 skill 都改 Final Step 容易重复。 | 优先建立统一 hook 或共享脚本入口。 |
| 事实源构建本身消耗 Token | 自动步骤若输出过多，会反向增加上下文成本。 | 只输出状态、计数、warning 和 recommended action。 |
| 主命令被副作用阻断 | usage hook 失败可能影响正常需求/BUG流程。 | 默认 warning，不阻断；仅 Sprint close 等收尾场景可设计更强门禁。 |

## 10. 状态

```yaml
status: done
lifecycle_stage: plan
next: /req-opsx REQ-0037-auto-token-fact-source-for-workflow-commands
readiness: Ready
needs_prototype: false
needs_api_change: false
needs_database_change: false
needs_orval: false
needs_docker_validation: false
```
