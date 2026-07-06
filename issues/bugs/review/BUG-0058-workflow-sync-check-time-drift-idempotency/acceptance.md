---
bug_id: BUG-0058-workflow-sync-check-time-drift-idempotency
created_at: 2026-07-05 08:00:34
updated_at: 2026-07-05 08:00:34
---

# Acceptance

## AC-001 归档时间不读取可变 updated_at

- **WHEN** archived Change 需要渲染到 Sprint Scope 表
- **THEN** workflow-sync MUST NOT 使用 issue trace 或 change trace frontmatter `updated_at` 作为归档时间事实源
- **AND** MUST 优先使用 lifecycle、变更记录或归档目录日期等稳定来源。

## AC-002 无正文变化不刷新 updated_at

- **WHEN** workflow-sync 处理 Markdown 文档且渲染结果与原文一致
- **THEN** 写入辅助逻辑 MUST NOT 仅因运行同步而刷新 frontmatter `updated_at`
- **AND** `--check` 与普通同步后的再次 `--check` MUST 保持 no delta。

## AC-003 workflow-sync check 幂等

- **WHEN** 连续执行两次 `python scripts/sync-workflow-status.py --check`
- **THEN** 第二次 MUST 返回 0
- **AND** 不得报告 `iterations/archive/sprint-004/sprint.md` 仅时间字段 drift。

## AC-004 回归测试覆盖时间漂移

- **WHEN** 存在 issue trace `updated_at` 晚于真实归档记录的场景
- **THEN** 自动化测试 MUST 证明归档时间仍取稳定归档事实
- **AND** 自动化测试 MUST 覆盖无正文变化时 `persist_markdown` 不 touch `updated_at`。
