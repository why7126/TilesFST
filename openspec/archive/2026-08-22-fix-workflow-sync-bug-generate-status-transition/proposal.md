---
change_id: fix-workflow-sync-bug-generate-status-transition
status: proposed
type: fix
source_bug: BUG-0136-workflow-sync-bug-generate-captured-draft
sprint: sprint-025
created_at: 2026-08-22 21:36:45
updated_at: 2026-08-22 21:36:45
---

# 修复 Workflow Sync 的 bug.generate 状态推进

## 背景

`BUG-0136-workflow-sync-bug-generate-captured-draft` 已确认：对仅完成 capture 的 BUG 执行 `/bug-generate` 后，`bug.md` 已生成，但 `scripts/sync-workflow-status.py --event bug.generate` 未主动将目标 BUG 从 `captured` 推进为 `draft`。

本问题会导致 `trace.md`、`issues/bugs/_registry.yaml`、`issues/bugs/CHANGELOG.md` 和 `bug.md` frontmatter 状态漂移，后续 `/bug-complete`、`/bug-review`、`/sprint-propose` 的入口判断和下一步提示可能被误导。

## 变更内容

- 为 Workflow Sync 补齐 `bug.generate` 事件的主状态推进规则：目标 BUG 已生成 `bug.md` 时，从 `captured` 或等价可生成前状态推进为 `draft`。
- 同步更新 `trace.md` frontmatter、fenced YAML、`lifecycle.generated`、`issues/bugs/_registry.yaml`、`issues/bugs/CHANGELOG.md` 和 `bug.md` frontmatter。
- 保持重复运行幂等，避免重复写入异常变更记录。
- 对缺少 `bug.md` 的目标 BUG 保持保护逻辑，不凭空推进到 `draft`，并输出明确 warning 或 no-op 摘要。
- 增加聚焦回归测试，覆盖首次生成、重复生成、缺失 `bug.md` 保护和 BUG / REQ generate 口径一致性。

## 不做范围

- 不修改业务 `src/` 功能代码。
- 不新增或修改 API、数据库、Web、小程序或对象存储能力。
- 不改变 `/bug-complete`、`/bug-review`、`/sprint-propose` 的状态目标，仅修复 `bug.generate` 事件缺口。

## 回滚方案

- 如修复导致 Workflow Sync 对生成事件误推进，可回退本 Change 中对 `scripts/sync-workflow-status.py` 或 `scripts/workflow_sync/` 的状态转换修改。
- 回滚后保留现有人工规避方式：执行 `/bug-generate` 后人工核对并修正 trace、registry、CHANGELOG 与 `bug.md` 状态。
- 回滚前必须确认没有已生成 BUG 被错误推进到不符合文档事实的状态。
