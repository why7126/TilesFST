---
bug_id: BUG-0136-workflow-sync-bug-generate-captured-draft
status: done
created_at: 2026-08-22 21:13:43
updated_at: 2026-08-22 21:55:31
severity_hint: medium
environment: workflow
related_requirement: null
related_bug: null
lifecycle_stage: plan
captured_via: capture
classification_rationale: Workflow Sync 的 `bug.generate` 属于既有 BUG 工作流状态同步能力；用户指出该事件未主动将 BUG 从 `captured` 推进到 `draft`，表现为已交付规则/脚本行为偏差，因此分类为 BUG。
---

# 现象

执行 BUG 文档生成链路后，Workflow Sync 对 `bug.generate` 事件未主动把目标 BUG 从 `captured` 推进为 `draft`。

# 复现步骤

1. 准备一条仅完成 capture 的 BUG，`trace.md` 状态为 `captured`。
2. 执行 `/bug-generate <BUG-id>` 或等价生成 `bug.md` 的命令。
3. 在命令 Final Step 中运行 `python scripts/sync-workflow-status.py --event bug.generate --bug <BUG-id> --sprint auto`。
4. 检查目标 BUG 的 `trace.md`、`issues/bugs/_registry.yaml` 和 `issues/bugs/CHANGELOG.md`。

# 期望 vs 实际

- 期望：`bug.generate` Workflow Sync 能主动识别生成事件，并将目标 BUG 主状态从 `captured` 推进为 `draft`，同步更新 trace、registry 和当前态看板。
- 实际：`bug.generate` 未主动完成 `captured -> draft` 状态推进，导致生成了 `bug.md` 后状态仍可能停留在 `captured` 或依赖人工/命令侧额外修正。

# 影响范围

- `/bug-generate` 命令完成后的 BUG 主状态事实源。
- `issues/bugs/_registry.yaml` 与 `issues/bugs/CHANGELOG.md` 当前态看板。
- 后续 `/bug-complete`、`/bug-review`、`/sprint-propose` 的入口状态判断。
- Workflow Sync 对 Issue 子文档状态传播的可信度。

# 初步线索

- 需复核 `scripts/sync-workflow-status.py` 中 `bug.generate` 事件到 BUG 状态的映射。
- 需确认 `bug.md` 已存在时，Workflow Sync 是否应以事件为准推进主状态，而不是仅做派生刷新。
- 可参考 `req.generate` 或其他事件的状态推进逻辑是否一致。

# 建议验收或复现要点

- [ ] 对仅 `captured` 的 BUG 执行 `bug.generate` 同步后，`trace.md` 状态变为 `draft`。
- [ ] `_registry.yaml` 中对应 BUG 状态同步为 `draft`。
- [ ] `CHANGELOG.md` 下一步从 `/bug-generate` 变为 `/bug-complete`。
- [ ] 重复运行 `bug.generate` Workflow Sync 幂等，不重复写入异常状态或破坏变更记录。
- [ ] 若目标 BUG 未生成 `bug.md`，同步逻辑需保持明确 warning 或不误推进。

# 附件

- 暂无。
