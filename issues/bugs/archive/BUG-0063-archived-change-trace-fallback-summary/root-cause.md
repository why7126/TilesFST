---
bug_id: BUG-0063-archived-change-trace-fallback-summary
title: archived Change 缺失 trace.md 时归档验证摘要兜底检查缺失根因分析
status: archived
created_at: 2026-07-11 16:06:00
updated_at: 2026-07-11 20:13:04
---

# 直接原因

Sprint 归档 readiness gate 当前只校验 Change 目录存在性与 `tasks.md` 完成度：

1. Change 目录缺失会被阻断。
2. `tasks.md` 缺失会被阻断。
3. `tasks.md` 存在未完成 checkbox 会被阻断。

该校验没有记录或判断 Change 目录中是否存在 `trace.md`，也没有在 `trace.md` 缺失时继续检查 `proposal.md`、`design.md`、`tasks.md` 是否包含标准化归档验证摘要。

# 根本原因

归档质量门禁的“完成证据”模型过窄。现有 readiness gate 将 `tasks.md` checkbox 视为主要完成证据，但 OpenSpec 归档审计还需要能追溯：

- 验证结论。
- 测试命令与结果。
- 关联 Issue / Sprint 状态。
- 归档时间和归档路径。
- 若没有 `trace.md`，等价证据位于哪个文档、哪个章节。

`/opsx-archive` 技能只要求“`trace.md` 存在时读取”，没有把缺失 trace 的兜底摘要作为归档前置门禁；`/sprint-archive` 复用 readiness gate 时，也没有补充这一层检查。

# 触发条件

满足以下条件时会稳定触发：

1. Change 已归档到 `openspec/changes/archive/YYYY-MM-DD-<change-id>/`。
2. 该归档目录缺失 `trace.md`。
3. `tasks.md` 所有 checkbox 均已完成。
4. `proposal.md`、`design.md`、`tasks.md` 没有统一格式的归档验证摘要，或现有脚本无法识别摘要。
5. 执行 `python scripts/validate-sprint-archive-readiness.py --sprint <sprint-id>`。

# 缺陷分类

| 维度 | 结论 |
|---|---|
| 类型 | governance / workflow tooling |
| 位置 | Sprint / OpenSpec 归档 readiness gate、opsx/sprint archive 技能约束 |
| 数据库 | 不涉及 |
| API | 不涉及 |
| 前端 | 不涉及 |
| 安全 | 不直接涉及权限或敏感信息泄露 |

# 修复方向

建议在后续 `fix-*` Change 中统一处理：

1. 扩展 `scripts/validate-sprint-archive-readiness.py` 的 `ChangeReadiness` 模型，加入 `trace_exists` 与 `fallback_summary` 结果。
2. 对 archived Change：若缺失 `trace.md`，必须在 `proposal.md`、`design.md`、`tasks.md` 中识别标准化归档验证摘要；缺失时输出 blocker。
3. 为 `fix-api-governance-route-tags-known-debt` 等历史样本增加回归测试，证明缺 trace 且无摘要时会失败。
4. 更新 `/opsx-archive` 与 `/sprint-archive` 技能说明，让手工流程和脚本门禁保持一致。
