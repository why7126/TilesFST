# Design: 规则/Skill 已读摘要复用纳入上下文预算治理

## Context

现有 `rules/agent-context-budget.md` 已建立“先定位，再摘要，再片段读取”的原则，并要求同一会话已读且无变更的规则文件用摘要承接。各命令 Skill 也已经普遍引用该规则。

缺口在于该机制仍缺少可执行细节：

- 没有明确 `.agents/skills/*/SKILL.md` 是否和 `rules/` 一样可复用摘要；
- 没有定义摘要最小字段和失效条件；
- 命令 Skill 的 Guardrails 表述不完全统一；
- 校验脚本目前只检查规则引用、章节和宽泛读取模式，不能检查摘要复用约束是否回退。

REQ-0040 承接 `docs/knowledge-base/retrospectives/sprint-007-retrospective.md` 的行动项 A-004，目标是把摘要复用机制变成规则、Skill 和校验脚本共同执行的治理能力。

## Goals / Non-Goals

**Goals:**

- 明确同一会话内规则与 Skill 已读摘要复用的定义、适用范围和失效条件。
- 统一命令 Skill 的 `Context Budget Guardrails` 最小表述。
- 增强校验脚本，阻止命令 Skill 缺失摘要复用约束或回退到默认宽泛读取。
- 保持安全边界，不持久化原始 prompt、系统/developer 指令、工具输出正文、密钥、`.env` 或本地绝对路径。

**Non-Goals:**

- 不改造 Codex Desktop、模型 API 或底层上下文管理机制。
- 不设计跨会话强缓存或长期摘要数据库。
- 不重做 REQ-0034/0035/0037 的 AI usage 事实源、Sprint snapshot 或 post-command hook。
- 不新增 Web / 小程序 / 管理端 UI，不改 API、数据库或上传存储链路。

## Decisions

### D1. 摘要默认只作为同一会话上下文承接

摘要复用默认依赖当前对话上下文，不新增仓库内持久化摘要文件。规则中只定义可用于判断的最小字段，如 `path`、`version_hint`、`summary`、`applicability`、`refresh_reason`。

原因：当前需求关注减少连续命令重复读取，短期收益来自同一会话内承接；落盘摘要会引入脱敏、生命周期、清理和提交边界问题，应另行设计。

### D2. Skill 文件纳入摘要复用范围

规则明确 `AGENTS.md`、`openspec/project.md`、相关 `rules/*.md`、当前命令 Skill 和共用 Skill 均可在同一会话已读且无变更时用摘要承接。

原因：连续命令中 Skill 文件尤其容易重复读取，且它们往往包含相同的 Context Budget、Workflow Sync 与 AI usage hook 段落。

### D3. 高风险命令必须补读关键片段

摘要复用不能替代强门禁。规则要求当任务升级到 apply/archive/release，或涉及 OpenSpec 红线、权限、安全、API、DB、上传、Docker、发布等强门禁时，必须补读当前 Change、Issue、Sprint、trace、Final Step 或失败相关片段。

原因：上下文节省不能以漏读门禁为代价，摘要不足时必须回到证据片段。

### D4. 校验脚本检查摘要复用约束

`scripts/validate-agent-context-budget.py` 在现有规则引用与宽泛读取检查基础上，新增对“规则和 Skill 已读摘要复用”表述的检查。

原因：只有文档约束容易回退；脚本门禁能在后续 Skill 更新时及时暴露缺失。

## Risks / Trade-offs

- 摘要过度概括导致漏读细节 → 通过失效条件和高风险补读规则缓解。
- 校验脚本误判不同措辞 → 允许检查多个关键词组合或等价表述，并在失败输出中给出具体文件。
- Skill 批量更新带来噪音 → 使用统一短句模板，避免重写长段落。
- 未来跨会话复用需求出现 → 本 Change 明确不落盘；后续通过独立 REQ/Change 处理。

## Migration Plan

1. 更新 `rules/agent-context-budget.md`，增加“已读摘要复用”章节。
2. 更新命令 Skill 的 `Context Budget Guardrails`，使用统一表述覆盖规则和 Skill。
3. 增强 `scripts/validate-agent-context-budget.py` 的检查逻辑。
4. 运行 `python scripts/validate-agent-context-budget.py`。
5. 按需运行相关测试，确认脚本变更稳定。

## Open Questions

- 是否需要为跨会话摘要复用单独建立本地-only 缓存？本 Change 暂不处理。
- 校验脚本是否应自动给出建议补丁？本 Change 只要求报告文件与行号。
