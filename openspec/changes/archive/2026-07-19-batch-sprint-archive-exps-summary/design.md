## Context

当前 `agent-workflow-tooling` 已要求 `/sprint-exps` 优先使用 Sprint Fact Sheet，`/sprint-archive` 也会运行 readiness gate 与 Fact Sheet，避免默认全文读取 Sprint 四件套、Issue trace 和 Change tasks。
但这些规则主要是“整体摘要”视角；当一个 Sprint 包含 10 个以上 Change 时，单个 Fact Sheet 或 readiness 报告仍可能把所有 Change 的 tasks/trace/warnings 集中暴露，导致模型在 archive/exps 阶段一次性接收过多证据。

本变更把“大 Sprint”定义为 `sprint.yaml` 中 `changes[]` 数量大于等于 10 的 Sprint，并为 archive/exps 增加 batch summary 读取边界。

## Goals / Non-Goals

**Goals:**

- 为 10+ Change Sprint 建立统一 batch summary 契约，降低 `tasks.md` 与 `trace.md` 一次性读取峰值。
- 让 `/sprint-archive` 可按批次展示 queue、blockers、warnings 和 evidence hints，并在失败时定位到具体批次和 Change。
- 让 `/sprint-exps` 复盘时先消费 Fact Sheet 的批次摘要，再按 warnings/evidence hints 分段回读。
- 保持成功路径 compact 输出，避免把批次摘要变成另一种长日志。

**Non-Goals:**

- 不改变 OpenSpec archive 的语义，不放宽 tasks 完成、trace、Issue promote、路径残留等现有门禁。
- 不新增业务 API、数据库表、Web/小程序/管理端页面或 Docker 配置。
- 不把原始 `tasks.md`、`trace.md`、验收报告或 session JSONL 持久化到新的摘要文件。

## Decisions

1. **在现有 Fact Sheet / readiness 输出中扩展 batch summary，而非新增长期文档事实源。**
   - 选择：`scripts/generate-sprint-fact-sheet.py --json` 输出 `change_batches` 或等价结构；readiness JSON 可复用同一批次构造逻辑。
   - 原因：Sprint 事实源仍是 `sprint.yaml`、Change `tasks.md`/`trace.md` 与验收文档；batch summary 是读前聚合，不应成为人工维护文档。
   - 备选：新增 `iterations/*/<sprint>/batch-summary.md`。放弃原因是容易产生过期摘要和额外同步负担。

2. **批次大小固定默认上限为 5 个 Change，并允许脚本内部常量或参数复用。**
   - 选择：10+ Change 才触发批次摘要；每批最多 5 个 Change，按 `/sprint-archive` queue 排序或 `sprint.yaml` 顺序输出。
   - 原因：5 个 Change 足以让模型局部判断 blockers，同时避免批次数过多。
   - 备选：按 token 估算动态切批。放弃原因是实现复杂，且当前目标是流程治理的确定性改进。

3. **批次摘要只保留聚合事实和证据路径。**
   - 选择：每个 batch 包含 batch id、change ids、tasks 完成计数、trace 状态计数、blocker/warning 数量、evidence hints、recommended next read；不复制 tasks/trace 正文。
   - 原因：这与 `rules/agent-context-budget.md` 和既有 Fact Sheet 可追溯、不全文回读要求一致。
   - 备选：在摘要中包含每个 Change 的未完成 task 文本。放弃原因是大 Sprint 中仍会造成高峰值；需要细节时由 evidence hints 分段读取。

4. **技能文件显式要求 batch-first 读取流程。**
   - 选择：更新 `sprint-archive` 与 `sprint-exps` Skill，使大 Sprint 先运行 Fact Sheet/readiness JSON，按批次处理，成功路径只转述聚合计数。
   - 原因：AI 命令的上下文峰值主要来自执行习惯，必须把读取顺序写入技能门禁。

## Risks / Trade-offs

- [Risk] 批次摘要遗漏某个阻断细节，导致归档判断不充分 → Mitigation：失败路径必须提供 evidence hints，且最终 archive/close 仍运行现有 readiness、Issue promote、路径残留和 Workflow Sync 门禁。
- [Risk] 批次顺序与实际 archive queue 顺序不一致 → Mitigation：优先复用 readiness/archive queue 的排序逻辑；无法复用时在摘要中标明排序依据。
- [Risk] JSON 输出字段增加影响既有测试快照 → Mitigation：新增字段应向后兼容；测试只断言关键字段和计数，不依赖完整 JSON 字段顺序。
- [Risk] 小 Sprint 输出被不必要地复杂化 → Mitigation：少于 10 个 Change 时可保留现有整体摘要路径，batch summary 可为空或标记 `not_applicable`。

## Migration Plan

1. 扩展 Fact Sheet/readiness 的内部 Change 收集结果，生成 batch summary。
2. 更新 `sprint-archive`、`sprint-exps` 技能的 Must Read/Run 与读取边界。
3. 补充覆盖 10+ Change Sprint 的脚本测试和上下文预算校验。
4. 运行相关测试、OpenSpec validate 与 Workflow Sync。
