---
bug_id: BUG-0058-workflow-sync-check-time-drift-idempotency
title: workflow-sync --check 时间漂移幂等性不足
severity: medium
status: in_sprint
owner: workflow
discovered_at: 2026-07-04 15:33:21
environment: local
related_requirement:
related_change: fix-workflow-sync-check-time-drift-idempotency
created_at: 2026-07-05 07:54:28
updated_at: 2026-07-05 15:09:02
---

# 现象

执行 `python scripts/sync-workflow-status.py --check` 时，已归档 Sprint 的 Scope 表可能仍报告漂移。漂移集中在 archived Change 的归档时间字段，例如同一 Change 的归档时间在不同同步轮次中呈现为 `08:15:02`、`08:16:02` 或其他被刷新后的时间值。

# 复现

1. 保持 `iterations/archive/sprint-004/sprint.md` 中 Scope 表已包含 archived Change 的归档时间。
2. 执行 `python scripts/sync-workflow-status.py --check`。
3. 如果 check 报告 `iterations/archive/sprint-004/sprint.md` drift，则对比当前文件与脚本渲染结果。
4. 观察 drift 是否只表现为 archived Change 时间字段变化，而非真实状态或范围变化。

# 期望 vs 实际

## 期望

- `workflow-sync --check` 对已归档 Sprint 的衍生 Scope 表保持幂等。
- archived Change 的归档时间使用稳定事实源，例如显式 lifecycle、变更记录或归档目录日期。
- 后续 workflow sync 刷新 issue trace / change trace 的 `updated_at` 时，不应改变归档时间推导结果。

## 实际

- 归档时间可能被 issue trace 或 change trace frontmatter `updated_at` 影响。
- 一次同步刷新 `updated_at` 后，再次执行 `--check` 可能报告新的时间漂移。
- 漂移会导致 CI 或人工验收误判衍生文档未同步。

# 影响范围

- 影响 `scripts/sync-workflow-status.py --check` 的稳定性。
- 影响 `iterations/*/sprint.md` Scope 表中 archived Change 的时间展示。
- 影响 workflow-sync 对 `_registry.yaml`、issue trace、Sprint 四件套的幂等信任度。
- 不直接影响后端 API、数据库结构、Web 管理端、店主端或小程序运行逻辑。

# 严重等级说明

严重等级为 `medium`。该问题不会造成线上业务不可用，也不影响用户侧功能；但会破坏工作流检查的确定性，使已归档内容在无业务变化时反复出现 drift，增加 CI 噪声和人工判断成本。
