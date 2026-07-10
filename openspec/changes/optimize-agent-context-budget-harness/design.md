# Design: Agent 上下文预算与 Harness 噪音治理

## 设计原则

1. 统一规则入口：新增 `rules/agent-context-budget.md`，避免每个技能复制一大段守则。
2. 技能轻引用：source-command 技能只需声明必须遵守统一规则，并保留命令特有的读取边界。
3. 默认排除高噪音：Harness/模板工程/历史 agent 目录、生成物、构建产物、归档目录默认不进入搜索面。
4. 大输出先汇总后展开：先输出文件清单、命中数、diff stat 或失败摘要，再读取具体片段。
5. 可校验：新增 `scripts/validate-agent-context-budget.py`，检查技能是否引用统一规则、是否保留常见禁止模式。

## 影响范围

- `AGENTS.md`：在执行前读取路由与完成检查中加入 Agent 上下文预算规则。
- `rules/agent-context-budget.md`：新增项目级规则。
- `.agents/skills/source-command-*`：统一引用上下文预算规则，并补强关键命令的输出/排除要求。
- `scripts/validate-agent-context-budget.py`：新增只读校验脚本。
- `openspec/changes/optimize-agent-context-budget-harness/`：记录本次治理变更。

## 关键策略

### 搜索排除默认值

默认大范围 `rg/find` 应排除：

```text
pm-harness*/**
**/assets/**
**/.git/**
**/node_modules/**
**/dist/**
**/coverage/**
openspec/changes/archive/**
src/web/openapi.json
src/web/src/shared/api/generated.ts
src/web/src/generated/**
.claude/**
.codex/**
.cursor/**
.kiro/**
.opencode/**
```

如任务明确分析 Harness、生成物或历史归档，可放开，但必须先说明原因，并优先读取清单或片段。

### diff 与生成物

- 默认使用 `git diff --stat`、`git diff --name-only` 或 `git diff -- <focused-files>`。
- 禁止默认展开 `src/web/openapi.json` 与 Orval 生成文件全文 diff。
- Orval/OpenAPI 只需说明“已生成/有变化”，必要时读取 schema 相关片段。

### Workflow Sync / 测试输出

- 成功时只保留 report 摘要。
- 失败时读取失败段落、命名文件或具体 marker，而不是全量重跑大输出。

## 验收

- `openspec validate optimize-agent-context-budget-harness --strict` 通过。
- `python scripts/validate-agent-context-budget.py` 通过。
- `python scripts/validate-directory-structure.py` 通过。
