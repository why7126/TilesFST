# Design: 归档 Change trace 兜底摘要门禁

## Context

当前 Sprint 归档 readiness gate 主要校验 Change 目录是否存在以及 `tasks.md` checkbox 是否全部完成。对于已归档到 `openspec/changes/archive/YYYY-MM-DD-<change-id>/` 的 Change，缺少 `trace.md` 并不会被自动阻断；如果 `proposal.md`、`design.md`、`tasks.md` 也没有统一的归档验证摘要，后续审计无法稳定追溯验证结论、测试命令、Issue/Sprint 状态和归档证据。

`BUG-0063` 的修复目标是把这类证据缺口前移到 readiness gate，而不是依赖 `/sprint-exps` 或人工复盘时才发现。

## Goals / Non-Goals

**Goals:**

- 对 archived Change 显式记录 `trace.md` 是否存在。
- 在 `trace.md` 缺失时识别标准化归档验证摘要。
- 缺少 trace 且缺少摘要时输出 blocker，并返回非零退出码。
- 更新归档技能说明，使 `/opsx-archive` 和 `/sprint-archive` 都遵循同一门禁。
- 为三类核心路径补充回归测试。

**Non-Goals:**

- 不批量修复所有历史 archived Change。
- 不改变 OpenSpec CLI archive 命令本身。
- 不修改业务 API、数据库、Web、小程序或管理端运行时逻辑。
- 不要求 active Change 必须提前写入归档摘要。

## Decisions

### D1. 只对 archived Change 强制 fallback summary

readiness gate 应区分 active 与 archived Change。active Change 可以通过 `trace.md`、`tasks.md`、`acceptance.md` 等开发中工件继续表达状态；archived Change 已成为事实源，若缺失 `trace.md` 就必须有等价摘要承接归档证据。

### D2. 摘要识别采用标准章节与关键词双层检查

推荐标准章节为 `## 归档验证摘要`。识别时优先匹配该章节；章节存在后检查至少覆盖：

- 验证命令与结果。
- 验收结论。
- 关联 Issue / Sprint 状态。
- 归档路径或归档时间等归档证据。

这样可以鼓励统一格式，同时允许摘要位于 `proposal.md`、`design.md` 或 `tasks.md` 任一文件中。

### D3. blocker 报告必须可操作

当缺失摘要时，报告必须包含 Change id、归档路径、`trace.md` 状态、检查过的候选文件和缺失项。这样 `/opsx-archive`、`/sprint-archive` 或人工修复时可以直接定位要补的文件。

### D4. 测试使用最小 fixture 覆盖门禁

测试应使用临时 Sprint / Change fixture 构造三类路径：

- archived Change 存在 `trace.md`，通过。
- archived Change 缺失 `trace.md` 但存在完整 `## 归档验证摘要`，通过并标记 fallback pass。
- archived Change 缺失 `trace.md` 且无摘要，失败并输出 blocker。

## Risks / Trade-offs

- 风险：历史归档包缺 trace 较多，新门禁可能暴露大量 warning 或 blocker。
  - 缓解：只阻断当前 readiness 目标范围内的 Change，并在报告中给出具体补救路径。
- 风险：摘要格式过松会漏掉关键证据。
  - 缓解：使用标准章节加必备信息项检查。
- 风险：摘要格式过严会误阻断已有有效摘要。
  - 缓解：先支持章节级标准格式，必要时在后续 Change 中扩展兼容别名。

## Migration Plan

1. 扩展 readiness 数据模型，记录 `trace_exists`、`fallback_summary_status`、`fallback_summary_file` 与缺失项。
2. 增加 archived Change trace / fallback 检查函数。
3. 将检查结果纳入 readiness report 与退出码。
4. 更新归档技能说明。
5. 补充测试并运行 OpenSpec 校验。
