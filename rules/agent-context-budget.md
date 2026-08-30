---
purpose: Agent上下文预算治理
content: 约束AI读取范围、搜索排除、Harness/模板工程噪音、生成物与大输出处理
source: BUG-0061会话token复盘后由AI生成，项目团队Review
update_method: Agent工作流、Harness模板、技能命令或上下文预算策略变化时更新
created_at: 2026-07-08 09:26:36
updated_at: 2026-08-30 15:36:34
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
- 不默认全量读取 `docs/**`、`issues/**`、`iterations/**`、`openspec/specs/**`、`openspec/archive/**`、legacy `openspec/changes/archive/**`。

AI 执行任务时 MUST NOT：

- 默认运行 `cat rules/*.md`、`cat docs/**`、`ls -R` 或无边界 `rg <keyword> .`。
- 为确认一个字段或状态读取整个目录或整个历史归档。
- 在成功路径中输出完整测试日志、完整 Workflow Sync 派生块或完整 generated 文件。

## 2.1 已读摘要复用

同一会话中，AI 已经读取过且无变更的规则和 Skill 文件 SHOULD 用摘要承接，避免重复全量展开。适用范围包括：

- `AGENTS.md`、`openspec/project.md`。
- 当前任务相关的 `rules/*.md`。
- 当前命令 Skill、共用 Skill（如 `.agents/skills/workflow-sync/SKILL.md`）以及 `.agents/skills/{req,bug,opsx,sprint,release,image,build}-*`、`.agents/skills/capture`、`.agents/skills/spec-opt`、`.agents/skills/initialize-project`。

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

## 2.2 引导式反馈契约

当命令需要用户选择、确认、补充信息或处理阻塞时，MUST 采用引导式反馈：

- 优先使用原生交互卡片组织问题；当客户端或工具层不支持原生交互卡片时，MUST 先说明降级原因，再降级为文本结构化选项。
- 两种形态都必须包含结构化选项、推荐项和可补充说明入口；不得用大段开放式追问替代。
- 每轮只聚焦 1-3 个关键决策；每个决策点 SHOULD 给出 2-4 个互斥选项。
- 至少一个选项 MUST 标注“推荐”，并说明推荐理由或适用前提。
- 用户已回答的决策 MUST 在后续输出中承接并动态收敛，只追问剩余阻塞点或新增风险点。
- 无需用户反馈的成功路径 SHOULD 保持紧凑，不为了套用格式追加无意义问卷。

## 3. 默认搜索排除

大范围搜索和文件清单默认排除：

```text
--glob '!pm-harness*/**'
--glob '!**/assets/**'
--glob '!**/.git/**'
--glob '!**/node_modules/**'
--glob '!**/dist/**'
--glob '!**/coverage/**'
--glob '!openspec/archive/**'
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

`.agents/skills/*/SKILL.md` 命令技能 MUST：

- 在 `Context Budget Guardrails` 或等价章节中引用本文件。
- 保留命令特定的 Must Read 与业务门禁，但不得要求默认宽泛读取整目录。
- 对 apply/archive/sprint 类高消耗命令，明确要求先读取 OpenSpec CLI `contextFiles`、任务文件、trace/status 片段，再按需扩展。
- 对 `/opsx-apply` 命令，MUST 明确所有 Change 都必须先纳入 Sprint，禁止恢复“无 REQ/BUG 来源或纯治理 Change 可跳过 Sprint Inclusion Gate”的豁免。
- 对下一步命令输出，MUST 明确 REQ 来源链路使用原始 `REQ-*`，BUG 来源链路使用原始 `BUG-*`；REQ/BUG 来源的后续 `/opsx-apply`、`/opsx-archive` 不得回退为真实 Change ID，非 REQ/BUG Change 才使用真实 Change ID。
- 对 `/spec-opt` 规范优化命令，MUST 明确只修改治理资产，覆盖 `.agents/skills`、`rules/`、`docs/`、`scripts/`、`AGENTS.md` 和 active OpenSpec Change 的同步矩阵，并禁止修改业务 `src/`。
- 对 `/bug-review` 命令，MUST 明确默认 approve 或显式 `--approve` 前运行根因 confirmed 门禁；`root_cause_status` 非 `confirmed`、缺少 `root-cause.md` 或缺少根因状态时不得 approve。
- 对 `/spec-study` 跨项目 Harness 学习应用命令，MUST 明确先学习并输出候选内容、等待用户确认后再应用；学习范围 MUST 横向覆盖项目入口、`rules/`、`docs/`、多 Agent 目录、`scripts/`、部署与环境示例；学习对象 MUST 全程只读且绝不允许被改动；应用阶段 MUST 遵守 active OpenSpec Change 与 Sprint Inclusion Gate，并禁止修改业务 `src/`；同一次学习应用流程只生成一份正式学习报告，学习报告 MUST 统一写入 `docs/spec-logs/YYYYMMDDhhmmss-study-xxx.md`，并承载本次学习触发的治理资产应用结果；不得额外生成内容重复的 `YYYYMMDDhhmmss-governance-xxx.md`，且不得包含用户隐私数据、真实客户数据、密钥、访问令牌、本机绝对路径、未脱敏日志、订单原文、聊天原文、工单原文、截图中的个人信息或学习对象源码；涉及路径证据时 MUST 使用仓库相对路径或 `<local-project>`、`<user-home>` 等脱敏占位符。
- 对 `/spec-study` 跨项目 Harness 学习，若学习对象存在 `docs/spec-logs/CHANGELOG.md`，MUST 日志优先：先读治理变更历史总账，再按主题读取相关单次 `study` / `governance` 日志，再横向校验真实治理资产，最后仅在证据不足时补读脚本或配置片段；日志只作为入口地图，不替代当前资产事实源。
- 对新增或高频命令技能，MUST 明确引导式反馈契约；需要用户决策时优先使用原生交互卡片，无法支持时降级为文本结构化选项。
- 对 AI usage post-command hook，MUST 明确默认 session 发现顺序：显式 `--session-jsonl`、`AI_USAGE_SESSION_JSONL`、`CODEX_SESSION_JSONL`、`AI_USAGE_SESSIONS_DIR`、`~/.codex/sessions/**/*.jsonl` 自动发现；常规 workflow 命令不得在尝试默认发现前声称无法做成本分析，历史回溯或自动发现失败时再要求显式 session 输入。
- 对发布命令族，MUST 从 `releases/<version>/release.json`、`announcement.mdx`、`image-build-plan.json`、`image-manifest.json`、`upgrade-plans/`、Web / 小程序 `PRODUCT_VERSION` 源和 validator 摘要定位当前状态；不得为了确认 usage docs、公告、镜像或升级状态全量展开历史 Sprint、Issue、Change 或 `releases/**`。命令输出 MUST 回显发布目标环境、usage docs、公开公告和镜像构建四类发布决策摘要，并将阻塞项按 `decision_missing`、`prepare_evidence_missing`、`publish_evidence_missing`、`production_only_pending`、`input_drift`、`environment_unavailable`、`scope_incomplete`、`public_safety`、`schema_invalid` 分类写成可执行修复路径。产品版本号不一致归类为 `prepare_evidence_missing`，修复后必须重跑 `/image-prepare <version>` 与 `/image-build <version>`。开发环境发布不得把生产 env、生产备份、生产 no-fallback/API/smoke 证据作为阻塞项；生产发布必须单独读取和校验生产门禁证据。`/release-status` 是只读状态面板入口，应用于用户需要理解当前阶段、默认 upgrade 路径和下一步时。
- 对 `/opsx-archive`、`/sprint-archive`、`/release-status` 和 `/release-publish`，MUST 通过 `scripts/validate-environment-tiered-evidence.py` 或已接入该模块的上层 validator 执行环境分层 evidence 门禁，阻断开发证据冒充生产、体验版 / 真机 Network 无证据却标 passed，以及生产发布前未重新判定的 `production_only_pending`。
- 对 `/git-check` 推送前安全检测命令，MUST 默认扫描 staged、modified tracked 和 untracked 文件，检测真实环境文件、运行时数据、数据库、大文件、密钥/Token/连接串、本机绝对路径和不应进入 Git 的本地数据；`--all` 可用于深度扫描全仓当前文件；输出必须脱敏，且不得自动删除文件、修改 `.gitignore` 或 unstage。
- 对 `/spec-opt` 规范优化命令，MUST 在完成本项目规范、技能、脚本、目录边界或校验规则迭代后写入 `docs/spec-logs/YYYYMMDDhhmmss-governance-xxx.md` 治理迭代日志，且不得包含用户隐私数据、真实客户数据、密钥、访问令牌、未脱敏日志、订单原文、聊天原文、工单原文、截图中的个人信息或学习对象源码。
- 在最终输出契约中区分「下一步」与「待用户决策/处理」：技能文件不得提供可被原样输出的尖括号占位模板或与当前命令无关的通用示例；已在「下一步」中给出的命令或动作不得重复写入「待用户决策/处理」；后者只列缺失输入、范围/策略选择、证据补充、验收/发布确认、生产实施确认、阻塞项或人工处理事项，没有则写“无”。

## 8. 校验

本地校验命令：

```bash
python scripts/validate-agent-context-budget.py
```

该脚本用于检查命令技能是否引用本规则，并阻止常见宽泛读取、最终输出占位模板、通用示例、重复诱因和规范语气泄漏风险回退。
