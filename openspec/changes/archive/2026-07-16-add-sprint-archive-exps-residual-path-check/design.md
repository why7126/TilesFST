# Design: Sprint 归档与复盘旧路径残留检查

## Context

当前 Sprint 生命周期要求 `/sprint-archive` 将 `iterations/change/<sprint-id>/` 迁移到 `iterations/archive/<sprint-id>/`，并要求工具通过 `resolve_sprint_dir()` 解析 change/archive 两阶段路径。Change 归档后也会从 `openspec/changes/<change-id>/` 迁移到 `openspec/changes/archive/<date>-<change-id>/`。

现有 readiness、Workflow Sync 与 Fact Sheet 已能处理 Sprint/Change 状态、归档证据和上下文预算，但没有专门检查关联文档中是否仍保留旧路径引用。该缺口会让 `sprint.md`、`acceptance-report.md`、`release-note.md`、复盘文档或 Issue/Change trace 留下过期链接，读者点击后看到不存在或错误阶段的路径。

## Goals / Non-Goals

**Goals:**

- 在 `/sprint-archive` 成功迁移和同步后，检查本 Sprint 关联文档是否残留旧路径引用。
- 在 `/sprint-exps` 生成复盘前，通过 Fact Sheet 或专用检查暴露旧路径残留，避免复盘继续传播旧链接。
- 检查范围以 Sprint scope 为边界，覆盖 Sprint 四件套、关联 Issue 文档、关联 Change 文档和复盘输出目标，不扫描整个历史归档。
- 报告必须提供旧路径、新路径、文件位置和建议修正动作。

**Non-Goals:**

- 不改变 Sprint、Issue、OpenSpec Change 的生命周期状态机。
- 不改变 `resolve_sprint_dir()` 对遗留扁平路径的兼容读取能力。
- 不自动重写所有历史归档文档；本变更只要求当前命令范围内检查与必要修复。
- 不影响业务 API、数据库、Web、小程序、管理端权限或 Docker 配置。

## Decisions

### 1. 新增可复用残留检查脚本

新增 `scripts/check-archived-path-residuals.py` 或等价模块，以 `--sprint <sprint-id>` 为入口解析 Sprint scope。脚本应复用现有路径解析能力，生成：

- 旧 Sprint 路径：`iterations/change/<sprint-id>/`
- 新 Sprint 路径：`iterations/archive/<sprint-id>/`
- 每个已归档 Change 的旧路径：`openspec/changes/<change-id>/`
- 每个已归档 Change 的新路径：`openspec/changes/archive/<date>-<change-id>/`

备选方案是把逻辑塞进 `generate-sprint-fact-sheet.py` 或 workflow sync。独立脚本更适合被 `/sprint-archive` 和 `/sprint-exps` 同时复用，也便于 dry-run、测试和失败摘要输出。

### 2. 检查范围由 Sprint scope 驱动

脚本从 `sprint.yaml` 读取 `requirements[]`、`bugs[]`、`changes[]`，只扫描这些对象的相关 Markdown 文档和 Sprint 四件套。默认排除 `node_modules`、`dist`、`coverage`、Orval generated、OpenAPI 大文件和无关 archive 目录。

该策略符合 `rules/agent-context-budget.md`：先由机器事实源定位，再读取必要文件，不用全仓库 `rg` 找路径字符串。

### 3. `/sprint-archive` 将残留作为关闭后门禁

Sprint 目录移动、Workflow Sync 和 issue promote 成功后，命令必须运行残留检查。若发现旧路径残留：

- 默认阻断最终成功报告，提示修复旧链接后重跑检查。
- 报告列出文件、行号、旧路径、新路径和建议命令。
- 若命令后续实现提供 `--apply` 自动修复，必须只替换精确匹配的仓库相对路径，不处理自由文本猜测。

### 4. `/sprint-exps` 将残留作为复盘风险输入

`/sprint-exps` 在 Fact Sheet 之后、写入复盘文档之前运行残留检查。若发现残留：

- Experience Analysis Report 必须展示 residual path warning。
- 复盘文档不得把旧路径作为证据链接继续写入。
- Fact Sheet 或 evidence hints 应包含残留文件路径，方便人工定位。

## Risks / Trade-offs

- [Risk] 路径字符串可能出现在代码块或历史说明中，不一定是链接错误 → Mitigation：报告中区分 Markdown 链接、反引号路径和普通文本；自动修复仅处理精确仓库相对路径。
- [Risk] 已归档 Change 目录带日期前缀，需要解析匹配 → Mitigation：复用现有 `find_archived_change_dir()` 逻辑或抽取共享 helper。
- [Risk] 检查过宽导致 token 和输出膨胀 → Mitigation：脚本输出聚合摘要，失败时只列命中文件与命中行；读取范围限定为 Sprint scope。
- [Risk] 老文档可能合法引用历史迁移前路径 → Mitigation：默认以 warning/blocker 报告，由命令层按当前 Sprint 是否正在归档决定是否阻断。

## Migration Plan

1. 新增残留检查脚本及单元测试，覆盖无残留、Sprint change 路径残留、active Change 路径残留、已归档 Change 日期路径解析。
2. 更新 `/sprint-archive` 技能，在 close/sync/promote 后运行检查，并将结果写入最终报告。
3. 更新 `/sprint-exps` 技能，在 Fact Sheet 之后运行检查，并把 warning 纳入复盘输入。
4. 如需要，扩展 `generate-sprint-fact-sheet.py` 的 JSON 输出，将 residual path warning 暴露给复盘命令。

## Open Questions

- 是否需要在第一版提供 `--apply` 自动修复，还是只提供 dry-run 检查与人工修复建议？建议第一版先提供检查，若测试覆盖充分再加入精确替换模式。
