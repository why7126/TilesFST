---
requirement_id: REQ-0040-rule-skill-read-summary-reuse-context-budget
title: 规则/Skill 已读摘要复用纳入命令上下文预算治理
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0034-ai-token-usage-observability
created_at: 2026-07-16 09:02:54
updated_at: 2026-07-18 09:18:43
---

# REQ-0040 规则/Skill 已读摘要复用纳入命令上下文预算治理

## 1. 需求背景

项目已通过 `rules/agent-context-budget.md` 建立上下文预算治理原则，要求命令执行时“先定位，再摘要，再片段读取”，并要求同一会话中已读且无变更的规则文件用摘要承接，避免重复全量读取。当前各命令 Skill 也普遍在 `Context Budget Guardrails` 中引用该规则。

但现有规则仍偏原则化，缺少“已读摘要复用”的统一执行定义：

- 哪些文件可以用摘要承接，尤其是 `.agents/skills/*/SKILL.md` 是否与 `rules/` 一样适用；
- 摘要需要包含哪些最小信息，才能既节省 token，又不丢失关键门禁；
- 摘要何时失效，例如文件变更、任务类型切换、风险升级或用户要求重读；
- 命令 Skill 应如何表述该机制，避免每个命令重复发明不同读法；
- 校验脚本如何发现命令 Skill 回退到宽泛读取或缺少摘要复用约束。

本需求用于把“规则/Skill 已读摘要复用”从口头原则沉淀为可执行的上下文预算治理机制，减少连续命令中反复读取同一规则和 Skill 文件造成的上下文浪费。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| AI / Codex Agent | 在连续执行 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 等命令时，能安全复用已读规则和 Skill 摘要，减少重复上下文输入。 |
| 项目负责人 | 希望工作流命令保持规范一致，同时降低高频规则读取带来的 token 成本。 |
| 流程维护者 | 需要一个统一模板和校验口径，避免每个 Skill 各自描述预算策略。 |
| 评审者 | 能确认摘要复用不会绕过 OpenSpec、Issue lifecycle、Workflow Sync、安全等强门禁。 |
| 复盘读者 | 在 Sprint 复盘中能识别上下文浪费是否被机制性治理，而不只是事后估算。 |

## 3. 需求目标

- 明确定义同一会话内规则与 Skill 文件的已读摘要复用机制。
- 将 `.agents/skills/*/SKILL.md` 纳入摘要复用治理，不只覆盖 `rules/`。
- 定义摘要的最小内容、适用范围、失效条件和禁止持久化内容。
- 为命令 Skill 提供统一的 `Context Budget Guardrails` 表述模板。
- 增强上下文预算校验，发现缺少规则引用、缺少摘要复用约束或默认宽泛读取的命令 Skill。
- 保持安全边界：不持久化原始 prompt、系统/developer 指令、工具输出正文、密钥或本地绝对路径。

## 4. 范围

### 4.1 包含

| 范围 | 说明 |
|---|---|
| 规则增强 | 更新 `rules/agent-context-budget.md`，明确已读摘要复用的定义、字段、失效条件与安全边界。 |
| Skill 执行模板 | 为命令 Skill 的 `Context Budget Guardrails` 增加统一摘要复用表述。 |
| Skill 覆盖范围 | 明确 `rules/` 与 `.agents/skills/*/SKILL.md` 均可在同一会话内复用摘要。 |
| 失效策略 | 文件内容变更、任务类型升级、命令风险提高、用户要求重读、证据不足时必须重新读取必要片段。 |
| 校验增强 | 扩展 `scripts/validate-agent-context-budget.py` 或等价门禁，检查命令 Skill 是否保留摘要复用约束。 |
| 输出约束 | 命令输出应优先说明“复用了哪些摘要、重新读取了哪些片段”，避免展开全文。 |

### 4.2 不包含

| 不包含 | 说明 |
|---|---|
| 修改 Codex 客户端上下文管理 | 不改造 Codex Desktop、模型 API 或底层 session 机制。 |
| 跨会话强缓存 | 默认只治理同一会话内摘要承接；跨会话持久化需后续单独设计。 |
| 保存原始规则或 Skill 全文副本 | 不在仓库中复制长规则、长 Skill 或工具输出正文。 |
| 重新设计 AI usage 事实源 | REQ-0034/0035/0037 已覆盖 token 事实源与 hook，本需求只治理读取预算机制。 |
| Web / 小程序 / 管理端 UI | 不新增用户可见页面或交互。 |
| API / 数据库变更 | 不新增接口、表结构或 Pydantic Schema。 |

## 5. 功能要求

### FR-001 定义已读摘要复用机制

系统 MUST 在上下文预算规则中定义“已读摘要复用”。

已读摘要 SHOULD 至少包含：

| 字段 | 说明 |
|---|---|
| `path` | 被摘要的规则或 Skill 文件路径。 |
| `read_time` | 本次会话中读取或确认摘要的时间，可仅存在于对话上下文。 |
| `version_hint` | 文件 `updated_at`、mtime、hash 或其他可判断变化的线索。 |
| `summary` | 与当前任务相关的规则、门禁和禁止事项摘要。 |
| `applicability` | 摘要适用的命令族、任务类型或风险边界。 |
| `refresh_reason` | 如需重读，记录触发原因，例如文件变更或用户要求。 |

摘要 MAY 只存在于同一对话上下文中；若后续实现需要落盘，MUST 另行明确脱敏、生命周期和提交边界。

### FR-002 覆盖规则文件与 Skill 文件

摘要复用机制 MUST 同时覆盖：

- `AGENTS.md`、`openspec/project.md`；
- `rules/*.md` 中与当前任务相关的规则；
- 当前命令 Skill，例如 `.agents/skills/req-generate/SKILL.md`；
- 必要的共用技能，例如 `.agents/skills/workflow-sync/SKILL.md`。

命令执行时，若文件已在同一会话读取且无变化，AI SHOULD 用摘要承接，不重复全量读取。若只需确认特定字段或门禁，AI SHOULD 分段读取必要片段。

### FR-003 定义摘要失效条件

以下任一情况发生时，摘要 MUST 视为失效或需要补读：

- 文件内容、mtime、hash 或 `updated_at` 显示已变更；
- 用户显式要求重新读取或复核原文；
- 任务从轻量 capture/explore 升级为 apply/archive/release 等高风险命令；
- 涉及 OpenSpec 红线、权限、安全、API、DB、上传、Docker、发布等强门禁，而摘要不足以支撑判断；
- 上一次摘要无法覆盖当前命令的特定步骤或 Final Step；
- 出现 Workflow Sync、校验脚本或测试失败，需要回到原文定位。

### FR-004 统一命令 Skill 表述

命令 Skill 的 `Context Budget Guardrails` SHOULD 使用统一表述，至少表达：

- 遵守 `rules/agent-context-budget.md`；
- 同一会话已读且无变更的规则和 Skill 用摘要承接；
- 先定位再分段读取，不默认读取整目录；
- 大输出优先摘要、命中数、diff stat 或失败关键段；
- 对高风险命令必须补读当前 Change、Issue、Sprint 或 trace 的必要片段。

各命令 MAY 保留自己的 Must Read 和业务门禁，但不得要求默认宽泛读取整套规则、全部历史归档或生成物。

### FR-005 增强上下文预算校验

上下文预算校验脚本 SHOULD 增强对命令 Skill 的检查。

校验 SHOULD 覆盖：

- 是否引用 `rules/agent-context-budget.md`；
- 是否存在 `Context Budget Guardrails` 或等价章节；
- 是否包含“规则和 Skill 已读摘要复用”约束；
- 是否存在默认宽泛读取模式，例如 `cat rules/*.md`、`ls -R`、无边界 `rg <keyword> .`；
- 是否对大输出、generated 文件、archive 与 Harness/template assets 有排除或摘要策略。

校验失败时 SHOULD 输出具体文件与行号，方便维护者修正 Skill。

### FR-006 输出与追踪约束

命令执行过程中的用户可见输出 SHOULD 保持短摘要化。

当复用摘要时，AI MAY 简要说明：

```text
已复用同一会话中读取过的 AGENTS.md、rules/agent-context-budget.md 与 workflow-sync Skill 摘要；本次只补读 REQ trace 与目标 Skill 片段。
```

输出 MUST NOT 包含：

- 原始 prompt、系统/developer 指令或完整 session；
- 密钥、Cookie、Authorization、`.env` 内容；
- 大段规则或 Skill 全文；
- 不必要的完整测试日志、完整 Workflow Sync 派生块或 generated 文件 diff。

### FR-007 与 AI usage 事实源协同

本需求 SHOULD 与 REQ-0034/0035/0037 协同，但不重复实现 AI usage 事实源。

实现后，后续 Sprint 复盘可通过 AI usage 数据观察摘要复用机制是否降低以下高消耗来源：

- 连续命令重复读取 `AGENTS.md`、`rules/*.md`；
- 重复读取 `.agents/skills/*/SKILL.md` 全文；
- 宽泛搜索历史 archive、generated 文件或 Harness/template assets；
- 成功路径输出过长日志。

## 6. UI 约束

本需求不涉及 Web 管理端、店主 Web、小程序或可视化 UI。

若后续需要展示上下文预算统计，应另行创建需求，并遵守 Design System semantic token 与管理端权限边界。

## 7. 关联需求

| 关联项 | 关系 | 说明 |
|---|---|---|
| REQ-0034-ai-token-usage-observability | 父级/同域 | 已建立 AI Token 使用量观测方向，可作为本需求的治理背景。 |
| REQ-0035-ai-usage-snapshot-sprint-close-exps | 相关 | Sprint close / exps 会消费 usage snapshot，可用于观察预算优化效果。 |
| REQ-0037-auto-token-fact-source-for-workflow-commands | 相关 | 已将 post-command hook 纳入命令链，本需求避免 hook 和命令本身产生额外读取浪费。 |
| `rules/agent-context-budget.md` | 规则事实源 | 本需求的主要规则落点。 |
| `.agents/skills/*/SKILL.md` | 执行入口 | 命令 Skill 需要按统一模板表达摘要复用机制。 |
| `scripts/validate-agent-context-budget.py` | 校验入口 | 可扩展为 Skill 预算规则门禁。 |

## 8. 状态块

```yaml
status: done
lifecycle_stage: plan
iteration: null
openspec_changes: []
next: /req-opsx REQ-0040-rule-skill-read-summary-reuse-context-budget
```
