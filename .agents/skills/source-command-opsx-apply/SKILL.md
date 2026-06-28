---
name: "source-command-opsx-apply"
description: "Implement tasks from an OpenSpec change (Experimental)"
---

# source-command-opsx-apply

Use this skill when the user asks to run the migrated source command `opsx-apply`.

## Command Template
Implement tasks from an OpenSpec change.

**Input**: Optionally specify a change name (e.g., `/opsx:apply add-auth`). If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

Optional flags:

| Flag | 含义 |
|------|------|
| `--skip-cross-cutting-gate` | 跳过 Step 3.5（仅 P0 热修；输出 MUST 注明理由） |

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
   - `contextFiles`: artifact ID -> array of concrete file paths (varies by schema)
   - Progress (total, complete, remaining)
   - Task list with status
   - Dynamic instruction based on current state

   **Handle states:**
   - If `state: "blocked"` (missing artifacts): show message, suggest using `/opsx:continue`
   - If `state: "all_done"`: congratulate, suggest archive
   - Otherwise: proceed to implementation

4. **Read context files**

   Read every file path listed under `contextFiles` from the apply instructions output.
   The files depend on the schema being used:
   - **spec-driven**: proposal, specs, design, tasks
   - Other schemas: follow the contextFiles from CLI output

   Also read when UI-related:

   ```text
   docs/knowledge-base/README.md
   issues/requirements/<REQ-ID>/acceptance.md    # §横切 AC
   issues/requirements/<REQ-ID>/trace.md         # knowledge_base_refs, cross_cutting_tags
   issues/bugs/<BUG-ID>/root-cause.md            # fix-* 时
   iterations/*/sprint.md                        # §横切预防清单（若 change 在 Sprint 内）
   ```

5. **Cross-cutting Apply Gate（MUST before `src/`）**

   除非 `--skip-cross-cutting-gate`，在实现任何 pending task **之前** MUST 输出 **Cross-cutting Apply Gate Report**。

   ### 5.1 判定 UI 场景标签

   按优先级推断（可多选）：

   1. `issues/requirements/<REQ>/trace.md` → `cross_cutting_tags`
   2. `design.md` / `proposal.md` 范围描述
   3. change id 与 tasks 关键词（list / modal / upload / settings / profile / form）

   | 标签 | 触发条件 |
   |------|----------|
   | `admin-list` | 管理端列表页、分页、table-card |
   | `admin-form` | 表单页、设置 Tab、页内保存 |
   | `admin-modal` | 弹窗 CRUD、modal-card |
   | `media-upload` | 图片/视频/Logo/头像上传 |

   **无标签**（纯 API/后端/脚本）→ Gate **N/A**，跳到 Step 6。

   ### 5.2 读取 best-practices（按标签）

   | 标签 | 文档 |
   |------|------|
   | `admin-list` | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` |
   | `admin-form` | `docs/knowledge-base/best-practices/admin-form-page-consistency.md` |
   | `admin-modal` | `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` |
   | `media-upload` | `docs/knowledge-base/best-practices/admin-media-upload-chain.md` |

   ### 5.3 文档门禁检查

   | 检查项 | add-* + UI 标签 | fix-* + UI 标签 |
   |--------|-----------------|-----------------|
   | `acceptance.md` §横切 AC (`AC-XCUT-xxx`) | **MUST 存在** | SHOULD（可引用父 BUG acceptance） |
   | `trace.md` `knowledge_base_refs` | SHOULD | SHOULD |
   | `design.md` 引用 knowledge-base | SHOULD | SHOULD（fix design 常含根因链接） |
   | `sprint.md` §横切预防清单 | SHOULD（在 Sprint 内时） | SHOULD |

   ### 5.4 实现对照清单（apply 过程中 MUST 遵守）

   从 best-practices「验收 gate」提取，在 Report 中列出 checkbox；**首个 UI 相关 task 开始前** 展示，**最后一个 UI task 完成前** 逐项确认：

   | 标签 | 实现 MUST 对照要点 |
   |------|-------------------|
   | `admin-list` | 分页 DOM 对齐 `/admin/users`；fixed toast；状态变更 DS confirm；无 `window.confirm` |
   | `admin-form` | 单保存 CTA（footer）；无页头重复保存；DS confirm；fixed toast 无 layout shift |
   | `admin-modal` | 仅 `{feature}-modal-card`；禁止 `modal-card` 双类；Computed width；矮视口 scroll |
   | `media-upload` | idle→uploading→done/failed；同会话回显；Docker `:3000` 边界验收（tasks 含则执行） |

   ### 5.5 Verdict 与暂停

   ```markdown
   ## Cross-cutting Apply Gate

   **Change:** <name>
   **Tags:** admin-list, …
   **Refs:** docs/knowledge-base/best-practices/…

   | Gate | Status |
   |------|--------|
   | AC-XCUT in acceptance | pass / fail / n/a |
   | knowledge_base_refs | pass / warn |
   | best-practices read | pass |

   **Verdict:** PROCEED | BLOCKED | WARN-PROCEED
   ```

   - **BLOCKED**（`add-*` 且缺 AC-XCUT）：**暂停**，建议 `/req-complete <REQ>`；不得改 `src/`
   - **WARN-PROCEED**（fix-* 或缺 design 引用）：可继续，MUST 在首个 UI task 备注中补 design 引用
   - **PROCEED**：进入 Step 6

6. **Show current progress**

   Display:
   - Schema being used
   - Progress: "N/M tasks complete"
   - Remaining tasks overview
   - Dynamic instruction from CLI

7. **Implement tasks (loop until done or blocked)**

   For each pending task:
   - Show which task is being worked on
   - **UI 类 task**：对照 Step 5 Gate 清单；不符则 pause 并修正或更新 design
   - Make the code changes required
   - Keep changes minimal and focused
   - Mark task complete in the tasks file: `- [ ]` → `- [x]`
   - Continue to next task

   **Pause if:**
   - Step 5 Gate **BLOCKED** 未解决
   - Task is unclear → ask for clarification
   - Implementation reveals a design issue → suggest updating artifacts
   - Error or blocker encountered → report and wait for guidance
   - User interrupts

8. **On completion or pause, show status**

   Display:
   - Tasks completed this session
   - Overall progress: "N/M tasks complete"
   - If all done: suggest archive
   - If paused: explain why and wait for guidance

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

**Output On Completion**

```
## Implementation Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** 7/7 tasks complete ✓

### Completed This Session
- [x] Task 1
- [x] Task 2
...

All tasks complete! You can archive this change with `/opsx:archive`.
```

**Output On Pause (Issue Encountered)**

```
## Implementation Paused

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** 4/7 tasks complete

### Issue Encountered
<description of the issue>

**Options:**
1. <option 1>
2. <option 2>
3. Other approach

What would you like to do?
```

**Guardrails**
- **Cross-cutting gate first**: Step 5 MUST 在改 `src/` 前完成；`add-*` UI 缺 AC-XCUT → BLOCKED
- Keep going through tasks until done or blocked
- Always read context files before starting (from the apply instructions output)
- If task is ambiguous, pause and ask before implementing
- If implementation reveals issues, pause and suggest artifact updates
- Keep code changes minimal and scoped to each task
- Update task checkbox immediately after completing each task
- Pause on errors, blockers, or unclear requirements - don't guess
- Use contextFiles from CLI output, don't assume specific file names

**References**

- 横切 AC 来源：`.cursor/commands/req-complete.md`
- Sprint 级清单：`.cursor/commands/sprint-propose.md` §横切预防清单
- best-practices：`docs/knowledge-base/best-practices/`
- Sprint 编排：`.cursor/commands/sprint-apply.md`（嵌入本命令 Step 5）

**Fluid Workflow Integration**

This skill supports the "actions on a change" model:

- **Can be invoked anytime**: Before all artifacts are done (if tasks exist), after partial implementation, interleaved with other actions
- **Allows artifact updates**: If implementation reveals design issues, suggest updating artifacts - not phase-locked, work fluidly

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md` and run:

```bash
python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto
```

- Exit code **MUST** be `0` before ending this command.
- Print the **Workflow Sync Report** to the user.
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`).
