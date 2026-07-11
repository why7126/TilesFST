## Context

`/sprint-exps` 当前要求读取 Sprint 四件套、全部 REQ/BUG/Change trace、review/root-cause/tasks，再由模型整理 Sprint Fact Sheet 与 Token Usage Fact Sheet。Sprint 005 已暴露出这一流程的 token 成本：仅 Sprint 三份长文档就超过千行，另有 10 个 Change 与 10 个 Issue 包需要人工筛读。

项目已经具备可复用基础：

- `scripts/workflow_sync/collect.py` 能解析 Sprint、Issue、Change、archive 路径、trace 状态与 tasks 计数。
- `scripts/validate-sprint-archive-readiness.py` 能生成 Sprint Change readiness 与 tasks 完成度摘要。
- `rules/agent-context-budget.md` 已规定先定位、再摘要、再片段读取，避免宽泛读取 archive 与 generated 文件。

这次变更将自动 Fact Sheet 前置为 `/sprint-exps` 的入口，而不是复盘完成后的副产物。

## Goals / Non-Goals

**Goals:**

- 为指定 Sprint 自动生成短小、可审计、可复用的 Fact Sheet。
- 将 Sprint 四件套、Issue/Change trace、tasks 与验收事实汇总成模型优先读取的摘要入口。
- 标记缺失、不一致、需要回读原文的风险项，避免模型默认全文展开长文档。
- 支持 Markdown 输出供人工阅读，并支持 JSON 输出供脚本或测试复用。
- 更新 `/sprint-exps` 技能，使其优先读取 Fact Sheet，再按风险项回读局部证据。

**Non-Goals:**

- 不改变 Sprint、Issue、OpenSpec 的生命周期状态机。
- 不替代 `sprint.yaml`、`trace.md`、`tasks.md` 或 acceptance report 的事实源地位。
- 不修改业务 API、数据库、Web、小程序、管理端业务逻辑。
- 不采集或伪造真实 token 计量；无法获得精确 token 时仍按现有规则标注估算。

## Decisions

### 1. 新增独立生成脚本

新增 `scripts/generate-sprint-fact-sheet.py`，输入 `--sprint <sprint-id>`，输出默认 Markdown，可通过 `--json` 输出机器可读结构。

原因：

- `/sprint-exps` 是技能文件，适合定义读取策略；事实收集应由脚本完成，便于测试与复用。
- 独立脚本可被 `/sprint-archive`、未来 CI 或人工命令调用，而不绑定单次模型会话。

替代方案：

- 只在 `source-command-sprint-exps/SKILL.md` 中写更细读取规则。缺点是仍让模型承担聚合工作，不能稳定降低输入 token。
- 扩展 `validate-sprint-archive-readiness.py`。缺点是 readiness gate 只关注归档阻断项，Fact Sheet 需要覆盖复盘与 token 风险，职责更宽。

### 2. 复用 workflow_sync 收集逻辑

Fact Sheet 生成应优先复用 `scripts/workflow_sync/collect.py` 的路径解析、Issue/Change 解析与 tasks 计数；必要时只增加小型 helper，不复制一套 YAML/trace/archive 解析。

原因：

- 避免 Sprint lifecycle、Issue stage、archive 目录匹配规则在多个脚本中漂移。
- Workflow Sync 已经是当前工作流状态派生的事实入口，Fact Sheet 应和它保持一致。

### 3. Fact Sheet 既输出事实，也输出回读建议

Markdown 输出建议包含：

- Sprint 基础信息：状态、生命周期路径、周期、容量、估算。
- Scope 汇总：REQ、BUG、Change 数量与列表。
- Change 表：位置、archive 目录、tasks 完成度、关联 REQ/BUG、trace 是否存在。
- Issue 表：目录阶段、trace 状态、关联 Change 状态、子文档状态残留风险。
- 验收摘要：acceptance report 的最终结论、归档时间、未闭环或历史未勾选提示。
- Token 风险：长文档行数、Change 数、tasks 总数、archive 回读风险、建议先读/后读清单。
- Evidence Hints：需要模型回读的具体文件路径和章节/关键词。

原因：

- 复盘仍需要判断和叙事，但模型应从聚合事实开始，而不是从原始长文档开始。
- Evidence Hints 能保留可追溯性，避免摘要变成不可审计的二手信息。

### 4. `/sprint-exps` 优先读取 Fact Sheet

技能流程改为：

1. 解析 Sprint id。
2. 运行或读取 Fact Sheet。
3. 优先基于 Fact Sheet 生成复盘分析。
4. 对 Fact Sheet 标记的缺失、不一致或高风险项，按 Evidence Hints 回读原文片段。

原因：

- 这直接落实 `rules/agent-context-budget.md` 的先摘要后片段读取。
- 对大 Sprint 的收益最明显，且小 Sprint 仍保留直接证据回读能力。

## Risks / Trade-offs

- [Risk] Fact Sheet 摘要遗漏重要语境 → Mitigation: 输出 Evidence Hints，并要求风险项触发局部回读。
- [Risk] 复用 `workflow_sync.collect` 时 helper 边界不清 → Mitigation: 只抽取只读收集函数，不让 Fact Sheet 脚本写 workflow-sync marker。
- [Risk] Markdown 输出过长又形成新 token 压力 → Mitigation: 默认输出聚合表与计数，详细原文只给路径和关键词；必要时提供 `--max-items` 或摘要截断。
- [Risk] 已归档历史 Sprint 文档格式不一致 → Mitigation: 对缺失字段输出 warning，不因非关键字段缺失而失败；对缺少 `sprint.yaml`、无 Change 列表等关键问题返回非零。
- [Risk] JSON 与 Markdown 双输出维护成本增加 → Mitigation: 先构建一个内部结构，再由 renderer 输出两种格式。

## Migration Plan

1. 新增 Fact Sheet 生成脚本并复用现有收集器。
2. 用 `sprint-005` 验证 Markdown / JSON 输出能覆盖 Sprint 005 复盘 A-004 的事实需求。
3. 更新 `/sprint-exps` 技能，要求先运行或读取 Fact Sheet。
4. 增加脚本测试或轻量命令验证。

回滚方式：若脚本输出不可信，可暂时恢复 `/sprint-exps` 原有人工读取路径；Fact Sheet 文件不作为唯一事实源，不影响业务运行。

## Open Questions

- Fact Sheet 是否在 `/sprint-exps` 时默认写入 `iterations/<stage>/<sprint-id>/fact-sheet.md`，还是仅默认 stdout、通过 `--write` 落盘？
- JSON 输出是否需要纳入长期稳定契约，还是先作为脚本测试使用的内部格式？
