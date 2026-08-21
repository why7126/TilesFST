---
name: "bug-complete"
description: "缺陷完善 - 补齐 root-cause、workaround、acceptance、trace"
---

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
- 不要默认 `cat rules/*.md`、`cat AGENTS.md openspec/project.md rules/...` 或读取整目录；按本命令 Step 0 列表读取必要文件，已在同一会话读取过且无变更时用规则和 Skill 摘要承接。
- 检索先用 `rg -l` / `rg --files` 定位文件，再用 `sed -n '<start>,<end>p'` 或 `nl -ba ... | sed -n` 读取必要片段。
- 大范围 `rg` MUST 限制目录与输出：优先加 `--glob '!openspec/archive/**' --glob '!openspec/changes/archive/**' --glob '!**/node_modules/**' --glob '!**/.git/**'`；只有追溯历史归档时才放开 archive，并说明原因。
- 对 Harness / 模板工程 / agent 资产目录执行搜索时，默认排除 `pm-harness*/**`、`**/assets/**`、历史/外部 agent 目录（如 `.claude/**`、`.kiro/**`、`.opencode/**`）；除非当前任务明确要求分析这些目录。
- 命令输出优先控制在 `max_output_tokens <= 8000`；预期超出时先输出文件清单或命中计数，再分段读取。
- 不重复读取同一大文件集合；若需要再次确认，优先读取变更片段、`git diff -- <file>` 或具体 frontmatter/status 字段。

# bug-complete

Use this skill when the user asks to run the workflow command `bug-complete`.

## Command Template

**Input**：`BUG-xxxx`（须 `bug.md`）

**Output**：root-cause.md、workaround.md、acceptance.md、trace.md；logs/、screenshots/ 目录（若需）

**禁止**：`openspec/`、`src/`

---

## 文档要点

| 文件 | 内容 |
|------|------|
| root-cause.md | 直接原因、根本原因、触发条件、分类（code/design/db/…） |
| workaround.md | 临时规避或无 |
| acceptance.md | 回归 AC-xxx |
| trace.md | status → enriching → pending_review |

媒体类 BUG 的 acceptance MUST 引用 `docs/standards/media-bug-four-point-acceptance-template.md`，覆盖 key、object、URL、render 四联。品牌证书相关 BUG MUST 明确图片证书使用 `images/default/brand-certificates/`，PDF/文档证书使用 `files/default/brand-certificates/`，历史对象/缩略图/审计脚本需记录 dry-run、apply、幂等摘要。

`root-cause.md` MUST 遵守 `rules/root-cause-evidence.md`：写入根因状态（`unknown`、`hypothesis`、`probable`、`confirmed`）、证据链、验证方式；confirmed 根因必须有可定位证据，证据不足时必须写人工补证步骤。

## Readiness

Ready：bug + root-cause + acceptance + trace

## Next

`/bug-review BUG-xxxx`

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md` and run:

```bash
python scripts/sync-workflow-status.py --event bug.complete --bug <BUG-id> --sprint auto
```

- Exit code **MUST** be `0` before ending this command.
- Print the summary **Workflow Sync Report** to the user; use `--output detail` only for debugging.
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`).

## Final Step — AI Usage Post-command Hook (MUST)

After Workflow Sync exits with code `0`, run:

```bash
python scripts/extract-ai-usage.py --post-command-hook --workflow-event bug.complete --bug <BUG-id> --json
```

- Print only the compact hook summary: `status`, `usage_mode`, `command_run_count`, `sprint_snapshot`, `warning_count`, and `recommended_action`.
- If local session input is unavailable, report `usage_mode: unavailable` and the recommended action; do not treat that as parent command failure.

## Final Output Contract（MUST）

命令结束前，最终回复 MUST 明确包含：

```text
下一步：<可直接执行的命令；若没有则写“暂无可推进下一步”>
待用户决策/处理：
- <需要用户选择、确认、补充或处理的事项；若没有则写“无”>
```

- 如果存在明确可推进的下一步，MUST 给出可复制执行的命令，例如 `/bug-review BUG-0122`。
- 如果下一步取决于用户选择，MUST 用条件化条目列出选项；已在「下一步」中给出的命令或动作，不得在「待用户决策/处理」中重复。
- 「待用户决策/处理」只列缺失输入、需用户选择的范围/策略/证据/验收/发布确认、阻塞项或需人工处理事项；没有则写“无”。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
