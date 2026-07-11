---
bug_id: BUG-0062-archive-issue-subdoc-status-consistency
title: 归档后 issue 子文档状态一致性检查缺失根因分析
status: archived
severity: high
owner: product
created_at: 2026-07-11 16:05:13
updated_at: 2026-07-11 20:13:04
related_requirement:
related_change:
---

# 根因分析

## 结论

该缺陷属于工作流治理与归档门禁缺陷。当前归档链路已经能同步 issue 主追踪文件 `trace.md`、`_registry.yaml` 以及 Sprint 派生文档，但没有把 issue 包内其他带状态字段的子文档纳入归档一致性检查。

因此，当 `bug.md`、`requirement.md`、`acceptance.md`、`root-cause.md`、`workaround.md`、`user-stories.md`、`business-flow.md` 等子文档仍保留 `draft`、`pending_review`、`in_sprint` 或 `applied` 时，归档流程仍可通过，并把整包迁入 `issues/**/archive/`。

## 直接原因

归档路径中的关键脚本职责边界存在缺口：

- `scripts/sync-workflow-status.py` 主要同步 `trace.md`、registry、Sprint Scope 与相关派生文档。
- `scripts/promote-issues-for-archive.py` 判断 issue 是否可进入 `archive/` 时，主要依据 `trace_status`、关联 Change 是否 archived、以及当前 issue stage。
- `scripts/promote-issue-stage.py` 执行阶段迁移时，只更新 `trace.md` 的 `lifecycle_stage` 与变更记录。
- `/opsx-archive` 和 `/sprint-archive` 技能说明中未要求对 issue 子文档状态残留执行强制门禁。

这些逻辑都没有扫描 issue 包内其他 Markdown 的 frontmatter / YAML block `status` 字段。

## 根本原因

工作流事实源的“主状态”和“包内文档状态”没有建立统一闭环规则：

- 规则层强调 `trace.md` 与 lifecycle stage 的一致性，但没有明确 archive 包内子文档允许/禁止的状态集合。
- 脚本层已有局部扫描能力，例如 Sprint 复盘 fact sheet 可识别 residual status，但该能力只作为 warning，不参与归档阻断。
- 归档门禁关注 Change tasks、OpenSpec archive 与 issue 主状态，未覆盖 issue 子文档状态一致性。

## 触发条件

满足以下条件时可触发：

1. REQ 或 BUG 已进入 review 阶段，并关联可归档的 OpenSpec Change。
2. `trace.md` 经 workflow-sync 推进为 `done`，或满足 promote 到 archive 的主状态条件。
3. issue 包内任一子文档仍保留非闭环状态，例如 `draft`、`pending_review`、`in_sprint`、`applied`、`todo`、`open`。
4. 执行 `/opsx-archive` 或 `/sprint-archive`。

## 分类

| 维度 | 分类 |
|---|---|
| 缺陷类型 | workflow / governance |
| 影响层级 | Issue 生命周期、OpenSpec 归档、Sprint 归档 |
| 主要模块 | `scripts/promote-issues-for-archive.py`、`scripts/promote-issue-stage.py`、`scripts/sync-workflow-status.py` |
| 相关模块 | `scripts/generate-sprint-fact-sheet.py`、`.agents/skills/source-command-opsx-archive/SKILL.md`、`.agents/skills/source-command-sprint-archive/SKILL.md` |
| API 层 | 不涉及 |
| 数据库层 | 不涉及 |
| 前端/小程序 | 不涉及 |

## 证据

- 归档 readiness 当前可在所有 Change tasks 完成时返回 PASS，但不会检查 issue 子文档状态残留。
- archive 目录中已有真实样本存在 `bug.md: status: draft`、`acceptance.md: status: pending_review`、`requirement.md: status: in_sprint` 等残留状态。
- `scripts/generate-sprint-fact-sheet.py` 已存在 `scan_issue_residual_status()`，说明该类残留状态可以被程序识别，但尚未纳入归档门禁。

## 修复方向建议

后续 `bug-opsx` / `opsx-apply` 可考虑：

- 抽取统一的 issue 子文档状态扫描能力，复用 `generate-sprint-fact-sheet.py` 中已有思路。
- 在 `promote-issues-for-archive.py` 或归档 readiness 阶段增加 blocker。
- 输出残留文件路径、字段来源和状态值，帮助人工快速修正。
- 明确 archive 包内允许的状态集合，例如 `done`、`archived`、`resolved`、`closed`，或对无状态子文档忽略。
- 补充测试覆盖 REQ 与 BUG 两类 issue 包，覆盖 frontmatter 与 fenced YAML block 两种状态来源。
