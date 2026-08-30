---
purpose: AI Usage session 默认发现治理日志
content: 记录将 ~/.codex/sessions 作为 AI Usage 默认 session 发现规范的治理变更
source: /spec-opt standardize-ai-usage-session-discovery
created_at: 2026-08-30 08:55:17
updated_at: 2026-08-30 08:55:17
---

# AI Usage session 默认发现治理日志

## 迭代目标

将本地 Codex sessions 目录作为 AI Usage 默认 session 发现规范，避免常规 workflow 命令在本机存在 session JSONL 时误报无法做成本分析。

## 变更摘要

- 明确 AI Usage hook 默认发现顺序：显式 `--session-jsonl`、`AI_USAGE_SESSION_JSONL`、`CODEX_SESSION_JSONL`、`AI_USAGE_SESSIONS_DIR`、`~/.codex/sessions/**/*.jsonl` 自动发现。
- 同步 `workflow-sync`、`sprint-archive`、`sprint-exps` 的 AI Usage 输出口径：常规命令先自动发现，失败或历史回溯时再要求显式 session 输入。
- 优化 AI Usage 脚本 recommended action，补充默认 sessions 目录和环境覆盖变量提示。
- 补充 OpenSpec delta、聚焦测试和 `data/ai-usage/README.md` 事实源说明。

## 影响范围

- 影响治理 Skill、上下文预算规则、AI Usage 脚本文案、测试、OpenSpec Change 和 Sprint 规划文档。
- 不影响业务 `src/` 运行时代码。
- 不影响 API、数据库、Web、小程序、管理端业务行为、Orval 或 Docker Compose。

## 更新文件

- `.agents/skills/workflow-sync/SKILL.md`
- `.agents/skills/sprint-archive/SKILL.md`
- `.agents/skills/sprint-exps/SKILL.md`
- `rules/agent-context-budget.md`
- `data/ai-usage/README.md`
- `scripts/ai_usage.py`
- `tests/test_ai_usage.py`
- `openspec/changes/standardize-ai-usage-session-discovery/`
- `iterations/change/sprint-028/`
- `docs/spec-logs/CHANGELOG.md`

## 关键决策

- 已采纳：默认扫描 `AI_USAGE_SESSIONS_DIR` 或 `~/.codex/sessions`，因为脚本已有安全关键词匹配与脱敏事实源写入边界。
- 已采纳：历史回溯仍要求显式 `--session-jsonl` 或 `--manual-map`，避免当前回溯会话被误选为历史 session。
- 未采纳：把真实 session 路径写入命令输出或长期文档；原因是本机绝对路径和原始 session 内容必须保持本地私有。

## 验证结果

- `python -m pytest tests/test_ai_usage.py`：36 passed。
- `python scripts/extract-ai-usage.py --post-command-hook --workflow-event explore --dry-run --json`：`usage_mode: actual`，`command_run_count: 1`。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `openspec validate standardize-ai-usage-session-discovery`：通过。
- `python scripts/validate-sprint-scope.py sprint-028 --item standardize-ai-usage-session-discovery`：通过。
- `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change standardize-ai-usage-session-discovery --sprint sprint-028 --json`：`usage_mode: actual`，刷新 `data/ai-usage/sprints/sprint-028.json`。
- `python scripts/validate-doc-prose-hygiene.py <focused-paths>`：通过，保留 7 条启发式 warning，均未阻断本次治理。

## 后续建议

若后续仍出现 estimated fallback，可优先检查默认 session 目录是否存在、候选 session 是否包含 `token_count`、workflow 关键词是否足以自动匹配；历史回溯继续使用显式 session 和 manual map。
