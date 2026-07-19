---
purpose: Agent上下文预算治理
content: 约束AI读取范围、搜索排除、Harness/模板工程噪音、生成物与大输出处理
source: BUG-0061会话token复盘后由AI生成，项目团队Review
update_method: Agent工作流、Harness模板、技能命令或上下文预算策略变化时更新
created_at: 2026-07-08 09:26:36
updated_at: 2026-07-16 09:28:05
note: 所有命令技能与普通开发任务均应遵守，优先级高于单个技能中的宽泛读取建议
---

# Agent 上下文预算治理

## 1. 目标

降低 AI 在需求、BUG、Sprint、OpenSpec 与 Harness 相关任务中的无效 token 消耗，避免重复读取大规则、大目录、历史归档、生成物和模板工程资产。

核心原则：先定位，再摘要，再片段读取；只有证据不足或任务明确要求时才扩大范围。

## 2. 默认读取边界

AI 执行任务时 MUST：

- 已在同一会话读取过且无变更的规则文件，用摘要承接，不重复全量读取。
- 先用 `rg -l`、`rg --files`、`find ... -maxdepth`、`git diff --name-only` 或 `git diff --stat` 定位，再读取必要片段。
- 对 Markdown、Spec、代码文件优先使用 `sed -n '<start>,<end>p'` 或 `nl -ba ... | sed -n` 分段读取。
- 命令输出默认控制在 `max_output_tokens <= 8000`；预期更大时先输出文件清单、命中数、失败摘要或 diff stat。
- 不默认全量读取 `docs/**`、`issues/**`、`iterations/**`、`openspec/specs/**`、`openspec/changes/archive/**`。

AI 执行任务时 MUST NOT：

- 默认运行 `cat rules/*.md`、`cat docs/**`、`ls -R` 或无边界 `rg <keyword> .`。
- 为确认一个字段或状态读取整个目录或整个历史归档。
- 在成功路径中输出完整测试日志、完整 Workflow Sync 派生块或完整 generated 文件。

## 2.1 已读摘要复用

同一会话中，AI 已经读取过且无变更的规则和 Skill 文件 SHOULD 用摘要承接，避免重复全量展开。适用范围包括：

- `AGENTS.md`、`openspec/project.md`。
- 当前任务相关的 `rules/*.md`。
- 当前命令 Skill、共用 Skill（如 `.agents/skills/workflow-sync/SKILL.md`）以及 `.agents/skills/{req,bug,opsx,sprint,release,build}-*`、`.agents/skills/capture`、`.agents/skills/initialize-project`。

可复用摘要 SHOULD 至少表达以下信息，字段名可等价：

```yaml
path: <规则或 Skill 路径>
version_hint: <updated_at、mtime、hash 或本会话已读时间线索>
summary: <与当前任务相关的规则、步骤和门禁摘要>
applicability: <本摘要适用的命令、阶段或风险范围>
refresh_reason: <本次继续复用或需要补读的原因>
```

摘要默认只存在于同一对话上下文中，MUST NOT 写入仓库或持久化原始 prompt、系统/developer 指令、完整 session JSONL、工具输出正文、密钥、Cookie、Authorization header、`.env` 内容或真实客户数据。

以下情况 MUST 补读目标文件或必要片段，不能仅凭旧摘要继续执行：

- 文件内容、mtime、hash、`updated_at` 或等价版本线索显示已变化。
- 用户明确要求重新读取、复核原文或引用精确文本。
- 当前命令从 capture、explore、generate 等轻量阶段升级到 apply、archive、release、req-opsx、bug-opsx、sprint-propose 等高风险阶段。
- 当前任务涉及 OpenSpec 红线、Issue lifecycle、权限、安全、API、DB、上传、Docker、发布、Workflow Sync Final Step 或 AI usage hook。
- 摘要不足以覆盖当前门禁，或 Workflow Sync、测试、校验脚本、OpenSpec CLI 返回失败。

成功路径输出 SHOULD 保持紧凑，只报告摘要复用状态、补读片段、计数、warning 或 recommended action；不得默认转述完整规则、完整 Skill、完整测试日志、完整 Workflow Sync 派生块或完整 generated diff。

## 3. 默认搜索排除

大范围搜索和文件清单默认排除：

```text
--glob '!pm-harness*/**'
--glob '!**/assets/**'
--glob '!**/.git/**'
--glob '!**/node_modules/**'
--glob '!**/dist/**'
--glob '!**/coverage/**'
--glob '!openspec/changes/archive/**'
--glob '!src/web/openapi.json'
--glob '!src/web/src/shared/api/generated.ts'
--glob '!src/web/src/generated/**'
--glob '!.claude/**'
--glob '!.codex/**'
--glob '!.cursor/**'
--glob '!.kiro/**'
--glob '!.opencode/**'
```

如当前任务明确要求分析 Harness、模板工程、agent 资产、历史归档或生成物，MAY 放开对应排除项，但 MUST 先说明原因，并优先输出清单或命中数。

## 4. Harness 与模板工程

- `pm-harness*/`、Harness 模板 assets、历史 agent 目录默认视为高噪音上下文。
- 非 Harness 任务不得读取 Harness 模板资产全文。
- 需要清理或校验 Harness 资产时，先限定具体路径与文件类型，再分段读取。
- 不应把长脚本、长批准命令或模板资产内容复制进技能文件；应引用脚本路径或规则文档。

## 5. OpenAPI、Orval 与生成物

API 变更仍 MUST 同步 OpenAPI / Orval / docs / tests，但复核方式应节制：

- 默认使用 `git diff --stat`、`git diff --name-only` 或目标 schema 片段。
- 不默认输出 `src/web/openapi.json` 全文或完整 diff。
- 不默认输出 `src/web/src/shared/api/generated.ts` 全文或完整 diff。
- 需要确认生成类型时，只读取相关接口、Schema 或导出函数片段。

## 6. Git Diff 与测试输出

- 普通复核优先 `git diff --stat` 与 `git diff -- <focused-files>`。
- 大 diff 先看文件列表；只对手写源码、文档或任务文件展开必要片段。
- 测试通过时只报告命令与摘要；测试失败时只展开失败用例、堆栈关键段和相关文件片段。
- Workflow Sync 成功时只报告 Workflow Sync Report 摘要；失败时按报告定位具体 marker 或文件片段。

## 7. 技能文件要求

`.agents/skills/{req,bug,opsx,sprint,build}-*`、`.agents/skills/capture`、`.agents/skills/initialize-project` 命令技能 MUST：

- 在 `Context Budget Guardrails` 或等价章节中引用本文件。
- 保留命令特定的 Must Read 与业务门禁，但不得要求默认宽泛读取整目录。
- 对 apply/archive/sprint 类高消耗命令，明确要求先读取 OpenSpec CLI `contextFiles`、任务文件、trace/status 片段，再按需扩展。

## 8. 校验

本地校验命令：

```bash
python scripts/validate-agent-context-budget.py
```

该脚本用于检查命令技能是否引用本规则，并阻止常见宽泛读取模式回退。
