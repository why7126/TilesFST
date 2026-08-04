## 上下文

`/sprint-exps` 已经要求优先运行 `scripts/generate-sprint-fact-sheet.py --sprint <sprint-id> --summary`，并使用 summary 控制大型 Sprint 的读取边界。现状问题是 AI usage snapshot 中的 `usage_matrices` 可包含多指标、多对象、多命令列的矩阵；当 Sprint 包含 10+ Change 或大量 REQ/BUG 时，summary 仍可能把完整矩阵带入默认输出，抵消 Fact Sheet 降低上下文占用的目标。

本变更属于 Agent 工作流工具治理，不改变产品业务 API、数据库或前端页面。

## 目标 / 非目标

**目标：**

- 让 Fact Sheet summary 默认输出 compact AI usage 摘要，而不是完整矩阵明细。
- 保留完整 `usage_matrices` 的可追溯读取能力，避免复盘需要真实矩阵时丢失数据。
- 让 `/sprint-exps` 的默认流程先消费 compact 摘要，再按需读取完整矩阵字段。
- 用测试固定 10+ Change Sprint 的默认输出边界，防止后续回退。

**非目标：**

- 不改变 AI usage snapshot 的存储结构。
- 不改变 command run 聚合、脱敏和 fresh gate 判定口径。
- 不调整复盘文档是否最终展示四张矩阵的产品语义；本变更只约束默认读取和默认输出边界。
- 不引入外部依赖。

## 决策

1. Summary 中新增 compact 视图字段。

   `ai_usage_snapshot` 在 summary 模式下保留 `fresh_gate`、`ai_usage_mode`、`snapshot_status`、关键 totals、coverage、warning_count、recommended_action，并新增或整理 `usage_matrices_summary`，记录 metrics、columns_count、rows_count、matrix_available、是否被省略以及按需读取提示。

   选择该方案是因为调用方仍能判断矩阵是否可用，却不会默认携带完整 rows。备选方案是直接删除 summary 中的矩阵信息，但会让 `/sprint-exps` 无法判断是否需要补读。

2. 完整矩阵继续通过 fields 模式读取。

   保留 `--fields ai_usage_snapshot.usage_matrices` 或等价字段路径，供用户明确要求完整矩阵、复盘文档确需落表、或调试聚合口径时使用。

   选择 fields 模式是因为项目已有 `evidence_hints` 按需读取模式，复用同一交互模型能减少新参数和新心智负担。

3. 10+ Change Sprint 默认强制 compact。

   当 summary 能识别 Sprint scope 中 Change 数量达到 10 个或以上时，默认输出 MUST NOT 包含完整 `usage_matrices.rows`。小 Sprint 也 SHOULD 使用 compact 输出，以保持一致；但测试重点覆盖 10+ Change 的高风险场景。

4. `/sprint-exps` Skill 文案同步收紧。

   技能默认只读取 compact Token Usage Fact Sheet summary。只有用户明确要求真实矩阵明细，或写入复盘文档的矩阵章节时，才通过 fields 模式读取完整矩阵，并继续遵守 fresh gate。

## 风险 / 权衡

- [风险] 复盘文档仍要求四张矩阵，若实现只保留 compact summary，可能导致复盘缺少矩阵数据。→ 缓解：tasks 明确要求在需要落表时通过 fields 模式补读完整矩阵。
- [风险] 现有测试或下游脚本断言 summary 中存在 `usage_matrices`。→ 缓解：测试更新为断言 compact summary，并补充 fields 模式读取完整矩阵的兼容测试。
- [风险] 字段命名变化造成调用方短期适配成本。→ 缓解：尽量新增 `usage_matrices_summary`，避免改变 snapshot 原始事实源；若必须移除 summary 内完整 `usage_matrices`，在文档和测试中明确迁移路径。

## 迁移计划

1. 调整 Fact Sheet summary 构建逻辑，默认生成 compact AI usage 摘要。
2. 保证完整 JSON 和 fields 模式仍可返回完整 `usage_matrices`。
3. 更新 `/sprint-exps` Skill 的默认读取边界和 Token Usage Fact Sheet 文案。
4. 更新并运行相关 pytest 与 OpenSpec 语言校验。
