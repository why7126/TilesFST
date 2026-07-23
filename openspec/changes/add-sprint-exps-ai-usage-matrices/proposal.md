# Proposal: 增强 sprint-exps AI 使用量矩阵

## 背景

`/sprint-exps` 已要求输出“模型 Token 使用分析”，但当前 Sprint AI usage snapshot 主要提供总量与按命令聚合，缺少“迭代/需求/BUG × 命令”的交叉视图。复盘时很难看清每个 Sprint、REQ、BUG 在各工作流命令上的 total/input/output token 与模型调用次数分布。

## 目标

- 在 `data/ai-usage` 派生的 Sprint snapshot 中新增 AI 使用量矩阵。
- `/sprint-exps` 复盘文档必须输出四张矩阵表：`total_tokens`、`input_tokens`、`output_tokens`、`model_call_count`。
- 矩阵纵向按 Sprint、REQ、BUG 排序，横向按规范命令顺序展示，并在最上方提供 `Total` 汇总行。
- 继续遵守 AI usage 脱敏边界，不写入 prompt、工具输出全文、本机绝对路径或敏感信息。

## 非目标

- 不改变业务 API、数据库、Web、小程序或管理端行为。
- 不引入新的运行时数据表或数据库迁移。
- 不改变 session 原始数据采集口径，只扩展 snapshot 派生聚合与复盘展示规范。

## 风险与缓解

- 风险：同一 command run 同时关联多个 REQ/BUG 时，矩阵按对象视角展示会出现对象行合计大于 Sprint 总行的情况。
  - 缓解：Sprint 行与 Total 行按唯一 command run 汇总；REQ/BUG 行用于对象归因分析，并在规范中说明口径。
- 风险：历史 snapshot 缺少矩阵字段。
  - 缓解：Fact Sheet 对缺失字段保持兼容，复盘要求提示刷新 `data/ai-usage` snapshot。
