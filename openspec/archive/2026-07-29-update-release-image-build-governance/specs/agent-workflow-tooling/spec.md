## MODIFIED Requirements

### Requirement: 工作流命令自动构建 AI usage 事实源
系统 MUST 为 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 工作流命令提供后置 AI usage fact source 构建流程，并在主命令和 Workflow Sync 成功后尝试生成或刷新脱敏使用量事实。对于 release 与 image 工作流命令，系统 MUST 提供等价的 post-command hook 归因规则，使发布版本与镜像构建命令可追踪。

#### Scenario: 主命令与 Workflow Sync 成功后触发
- **WHEN** `/req-*`、`/bug-*`、`/opsx-*` 或 `/sprint-*` 工作流命令完成
- **AND** 主命令完成且 Workflow Sync 返回成功
- **THEN** 系统 MUST 触发统一 AI usage fact source hook 或等价共享流程
- **AND** 系统 MUST 输出短摘要，包含 hook status、usage mode、warning 数量和 recommended action

#### Scenario: release 与 image 命令写入版本归因
- **WHEN** `/release-*` or `/image-*` workflow commands run with `--release vX.Y.Z` or `<version>`
- **THEN** their AI usage hook SHALL support release version attribution
- **AND** image command usage records SHALL be attributable to the release version and, when provided, the related image plan or manifest
- **AND** successful output SHALL stay compact and SHALL NOT print raw session content, prompts, local absolute paths, secrets, or full command-run JSON.

### Requirement: Release 命令 AI usage 版本级存储
系统 MUST 为 `/release-propose`、`/release-prepare`、`/release-publish` 提供版本级 AI usage artifact，避免 release 命令只散落在通用 command-runs 或被误归到单一 Sprint snapshot。系统 SHOULD 为 `/image-prepare` 与 `/image-build` 提供同一 release version 目录下的 AI usage artifact，避免镜像构建命令脱离发布版本事实源。

#### Scenario: release 命令写入版本目录
- **WHEN** release post-command hook 提供 `--release vX.Y.Z`
- **AND** hook 可安全解析本地 session 输入
- **THEN** 系统 MUST 写入 release command run 明细 `data/ai-usage/command-runs/releases/vX.Y.Z/<date>--<workflow-event>--<session-hash>.json`
- **AND** 系统 MUST 写入版本级 artifact `data/ai-usage/command-runs/releases/vX.Y.Z/<workflow-event>.json`
- **AND** `<workflow-event>` SHALL 为 `release.propose`、`release.prepare` 或 `release.publish`
- **AND** 版本级 artifact MUST 包含 `release_version`、`workflow_event`、`generated_at`、`coverage`、`totals` 和脱敏 command run 明细或等价安全摘要

#### Scenario: image 命令写入版本目录
- **WHEN** image post-command hook provides `--release vX.Y.Z` or equivalent release version context
- **AND** hook can safely parse local session input
- **THEN** the system SHOULD write image command run details under `data/ai-usage/command-runs/releases/vX.Y.Z/`
- **AND** `<workflow-event>` SHOULD be `image.prepare` or `image.build`
- **AND** the version-level artifact SHOULD include release_version, workflow_event, generated_at, coverage, totals, image_plan or image_manifest summary, and safe command run details.

### Requirement: 工作流成功路径紧凑输出契约
系统 MUST 为 Workflow Sync 与 AI usage post-command hook 建立统一 compact summary 输出契约，使工作流命令成功路径默认只输出聚合状态、关键上下文和推荐动作。Image 命令成功路径 SHALL follow the same compact-output contract and summarize plan/manifest paths, gate status, blocker count, and next command instead of printing full Docker logs or full manifest JSON.

#### Scenario: Workflow Sync 默认成功摘要
- **WHEN** Workflow Sync succeeds
- **THEN** 系统 MUST 默认输出 Workflow Sync Report 摘要

#### Scenario: AI usage hook 输出固定摘要字段
- **WHEN** 工作流命令在 Workflow Sync 成功后执行 AI usage post-command hook
- **THEN** hook output SHALL use a compact summary
- **AND** compact summary MUST 包含 `status`、`usage_mode`、`command_run_count`、`sprint_snapshot`、`warning_count` 和 `recommended_action`
- **AND** 系统 MUST NOT 默认打印完整 session、原始 prompt、系统指令、developer 指令、技能全文、工具输出正文、完整 snapshot JSON 或完整 command run 明细

#### Scenario: image 命令成功输出摘要
- **WHEN** `/image-prepare` or `/image-build` succeeds or records blockers
- **THEN** command output SHALL summarize version, image_required, plan path, manifest path when present, gate status, blocker count, validation summary, and next command
- **AND** it SHALL NOT print full Docker build logs, full tarball contents, full image manifest JSON, raw env files, or secrets on the success path.

### Requirement: 命令 Skill 摘要复用 Guardrails
命令 Skill MUST 在 `Context Budget Guardrails` 或等价章节中表达规则与 Skill 已读摘要复用约束，并保留命令特定门禁。新增或更新 image 命令 Skill SHALL follow the same guardrails and SHALL read release and image artifacts by targeted path rather than scanning all releases or archives.

#### Scenario: 命令 Skill 使用统一预算表述
- **WHEN** 新增或更新 `.agents/skills/{req,bug,opsx,sprint,build}-*`、`.agents/skills/capture`、`.agents/skills/initialize-project` 或 release 命令 Skill
- **THEN** Skill MUST 引用 `rules/agent-context-budget.md`
- **AND** Skill SHOULD 明确同一会话已读且无变更的规则和 Skill 用摘要承接
- **AND** Skill MUST 保留命令特定 Must Read、Workflow Sync、AI usage hook 和业务门禁

#### Scenario: image 命令 Skill 控制读取范围
- **WHEN** `/image-prepare` or `/image-build` Skill is added or updated
- **THEN** the Skill SHALL read `releases/<version>/release.json`, image plan or manifest, targeted Dockerfile, Compose, build script, env example, schema, and migration inputs
- **AND** it SHALL NOT default to reading all `releases/**`, all `openspec/archive/**`, generated OpenAPI clients, full Docker logs, or raw env files.
