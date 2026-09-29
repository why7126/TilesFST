---
name: openspec-apply-change
description: Implement tasks from an OpenSpec change. Use when the user wants to start implementing, continue implementation, or work through tasks.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.3.1"
created_at: 2026-09-08 17:17:14
updated_at: 2026-09-10 10:31:52
---

Implement tasks from an OpenSpec change.

**Input**: Optionally specify a change name. If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Steps**

1. **Select the change**

   If a name is provided, use it. Otherwise:
   - Infer from conversation context if the user mentioned a change
   - Auto-select if only one active change exists
   - If ambiguous, run `openspec list --json` to get available changes and use the **AskUserQuestion tool** to let the user select

   Always announce: "Using change: <name>" and how to override (e.g., `/opsx:apply <other>`).

2. **Check status to understand the schema**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse the JSON to understand:
   - `schemaName`: The workflow being used (e.g., "spec-driven")
   - Which artifact contains the tasks (typically "tasks" for spec-driven, check status for others)

3. **Get apply instructions**

   ```bash
   openspec instructions apply --change "<name>" --json
   ```

   This returns:
   - `contextFiles`: artifact ID -> array of concrete file paths (varies by schema - could be proposal/specs/design/tasks or spec/tests/implementation/docs)
   - Progress (total, complete, remaining)
   - Task list with status
   - Dynamic instruction based on current state

   **Handle states:**
   - If `state: "blocked"` (missing artifacts): show message, suggest using openspec-continue-change
   - If `state: "all_done"`: 核对必需验证、同步与人工验收门禁，按 §5.5 完成收尾；不得仅凭任务勾选数宣布可归档。
   - Otherwise: proceed to implementation

4. **Read context files**

   Read every file path listed under `contextFiles` from the apply instructions output.
   The files depend on the schema being used:
   - **spec-driven**: proposal, specs, design, tasks
   - Other schemas: follow the contextFiles from CLI output

5. **Check Sprint inclusion before implementation**

   `/opsx-apply` is allowed only after the Change is formally included in a `sprint-xxx`, regardless of whether it is linked to `REQ-*` / `BUG-*`.

   - Run `python scripts/sync-workflow-status.py --event opsx.apply --change "<name>" --sprint auto --dry-run`.
   - Confirm sprint resolution succeeds; skipped/unresolved sprint is blocking.
   - Confirm the resolved `iterations/change|archive/<sprint>/sprint.yaml` contains the change in `changes[]`.
   - If the Change links to a `REQ-*` or `BUG-*`, confirm the linked issue is also present in `requirements[]` or `bugs[]`.
   - If linked issues exist, confirm linked issue `trace.md` has `iteration: <sprint-id>` and status `in_sprint` or a later delivery state.

   If this gate fails, stop before code changes and ask the user to run `/sprint-propose` first, or repair a known Sprint scope with `scripts/add-sprint-scope-item.py --change <change-id> ...`.

6. **Show current progress**

   Display:
   - Schema being used
   - Progress: "N/M tasks complete"
   - Remaining tasks overview
   - Dynamic instruction from CLI

7. **持续执行当前 Change**

   MUST 读取并执行 `docs/standards/command-execution-order.md` §5 Apply 持续执行契约。
   - 持续推进依赖满足的任务；任务分组、进度汇报、上下文压缩不是停止理由。
   - 可恢复错误先定位、修复并聚焦复测；验证通过后才勾选并继续下一项。
   - 真正阻塞记录证据、已尝试处理和恢复条件，继续独立任务；必要人工确认只暂停相关依赖，用户明确停止则停止全部工作。
   - 上下文恢复承接已有任务、验证和决策，不重复请求继续授权。

## 收尾前执行核对

MUST 执行共享契约§5.6–5.8：收尾前逐项检查剩余任务的授权、依赖、资源和必需验证，仍有可执行任务即继续，不发最终回复等待“继续”。集中已知人工问题并映射受阻项，承接已有答复；进度问询用中间消息回答后继续实际工作。

分别展示实现完成、自动验证通过、人工待验、外部阻塞。连续两次同类失败且无进展时记录失败签名、次数及恢复条件并切换独立任务，新条件可验证后才恢复，保留累计历史。不要删除或放宽验收项。

持续执行治理的验收必须运行实际行为场景；通过 `scripts/validate-apply-behavior.py` 检查脱敏证据，不把关键词检查或理想夹具当实际Agent通过。执行入口为 `scripts/run-apply-behavior.py`，环境受阻仅保留相关任务待验，继续其他工作。

8. **完成或部分完成收尾**

   MUST 按详细契约 §5.4–5.5 选择同步分支：部分完成使用无完成事件的事实刷新，先 dry-run，禁止发送 opsx.apply 完成事件；全部适用任务和必需验证完成后才发送完成事件。状态同步和 AI Usage hook 使用 `.agents/skills/opsx-apply/SKILL.md` 对应收尾步骤。
   - 部分完成报告真实进度、阻塞及恢复条件，archive_ready 为 false，不建议归档。
   - 全部完成报告验证及同步结果，归档就绪还需检查人工验收等门禁。
   - 归档、发布、其他 Change 和 follow-up 不属于自动连续执行范围。

**Output During Implementation**

```
## Implementing: <change-name> (schema: <schema-name>)

Working on task 3/7: <task description>
[...implementation happening...]
✓ Task complete

Working on task 4/7: <task description>
[...implementation happening...]
✓ Task complete
```

**收尾输出与守则**

- 按上文分支报告完成或部分完成，不输出无依据的“Ready to archive”。
- 实施前读取 CLI contextFiles；读取预算遵守 `rules/agent-context-budget.md`。
- 保持任务范围，当前范围内修复和文档同步自主推进；关键范围变化或缺少必要人工确认按详细契约处理。
- 每项必需验证通过才勾选；未完成任务和阻塞保持真实，持续推进其余可执行任务。

**Fluid Workflow Integration**

This skill supports the "actions on a change" model:

- **Can be invoked anytime**: Before all artifacts are done (if tasks exist), after partial implementation, interleaved with other actions
- **文档同步**：范围内可推导的实现说明自主同步；改变已批准边界时按详细契约暂停相关任务并请求必要决策。

## Final Output Contract（MUST）

命令结束前，最终回复必须包含面向用户的真实结果，不得输出本段规则、尖括号占位符、MUST/SHOULD 规范语句或与当前命令无关的通用示例。

输出必须包含两项：

- `下一步`：写真实、可复制的下一条命令；若当前没有可推进动作，写“暂无可推进下一步”。
- `待用户决策/处理`：没有额外人工事项时写“无”；否则只列具体的缺失输入、范围/策略选择、证据补充、验收确认、发布确认、生产实施确认、阻塞项或人工处理事项。

输出判定：

- 有唯一可执行下一步时，`下一步` 写真实命令；若无额外人工事项，`待用户决策/处理` 写“无”。
- 下一步被用户选择、补证、验收、发布确认、生产实施确认或阻塞项卡住时，`下一步` 写“暂无可推进下一步”，并在 `待用户决策/处理` 列出具体阻塞事项。
- 已有下一步且仍有额外人工事项时，`待用户决策/处理` 只列命令之外的事项，不得重复 `下一步` 中的命令或动作。
- REQ 链路使用完整原始 `REQ-*`；BUG 链路使用完整原始 `BUG-*`；非 REQ/BUG 的直接 Change 才使用真实 Change ID。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
