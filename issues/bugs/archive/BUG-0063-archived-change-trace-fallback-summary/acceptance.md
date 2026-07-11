---
bug_id: BUG-0063-archived-change-trace-fallback-summary
title: archived Change 缺失 trace.md 时归档验证摘要兜底检查缺失验收标准
status: archived
created_at: 2026-07-11 16:06:00
updated_at: 2026-07-11 20:13:04
---

# 验收标准

## AC-001 archived Change trace 缺失检查

- [ ] 归档 readiness gate 能检测 archived Change 目录是否缺失 `trace.md`。
- [ ] readiness 报告中展示每个 Change 的 `trace.md` 状态。
- [ ] active Change 与 archived Change 的检查结果语义清晰区分。

## AC-002 归档验证摘要兜底规则

- [ ] 当 archived Change 缺失 `trace.md` 时，校验会检查 `proposal.md`、`design.md`、`tasks.md` 中是否存在标准化归档验证摘要。
- [ ] 标准化摘要至少覆盖验证命令/结果、验收结论、关联 Issue/Sprint 状态和归档证据。
- [ ] 缺失 `trace.md` 且无兜底摘要时，readiness gate 输出 blocker，不应静默 `PASS`。

## AC-003 历史样本回归

- [ ] 使用缺失 `trace.md` 的历史 archived Change 样本覆盖回归测试。
- [ ] 证明 `fix-api-governance-route-tags-known-debt` 这类缺 trace 样本不会再被无条件视为完整归档证据。
- [ ] 若历史样本已有足够摘要，报告应明确标记为 fallback summary pass；若没有，应标记为 blocker 或 warning，并给出缺失项。

## AC-004 技能与脚本一致

- [ ] `/opsx-archive` 技能说明补充：缺失 `trace.md` 时必须有归档验证摘要兜底。
- [ ] `/sprint-archive` 技能说明补充：readiness gate 必须覆盖 trace / fallback summary 检查。
- [ ] 手工归档 fallback 与脚本归档流程使用同一验收口径。

## AC-005 不扩大运行时影响

- [ ] 不修改后端 API 路径、请求、响应或错误码。
- [ ] 不修改数据库 schema 或迁移。
- [ ] 不修改 Web、小程序或管理端运行时功能。
- [ ] 不需要 Orval 生成。

## AC-006 回归验证命令

- [ ] 新增或更新脚本级测试覆盖 trace 缺失 + 无摘要、trace 缺失 + 有摘要、trace 存在三类场景。
- [ ] `python scripts/validate-sprint-archive-readiness.py --sprint <fixture>` 对缺 trace 且无摘要场景返回非零。
- [ ] 相关 pytest 或脚本校验通过。
