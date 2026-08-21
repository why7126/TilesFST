---
name: "sprint-propose"
description: "提议并创建新 Sprint 迭代规划（四件套）"
---

# sprint-propose

Use this skill when the user asks to run `/sprint-propose` or create/update a Sprint plan.

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- Sprint 范围分析先读取候选 `trace.md` 与摘要，不得全量展开上一 Sprint 四件套、复盘库或所有 active changes。
- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
- 不要 `ls -R` 或全量 `cat iterations/** docs/knowledge-base/**`；先列清单，再分段读取。
- 复盘默认只读最近 1 份；只有 open 行动项跨 Sprint 复发或用户要求时读第 2 份。
- `best-practices/` 只读取候选 REQ/BUG/Change 标签命中的文件。
- 已存在 Sprint 时先读 `sprint.yaml` 和 `sprint.md` 的目标/Scope/知识库承接片段。
- 搜索候选项默认排除 `openspec/archive/**` 与 legacy `openspec/changes/archive/**`；编号冲突只看目录名。
- 命令输出优先 `max_output_tokens <= 8000`。

## Input

- `sprint-xxx`：指定 Sprint ID。
- 自然语言目标：由 Agent 推导候选范围和编号。
- Flags：`--req`、`--bug`、`--change`、`--duration 2w`、`--dry-run`。

## Sprint ID Rules（MUST）

- Sprint ID MUST 使用 `sprint-xxx` 三位数字递增格式，例如 `sprint-022`。
- 当用户未指定 Sprint ID 且当前没有 `iterations/change/sprint-xxx/` 进行中迭代时，MAY 自动创建下一个 Sprint。
- 自动编号 MUST 同时扫描 `iterations/archive/` 与 `iterations/change/` 下符合 `sprint-[0-9]{3}` 的目录和 `sprint.yaml:sprint_id`，取最大编号加一；例如最新归档为 `sprint-021` 且无进行中迭代时，自动创建 `sprint-022`。
- 如果已存在 `iterations/change/sprint-xxx/` 进行中迭代，MUST 优先复用或要求用户明确选择，不得默认另建并行 Sprint。
- 不得使用日期、主题词或混合命名创建 Sprint，例如 `sprint-2026-08-07-spec-sync`。

## Must Read

```text
AGENTS.md
openspec/project.md
rules/global.md
rules/document-governance.md
rules/requirement-management.md
rules/bug-management.md
rules/directory-structure.md
rules/iterations-lifecycle.md
.agents/skills/workflow-sync/SKILL.md
docs/knowledge-base/README.md（存在时）
```

按候选范围分段读取：

```text
project.yaml（容量，若存在）
issues/requirements/{plan,review,archive}/<REQ>/trace.md + requirement/acceptance 摘要
issues/bugs/{plan,review,archive}/<BUG>/trace.md + bug/root-cause/acceptance 摘要
openspec/changes/<change>/proposal.md + tasks.md 摘要
iterations/change|archive/<sprint>/sprint.yaml（编号/冲突）
docs/knowledge-base/retrospectives/<latest>-retrospective.md（最近复盘）
docs/knowledge-base/best-practices/<matched>.md（按标签）
```

## Gates

### Review Gate（MUST）

纳入 Sprint 正式规划前，REQ/BUG status MUST 为 `approved` 或 `in_sprint`。

未评审条目：

- 不得写入 `sprint.yaml` 的 `requirements[]` / `bugs[]`。
- 不得写入 Sprint 目标、Scope、里程碑、工作量合计、release、acceptance 正式范围。
- 不得更新 `trace.md` `iteration`。
- 只能列入 `sprint.md`「延后项（待评审）」并提示 `/req-review` 或 `/bug-review`。

### Readiness Gate

| 类型 | Ready 条件 | Not Ready 处理 |
|---|---|---|
| REQ | `requirement.md`、`acceptance.md`、`trace.md` 齐全且 approved/in_sprint | 延后并建议 `/req-complete` 或 `/req-review` |
| BUG | `bug.md`、`root-cause.md`、`acceptance.md`、`trace.md` 齐全且 approved/in_sprint | 延后并建议 `/bug-complete` 或 `/bug-review` |
| Change | 若直接纳入 Change，则 `proposal.md`、`design.md`、`tasks.md` 存在且未 archived | 已评审 REQ/BUG 可先无 Change 纳入；缺失时在输出提示后续 `/req-opsx` 或 `/bug-opsx` |

### Capacity Gate

- 优先级：P0 BUG > P0 REQ > P1 > P2。
- 估算：XS=0.5、S=1、M=3、L=5、XL=8、XXL=13 人天。
- add-* 主能力 SHOULD <= 6。
- fix 缓冲 SHOULD >= 30% SP/人天。
- 必须在生成正式四件套或更新 REQ/BUG/Change trace 前计算：
  `capacity_usage = estimated_person_days / capacity_person_days`。
- 若容量或估算缺失导致无法计算，MUST 先补齐输入；不得默认通过。
- `estimated_person_days > capacity_person_days * 1.2` 时 MUST 硬阻断正式规划：
  - 不得生成 `iterations/change/<sprint>/` 四件套。
  - 不得更新 `trace.md` 的 `iteration` 或 Change trace。
  - 输出硬提示：必须拆分 Sprint、移出低优先级项或替换范围后重新运行 `/sprint-propose`。
- `capacity_person_days < estimated_person_days <= capacity_person_days * 1.2` 时 MAY 继续，但 MUST 写入容量风险、fix 缓冲影响和延后项建议。
- `estimated_person_days <= capacity_person_days` 时按既有 Review Gate、Readiness Gate 和 Capacity Gate 继续。

## Knowledge Intake

- 读取最近 Sprint 复盘，提取 open 行动项并写入 §知识库承接。
- 按范围标签选择 best-practices：`admin-list`、`admin-form`、`admin-modal`、`media-upload`。
- `sprint.md` 必须包含 §横切预防清单，列出适用 best-practices 与验收 gate 摘要。

## Artifacts（非 `--dry-run` MUST）

目录：`iterations/change/sprint-xxx/`

```text
sprint.yaml
sprint.md
release-note.md
acceptance-report.md
```

`sprint.yaml` MUST 包含：

```yaml
sprint_id: sprint-xxx
status: planning
lifecycle_stage: change
start_date: YYYY-MM-DD HH:mm:ss
end_date: YYYY-MM-DD HH:mm:ss
capacity: { developers: <int>, testers: <int> }
requirements: []
bugs: []
changes: []
estimated_story_points: <number>
estimated_person_days: <number>
```

`sprint.md` MUST 包含：目标、Scope、工作量、fix 缓冲、里程碑、风险、知识库承接、横切预防清单、依赖 ASCII 树、发布计划、关联文档。

Markdown frontmatter MUST 含 `created_at`、`updated_at`；更新只改 `updated_at`。

## Trace Updates

对纳入的 REQ/BUG/Change 更新：

```text
trace.md iteration: sprint-xxx
openspec/changes/<change>/trace.md（若存在）
```

已评审但尚未创建 Change 的 REQ/BUG MAY 作为正式范围纳入 Sprint：

- `sprint.yaml` MUST 记录对应 `requirements[]` 或 `bugs[]`。
- `changes[]` MAY 暂不包含对应 Change。
- 输出 MUST 明确提示下一步执行 `/req-opsx <REQ-id>` 或 `/bug-opsx <BUG-id>`。
- 后续 `/req-opsx` 或 `/bug-opsx` 的 Workflow Sync MUST 将新 Change 回填同一 Sprint。
- `/opsx-apply` 仍 MUST 等待 Change 被写入 `changes[]` 后才能继续。

## Existing Sprint Scope Update（MUST）

当目标 `iterations/change|archive/<sprint>/sprint.yaml` 已存在，且本命令是在已有 Sprint 中追加或修正 REQ/BUG/Change 正式范围时，MUST 先使用确定性脚本更新机器事实源，不得只手工编辑 `sprint.md`、Issue trace 或 Markdown Scope 表：

```bash
python scripts/add-sprint-scope-item.py \
  --sprint <sprint-id> \
  [--req <REQ-id> | --bug <BUG-id>] \
  [--change <change-id>] \
  --size <XS|S|M|L|XL|XXL> \
  --story-points <number> \
  --person-days <number> \
  --rationale "<估算与影响说明>"
```

- 脚本成功后再运行 Workflow Sync 派生刷新 `sprint.md`、`release-note.md`、`acceptance-report.md`、Issue trace 和 Change trace。
- 多个范围项追加到同一个 Sprint 时，MUST 严格串行运行 `scripts/add-sprint-scope-item.py`；不得使用并行工具同时写同一个 `sprint.yaml`。脚本虽然带文件锁，但命令编排仍必须以最新写入后的 YAML 作为下一项输入，避免覆盖、重复键或坏 UTF-8。
- `sprint.md` `## 1. 目标` 的 Sprint 目标编号列表 MUST 同步包含本次新增或修正的 REQ/BUG/必要纯 Change；对应 `### xxx 要点` 段落 MUST 同步补齐或更新。
- `sprint.md` `## 2. Scope` 主表 MUST 保持六列：`类型 | 编号 | 标题 | 状态 | 估算 | 说明`。不得改成 `范围项 | 状态 | 估算` 窄表；需要降低预览宽度时，只能缩短 `说明` 文案或把细节放入 workflow-sync 分组表。
- 若新增项带有 Change，结束前 MUST 运行 `python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto --dry-run`，并确认输出解析到目标 Sprint，不得报告 `not in sprint scope`。
- 若 dry-run 仍报告 `not in sprint scope`，MUST 停止并修复 `sprint.yaml` 机器源；不得以 `sprint.md` Scope 表或人工摘要已出现该项作为完成依据。

## Output

报告 Sprint ID、状态、纳入 REQ/BUG/Change 数量、估算、知识库承接、容量门禁、四件套路径、下一步、待用户决策/处理。

若纳入范围存在已评审但尚未 Change 的 REQ/BUG，下一步 MUST 输出可直接执行的命令，例如：

```text
下一步：
- /req-opsx REQ-xxxx
- /bug-opsx BUG-xxxx
待用户决策/处理：
- 确认是否在本 Sprint 内立即创建上述 Change；若暂缓，说明暂缓原因。
```

## Final Step — Workflow Sync（MUST）

Run:

```bash
python scripts/sync-workflow-status.py --event sprint.propose --sprint <sprint-id>
```

- Exit code MUST be `0`。
- Print summary Workflow Sync Report；use `--output detail` only for debugging。
- Do not hand-edit workflow-sync marker blocks。

Then validate the user-readable Sprint Scope view:

```bash
python scripts/validate-sprint-scope.py <sprint-id> \
  [--item <REQ-id>] [--item <BUG-id>] [--item <change-id>]
```

- Exit code MUST be `0` before finishing `/sprint-propose`.
- Pass every REQ/BUG/Change newly added or updated by this run.
- This check is required because `sprint.yaml` is the machine source, but `sprint.md` `## 1. 目标` target id list and `## 2. Scope` are product-facing planning sources; all MUST contain the same formal scope.

## Final Step — AI Usage Post-command Hook (MUST)

After Workflow Sync exits with code `0`, run:

```bash
python scripts/extract-ai-usage.py \
  --post-command-hook \
  --workflow-event sprint.propose \
  --sprint <sprint-id> \
  [--req <REQ-id>] \
  [--bug <BUG-id>] \
  [--change <change-id>] \
  --json
```

- Print only the compact hook summary: `status`, `usage_mode`, `command_run_count`, `sprint_snapshot`, `warning_count`, and `recommended_action`.
- Pass every REQ/BUG/Change newly added or updated by this `/sprint-propose` run so the hook can attribute the correct command run and auto-discover the local session when `--session-jsonl` is not available.
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
