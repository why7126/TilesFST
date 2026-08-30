## MODIFIED Requirements

### Requirement: 工作流命令自动构建 AI usage 事实源
系统 MUST 为 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 工作流命令提供后置 AI usage fact source 构建流程，并在主命令和 Workflow Sync 成功后尝试生成或刷新脱敏使用量事实。对于 release 与 image 工作流命令，系统 MUST 提供等价的 post-command hook 归因规则，使发布版本与镜像构建命令可追踪。Hook 在未显式传入 session 文件时 MUST 先尝试自动发现本地 Codex session；默认发现目录为 `AI_USAGE_SESSIONS_DIR` 指定目录，未设置时为 `~/.codex/sessions/**/*.jsonl`。仅当自动发现失败、候选 session 不存在、候选缺少可归因 `token_count`，或需要历史回溯/审计的精确映射时，才要求用户显式提供 `--session-jsonl` 或设置 `AI_USAGE_SESSION_JSONL`。

#### Scenario: 主命令与 Workflow Sync 成功后触发
- **WHEN** 任一受支持工作流命令完成
- **AND** 主命令完成且 Workflow Sync 返回成功
- **THEN** 命令 MUST 运行统一 AI usage post-command hook 或报告明确跳过原因
- **AND** hook MUST 继承 workflow event、REQ、BUG、Change、Sprint 或 Release 上下文

#### Scenario: 默认发现本地 Codex sessions
- **WHEN** hook 未收到显式 `--session-jsonl`
- **AND** `AI_USAGE_SESSION_JSONL` 与 `CODEX_SESSION_JSONL` 均未设置
- **THEN** hook MUST 扫描 `AI_USAGE_SESSIONS_DIR` 或默认 `~/.codex/sessions/**/*.jsonl`
- **AND** hook MUST 使用 workflow event、Sprint、REQ、BUG、Change 或 Release 关键词选择候选 session
- **AND** 成功路径 MUST 输出 compact summary，且不得输出本机绝对 session 路径或原始 session 内容

#### Scenario: 自动发现失败后给出可执行补救动作
- **WHEN** hook 自动发现失败、候选文件不可读、缺少可归因 token_count 或需要历史回溯精确映射
- **THEN** hook MUST 输出 `usage_mode: unavailable` 或 `estimated_fallback` 的 compact warning
- **AND** recommended_action MUST 优先说明检查默认 sessions 目录、`AI_USAGE_SESSIONS_DIR`、`AI_USAGE_SESSION_JSONL` 或显式 `--session-jsonl`
- **AND** 命令输出 MUST NOT 简化为“本地 session 输入不可用所以无法做成本分析”

#### Scenario: AI usage hook 输出保持紧凑
- **WHEN** hook 完成、跳过或降级
- **THEN** successful output SHALL include only status, usage_mode, command_run_count, sprint_snapshot or release artifact summary, warning_count, and recommended_action.
- **AND** successful output SHALL stay compact and SHALL NOT print raw session content, prompts, local absolute paths, secrets, or full command-run JSON.
