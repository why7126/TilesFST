---
bug_id: BUG-0136-workflow-sync-bug-generate-captured-draft
title: Workflow Sync 对 bug.generate 未主动从 captured 推进 draft
severity: medium
status: done
owner: null
discovered_at: 2026-08-22 21:13:43
environment: workflow
related_requirement: null
related_change: fix-workflow-sync-bug-generate-status-transition
created_at: 2026-08-22 21:18:43
updated_at: 2026-08-25 14:53:29
---

# Workflow Sync 对 bug.generate 未主动从 captured 推进 draft

## 现象

执行 BUG 文档生成链路后，Workflow Sync 对 `bug.generate` 事件未主动把目标 BUG 从 `captured` 推进为 `draft`。这会导致 `bug.md` 已生成，但 `trace.md`、registry 或当前态看板仍可能保留旧状态。

## 复现步骤

1. 准备一条仅完成 capture 的 BUG，`trace.md` 状态为 `captured`。
2. 执行 `/bug-generate <BUG-id>` 或等价生成 `bug.md` 的命令。
3. 在命令 Final Step 中运行：

   ```bash
   python scripts/sync-workflow-status.py --event bug.generate --bug <BUG-id> --sprint auto
   ```

4. 检查目标 BUG 的 `trace.md`、`issues/bugs/_registry.yaml` 和 `issues/bugs/CHANGELOG.md`。

## 期望结果

- `bug.generate` Workflow Sync 能识别生成事件，并将目标 BUG 主状态从 `captured` 推进为 `draft`。
- `trace.md` frontmatter 与 fenced YAML 中的 `status`、`lifecycle.generated` 和 `updated_at` 同步更新。
- `issues/bugs/_registry.yaml` 对应条目的 `status` 更新为 `draft`。
- `issues/bugs/CHANGELOG.md` 当前态行的下一步从 `/bug-generate` 推进为 `/bug-complete`。
- 重复运行 `bug.generate` 保持幂等，不重复写入异常状态或破坏变更记录。

## 实际结果

`bug.generate` 未主动完成 `captured -> draft` 状态推进，导致生成 `bug.md` 后仍可能需要命令侧或人工额外修正状态事实源。

## 影响范围

- `/bug-generate` 命令完成后的 BUG 主状态事实源。
- `issues/bugs/_registry.yaml` 与 `issues/bugs/CHANGELOG.md` 当前态看板。
- 后续 `/bug-complete`、`/bug-review`、`/sprint-propose` 的入口状态判断。
- Workflow Sync 对 Issue 子文档状态传播的可信度。

## 严重等级说明

严重等级为 `medium`。该问题不直接影响业务用户数据、API 运行或前端展示，但会造成 BUG 生命周期状态漂移，使后续工作流命令、评审入口和迭代规划建议出现误导，属于治理链路中的中等风险缺陷。
openspec_changes:
  - change_id: fix-workflow-sync-bug-generate-status-transition
    type: update
    status: archived
