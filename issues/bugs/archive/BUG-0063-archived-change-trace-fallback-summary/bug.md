---
bug_id: BUG-0063-archived-change-trace-fallback-summary
title: archived Change 缺失 trace.md 时归档验证摘要兜底检查缺失
severity: high
status: archived
owner:
discovered_at: 2026-07-11 13:21:59
environment: local
related_requirement:
related_change: fix-archive-trace-fallback-summary-gate
updated_at: 2026-07-11 20:13:04
---

# 现象

归档后的 OpenSpec Change 可以缺失 `trace.md`，且现有归档校验未要求 `proposal.md`、`design.md`、`tasks.md` 至少保留归档验证摘要。缺少 trace 且没有等价摘要时，归档包无法稳定说明验证结论、测试命令、关联 Issue/Sprint 状态、归档时间和归档证据。

# 复现

1. 选择一个已归档或准备归档的 Change。
2. 确认该 Change 目录缺失 `trace.md`。
3. 确认 `proposal.md`、`design.md`、`tasks.md` 中没有标准化归档验证摘要。
4. 运行归档 readiness 校验，例如：

```bash
python scripts/validate-sprint-archive-readiness.py --sprint sprint-005
```

5. 观察校验结果。

# 期望 vs 实际

- 期望：归档校验应检查 archived Change 是否缺失 `trace.md`；若缺失，应要求 `proposal.md`、`design.md`、`tasks.md` 中至少存在标准化归档验证摘要，否则阻断归档或输出明确 blocker。
- 实际：现有 readiness gate 只检查 Change 目录和 `tasks.md` 完成度。即使 archived Change 缺失 `trace.md`，只要 tasks 全部勾选，仍会显示 `PASS`。

# 影响范围

- 影响 `/opsx-archive`、`/sprint-archive` 后的归档审计和复盘追溯。
- 影响 `openspec/changes/archive/**` 中缺少 `trace.md` 的历史归档包。
- 不影响后端 API、数据库、Web、小程序或管理端运行时功能。

# 严重等级说明

严重等级为 `high`。该问题不会直接造成线上功能不可用，但会削弱 OpenSpec 归档事实源可信度：归档包可能表面完成，实际缺少统一验收证据，后续审计、复盘、Sprint fact sheet 和 workflow 状态追溯都需要从分散文档中人工拼接。

# 已知证据

- Sprint 005 复盘已记录同类问题：`fix-api-governance-route-tags-known-debt` 归档目录缺少 `trace.md`，仅保留 `proposal.md`、`design.md`、`tasks.md`。
- 当前 readiness gate 对 `sprint-005` 可返回 `PASS`，其中 `fix-api-governance-route-tags-known-debt` 的 tasks 为 `9/9`，但归档目录缺少 `trace.md`。
