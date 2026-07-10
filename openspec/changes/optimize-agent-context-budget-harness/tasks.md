# Tasks

- [x] 新增 `rules/agent-context-budget.md`，定义统一上下文预算、Harness 排除、生成物/diff 输出规则。
- [x] 更新 `AGENTS.md`，将 Agent 上下文预算纳入执行前读取路由与完成检查。
- [x] 更新 `.agents/skills/source-command-*`，统一引用上下文预算规则并保留命令特定边界。
- [x] 新增 `scripts/validate-agent-context-budget.py`，校验 source-command 技能是否遵守预算入口。
- [x] 新增 OpenSpec delta spec，记录 Agent 上下文预算治理能力。
- [x] 运行 OpenSpec、目录结构与 Agent 上下文预算校验。
