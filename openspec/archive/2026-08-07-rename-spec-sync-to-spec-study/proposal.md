## 背景

`spec-sync` 的职责是学习其他项目 Harness 工程并在用户确认后应用到本项目治理资产，但 “sync” 容易让人误解为直接同步或复制。为强调先学习、后确认、再应用的工作方式，需要将命令改名为 `spec-study`。

## 变更内容

- 将 `.agents/skills/spec-sync/` 重命名为 `.agents/skills/spec-study/`。
- 将用户命令从 `/spec-sync` 调整为 `/spec-study`。
- 将 `/spec-study` 学习报告统一放在 `docs/spec-logs/YYYYMMDD-xxx.md`。
- 同步 `AGENTS.md`、`rules/agent-context-budget.md`、校验脚本、Sprint 文档和正式 OpenSpec spec 中的命名。
- 保留原有能力边界：学习对象只读、应用前用户确认、应用阶段禁止修改 `src/`。

## 能力

### 新增能力

- 无。

### 修改能力

- `agent-workflow-tooling`：将 Harness 学习同步技能命名从 `/spec-sync` 调整为 `/spec-study`。

## 影响

- 影响 `.agents/skills/spec-study/SKILL.md`、`AGENTS.md`、`rules/agent-context-budget.md`、`rules/directory-structure.md`、`docs/README.md`、`docs/spec-logs/README.md`、`scripts/validate-agent-context-budget.py`、`openspec/specs/agent-workflow-tooling/spec.md`、`iterations/archive/sprint-022/` 与本 Change 文档。
- 不影响后端 API、数据库、Web、小程序、管理端业务实现。
- 不需要 Orval。
- 不需要 Docker Compose 验证。
