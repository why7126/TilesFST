---
bug_id: BUG-0062-archive-issue-subdoc-status-consistency
title: 归档后 issue 子文档状态一致性检查缺失评审记录
status: archived
review_decision: approved
severity: high
owner: product
reviewed_at: 2026-07-11 16:08:19
created_at: 2026-07-11 16:08:19
updated_at: 2026-07-11 20:13:04
related_requirement:
related_change:
next_step: /bug-opsx BUG-0062-archive-issue-subdoc-status-consistency
---

# 缺陷评审记录

## 评审结论

结论：批准修复（`approved`）。

`BUG-0062-archive-issue-subdoc-status-consistency` 属于 OpenSpec + Issue 工作流治理缺陷。当前归档流程可让 `trace.md` 与 registry 显示已完成，但同一 issue 包内其他子文档仍残留 `draft`、`pending_review`、`in_sprint` 等非闭环状态，破坏归档事实源一致性。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | archive 目录已有真实残留样本；归档脚本当前主要检查 trace 状态与 Change 状态，未检查 issue 子文档状态。 |
| 严重等级合理 | 通过 | 不直接影响线上业务，但会破坏研发事实源、归档审计和 Sprint 复盘可信度，`high` 合理。 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖 REQ/BUG、frontmatter/YAML block、阻断报告和无残留成功路径。 |
| 是否需 hotfix 路径 | 不需要 | 属于工作流治理缺陷，可走常规 `fix-*` Change；历史包清理应另行评审。 |

## 评审依据

- `bug.md` 已记录现象、复现步骤、期望/实际、影响范围和严重等级说明。
- `root-cause.md` 已说明缺口位于归档门禁未扫描 issue 子文档状态。
- `workaround.md` 已给出人工 `rg` 检查与处理建议。
- `acceptance.md` 已定义修复后的回归验收标准。
- `trace.md` 已达到 `pending_review`，具备评审条件。

## 决策

- 状态变更为 `approved`。
- 允许执行 `/bug-opsx BUG-0062-archive-issue-subdoc-status-consistency` 创建 `fix-*` OpenSpec Change。
- 允许后续纳入 Sprint 正式规划。
- 修复范围应优先限定在归档 readiness / promote 门禁与对应测试，不直接批量改写历史 archive 包状态。

## 风险与约束

- 修复不得绕过 OpenSpec Change 流程。
- 修复不得直接修改业务 API、数据库、Web、小程序或管理端业务 UI。
- 修复不得直接批量替换历史 archive 包状态；历史清理需要独立评审。
- 修复报告必须输出具体文件路径和残留状态，避免只给出笼统失败信息。
