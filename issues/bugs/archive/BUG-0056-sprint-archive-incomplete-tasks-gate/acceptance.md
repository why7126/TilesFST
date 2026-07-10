---
bug_id: BUG-0056-sprint-archive-incomplete-tasks-gate
created_at: 2026-07-04 15:04:22
updated_at: 2026-07-04 15:04:22
---

# Acceptance

## AC-001 默认阻断未完成 tasks

- **WHEN** Sprint 的任一 change `tasks.md` 存在 `- [ ]`
- **THEN** `/sprint-archive` 前置校验 MUST 返回非零退出码
- **AND** 报告 MUST 明确列出 change id 与未完成任务数。

## AC-002 已提前归档的未完成 change 仍可被发现

- **WHEN** Sprint 已在 `iterations/archive/`，且对应 archived change 的 `tasks.md` 仍有未完成项
- **THEN** 校验脚本 MUST 继续报告 blocked
- **AND** 不得因为 change 已在 archive 目录而跳过 tasks 校验。

## AC-003 完成状态通过

- **WHEN** Sprint 内所有 change 的 `tasks.md` 均为 `- [x]`
- **THEN** 校验脚本 MUST 返回 0
- **AND** 报告 verdict MUST 为 PASS。

## AC-004 命令文档强制使用校验脚本

- **WHEN** AI 或开发者执行 `/sprint-archive`
- **THEN** `.cursor/commands/sprint-archive.md` 与 Codex skill MUST 要求先运行校验脚本
- **AND** 默认模式下 blocked verdict MUST 停止归档、停止 Sprint close、停止 issue promote。
