---
requirement_id: REQ-0035-ai-usage-snapshot-sprint-close-exps
title: AI usage snapshot 纳入 Sprint close / exps 默认流程
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0034-ai-token-usage-observability
created_at: 2026-07-11 23:42:45
updated_at: 2026-07-15 13:14:04
---

# REQ-0035 AI usage snapshot 纳入 Sprint close / exps 默认流程

## 1. 需求背景

REQ-0034 已建立 AI Token 使用量观测与 Sprint 复盘接入方向，但如果 Sprint 收尾和复盘命令仍依赖人工记忆或临时估算，`/sprint-exps` 仍可能继续输出 estimated fallback，无法稳定沉淀真实 AI 使用量经验。

当前风险集中在流程默认值：

- Sprint close 或归档前未自动生成 AI usage snapshot，导致复盘时缺少真实事实源；
- `/sprint-exps` 在 snapshot 缺失时可能静默回退估算，读者难以区分真实统计与估算；
- snapshot 生成失败、缺失或过期时缺少统一提示，无法形成可执行的收尾检查；
- AI usage 事实源虽然存在，但未被 Sprint close / exps 命令链稳定消费。

本需求用于把 AI usage snapshot 生成与读取纳入 Sprint close / exps 默认流程，让每次 Sprint 复盘优先使用真实统计，并在无法使用真实数据时明确暴露缺口。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 项目负责人 | Sprint 收尾时确认 AI 使用量事实源已生成，复盘不再依赖不透明估算。 |
| 开发负责人 | 通过真实 snapshot 识别高消耗命令环节、失败重跑和上下文浪费来源。 |
| AI / Codex Agent | 在 `/sprint-archive`、Sprint close 和 `/sprint-exps` 中按默认流程生成、校验和消费 snapshot。 |
| 复盘读者 | 清楚区分真实统计、缺失数据和估算 fallback，避免误读复盘结论。 |
| 流程维护者 | 能在技能、规则和脚本层建立稳定门禁，避免后续命令回退到旧行为。 |

## 3. 需求目标

- Sprint close / archive 默认触发或检查 AI usage snapshot 生成。
- `/sprint-exps` 默认优先读取 snapshot，不再静默使用 estimated fallback。
- snapshot 缺失、过期或生成失败时，命令输出必须给出明确 warning 与修复建议。
- 真实统计与估算 fallback 在复盘文档中必须有清晰标识。
- 该流程应复用 REQ-0034 已定义的 AI usage 事实源、脱敏策略和聚合口径。

## 4. 范围

### 4.1 包含

| 范围 | 说明 |
|---|---|
| Sprint close / archive 默认检查 | 在 Sprint 收尾流程中检查 AI usage snapshot 是否存在、是否覆盖目标 Sprint。 |
| snapshot 生成入口 | 当缺少 snapshot 时，提供默认生成动作或明确的生成命令提示。 |
| `/sprint-exps` 消费规则 | 复盘优先读取真实 snapshot，并按命令环节展示 AI usage 分析。 |
| fallback 显式化 | 无真实 snapshot 时允许估算，但必须显式标注并列出缺口。 |
| 技能与规则约束 | 更新相关命令技能或流程规则，使 snapshot 成为默认步骤。 |
| 校验与报告 | 输出 snapshot 状态、覆盖范围、统计口径和 warning。 |

### 4.2 不包含

| 不包含 | 说明 |
|---|---|
| 重新设计 AI usage 事实源 | 事实源目录、字段、脱敏和聚合口径沿用 REQ-0034。 |
| 修改 Codex 客户端 | 不改造 Codex Desktop 或底层 session 记录机制。 |
| 构建 Web UI | 不新增管理端、店主端或小程序页面。 |
| 精确费用核算 | 只处理 token usage snapshot，不承担价格、账单或成本中心核算。 |
| 自动修复历史 Sprint | 旧 Sprint 可按需补跑 snapshot，但不要求本需求一次性回填所有历史数据。 |

## 5. 功能要求

### FR-001 Sprint close 默认检查 snapshot

Sprint close / archive 流程 MUST 检查目标 Sprint 是否存在 AI usage snapshot。

检查结果 MUST 至少包含：

| 字段 | 说明 |
|---|---|
| `sprint_id` | 被检查的 Sprint 编号。 |
| `snapshot_path` | snapshot 相对路径；缺失时为 `null`。 |
| `snapshot_status` | `present`、`missing`、`stale`、`failed`。 |
| `coverage` | snapshot 覆盖的时间范围、命令数量或可归因对象摘要。 |
| `usage_mode` | `actual` 或 `estimated_fallback`。 |

若 snapshot 缺失，流程 SHOULD 尝试执行默认生成步骤；若无法自动生成，MUST 输出明确 warning 与下一步命令。

### FR-002 snapshot 生成接入默认流程

系统 MUST 为 Sprint close / archive 提供默认 snapshot 生成入口。

生成入口 SHOULD：

- 复用 REQ-0034 定义的 `data/ai-usage/` 事实源；
- 使用目标 Sprint 的 scope、时间范围和关联 REQ/BUG/Change 辅助归因；
- 生成或刷新 Sprint 聚合快照；
- 输出生成摘要，而不是输出完整 session、prompt 或工具日志；
- 对缺失 session、无法归因、疑似敏感内容跳过等情况输出 warnings。

若生成失败，命令 MUST 不得静默继续写出“真实统计”结论。

### FR-003 `/sprint-exps` 优先读取真实 snapshot

`/sprint-exps` MUST 优先读取目标 Sprint 的 AI usage snapshot。

当 snapshot 可用时，复盘输出 MUST 使用 `actual` 口径，并展示：

- command run 数；
- 模型调用次数；
- input / cached / output / reasoning / total tokens；
- 工具调用次数；
- 失败重跑次数；
- 高消耗命令环节和可执行优化建议。

当 snapshot 不可用时，`/sprint-exps` MAY 使用估算 fallback，但 MUST 在输出中显式标注 `estimated_fallback`，并列出缺失原因和建议补跑命令。

### FR-004 禁止静默 estimated fallback

任何 Sprint close / exps 输出不得静默使用 estimated fallback。

满足以下任一情况时，输出 MUST 明确标注：

- snapshot 文件不存在；
- snapshot 生成时间早于 Sprint 最近一次 scope 或 trace 变更；
- snapshot 无法覆盖当前 Sprint 的关键 REQ/BUG/Change；
- snapshot 中 token 统计为 0 或缺少必要指标；
- session 数据不可访问或解析失败；
- 只能根据历史经验、手工观察或非结构化日志估算。

标注内容 MUST 包含：

```yaml
ai_usage_mode: estimated_fallback
reason: ...
recommended_action: ...
```

### FR-005 snapshot 新鲜度与覆盖校验

系统 SHOULD 校验 snapshot 新鲜度和覆盖范围。

校验规则 SHOULD 至少考虑：

- snapshot 生成时间是否晚于目标 Sprint 最近一次 archive / close / scope 更新；
- snapshot 是否包含目标 Sprint ID；
- snapshot 是否覆盖 Sprint scope 中的主要 REQ/BUG/Change；
- snapshot 是否包含至少一个 command run 或明确说明无可用 session；
- snapshot 是否包含 `actual` / `estimated_fallback` 口径字段。

无法完全校验时，MUST 降级为 warning，不得伪装为完整真实统计。

### FR-006 收尾报告记录 snapshot 状态

Sprint close / archive 输出 SHOULD 记录 AI usage snapshot 状态摘要。

摘要 SHOULD 包含：

| 项 | 说明 |
|---|---|
| snapshot 状态 | present / missing / stale / failed |
| 使用口径 | actual / estimated_fallback |
| 生成时间 | `YYYY-MM-DD HH:mm:ss` |
| 关联文件 | snapshot 相对路径 |
| warning 数量 | 无法归因、数据缺失、解析失败等 |

是否写入 `acceptance-report.md`、`release-note.md` 或 Sprint trace 由后续设计明确；第一版至少要求命令输出可见，避免复盘遗漏。

### FR-007 技能与规则默认步骤

相关命令技能 MUST 把 AI usage snapshot 生成或校验列入默认流程。

候选命令包括：

- `/sprint-archive`：归档前检查或生成 snapshot；
- `/sprint-exps`：复盘前读取 snapshot，缺失时显式 fallback；
- 未来若存在独立 Sprint close 命令，也应继承同一规则。

技能说明 MUST 避免要求读取原始 session 全文；应通过脚本或聚合文件读取摘要。

### FR-008 安全与脱敏继承

snapshot 默认流程 MUST 继承 REQ-0034 的安全与脱敏约束：

- 不写入原始 prompt；
- 不写入系统指令、developer 指令或技能全文；
- 不写入 `~/.codex/sessions` 原始 JSONL；
- 不写入本机绝对路径；
- 不写入工具输出全文；
- 不写入密钥、Cookie、Authorization、真实客户数据或 `.env` 内容。

若 snapshot 生成步骤发现疑似敏感内容，MUST 跳过原文，仅记录统计数字和 warning。

## 6. UI 约束

本需求不涉及 Web、管理端、小程序或店主端 UI。

命令输出和复盘 Markdown SHOULD 保持轻量、可扫描：

- 使用表格展示 snapshot 状态和命令环节统计；
- 使用 `actual` / `estimated_fallback` 明确标记口径；
- 只展示摘要和相对路径，不复制原始日志；
- warning 应短句化，并附可执行下一步。

## 7. 关联需求

| 类型 | 关联项 | 说明 |
|---|---|---|
| 父需求 | `REQ-0034-ai-token-usage-observability` | 已定义 AI usage 事实源、指标、脱敏和 sprint-exps 接入方向。 |
| 相关流程 | `/sprint-archive` | Sprint 收尾 / 归档阶段检查或生成 snapshot。 |
| 相关流程 | `/sprint-exps` | Sprint 经验复盘优先消费 snapshot。 |
| 相关规则 | `rules/agent-context-budget.md` | 控制读取范围，避免 snapshot 分析本身造成过高上下文消耗。 |
| 相关技能 | `.agents/skills/sprint-archive/SKILL.md` | 后续需要纳入默认步骤。 |
| 相关技能 | `.agents/skills/sprint-exps/SKILL.md` | 后续需要禁止静默 estimated fallback。 |

## 8. 风险与约束

| 风险 | 说明 | 缓解 |
|---|---|---|
| close 阶段定义不清 | 项目当前可能以 `/sprint-archive` 承担 close 语义。 | 后续设计明确 close 与 archive 的边界；第一版优先接入 `/sprint-archive`。 |
| session 数据不可访问 | 本机 session 文件可能被清理或不在当前机器。 | 输出 `estimated_fallback` 与补救建议，不伪造真实统计。 |
| snapshot 过期 | Sprint scope 或 trace 更新后 snapshot 未刷新。 | 校验新鲜度，标记 `stale` 并提示重生成。 |
| 复盘输出变重 | token 分析表过长会增加复盘成本。 | 只展示聚合摘要和 top sources，明细留在 snapshot 文件。 |
| 敏感信息泄露 | session 中包含 prompt、路径和工具输出。 | 继承 REQ-0034 脱敏规则，只保留统计与低风险元数据。 |

## 9. 状态

```yaml
status: done
lifecycle_stage: review
next: /opsx-apply update-ai-usage-snapshot-sprint-close-exps
readiness: Ready
needs_prototype: false
needs_api_change: false
needs_database_change: false
needs_orval: false
needs_docker_validation: false
```
