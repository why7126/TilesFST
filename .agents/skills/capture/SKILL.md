---
name: "capture"
description: "智能收集 - 自动区分需求与缺陷，按需拆分并分别走 req-capture / bug-capture 落盘"
---

# capture

Use this skill when the user asks to run the workflow command `capture`.

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
- 检索先定位再分段读取；大范围 `rg/find` 默认排除 Harness、模板 assets、历史 agent 目录、archive、generated、node_modules、dist、coverage。
- 命令输出优先 `max_output_tokens <= 8000`；大 diff、OpenAPI/Orval 生成物、测试日志、Workflow Sync 输出先给摘要或命中数。


## Command Template

**Input**：用户不确定是需求还是 BUG 时的原始描述；可含混合多条。可选：`--priority`、`--severity`、`--parent REQ-xxxx`

**Output**：分类分析表 + 各 REQ/BUG 的 capture.md + trace.md + registry 更新

**禁止**：`requirement.md`、`bug.md`、`src/`、`openspec/`

**定位**：类型已知时用 `/req-capture` 或 `/bug-capture`；本命令用于类型未决或混合输入。

---

## Steps

1. 读 `rules/requirement-management.md`、`rules/bug-management.md`、两个 `_registry.yaml`
2. **解析 → 分类（REQ/BUG）→ 拆分**（见 `.agents/skills/capture/SKILL.md`）
3. 落盘：REQ 遵循 req-capture 模板与规则；BUG 遵循 bug-capture 模板与规则；frontmatter 加 `captured_via: capture` 与 `classification_rationale`
4. 输出分类分析表 + Capture 摘要

---

## 分类要点

- 已有能力/规范下的偏差 → **BUG**
- 尚未交付的新能力/流程 → **REQ**
- 混合输入 → 拆条目后分别归类
- 新功能 PRD 未达标 → BUG + `related_requirement`
- 媒体/对象存储输入若描述图片、视频、Logo、证书、缩略图、`object_key` 或 `/media/` 偏差，优先按媒体类 BUG 记录；品牌证书图片应检查是否归入 `images/default/brand-certificates/`，PDF/文档证书应检查是否归入 `files/default/brand-certificates/`
- 边界不清 → 分类表标注待澄清，capture 写待澄清项

拆分分别套用 `/req-capture` Multi-REQ 与 `/bug-capture` Multi-BUG 规则。

## 需求相关偏差阶段分流（MUST）

当输入描述某个已有关联 REQ、BUG、Change 或 Sprint 的“不如预期”时，MUST 先判断生命周期阶段，再决定是否创建新的 REQ / BUG：

| 阶段 / 条件 | 分类与动作 |
|---|---|
| 目标 Change 已 `/opsx-apply`、未 `/opsx-archive`，且反馈仍属于原需求、原 Change、原验收项或原能力边界 | 不自动创建 REQ / BUG；提示走 `/opsx-modify <REQ-id|BUG-id|change-id> <反馈>` |
| 目标 Change 未归档，但反馈新增原需求未包含的功能，或改变 API / DB / 权限 / 部署 / 对象存储边界 | 按新增能力记录为 REQ；建议 `/req-capture`，必要时说明会形成后续 Change |
| 目标 Change 未归档，但反馈是独立缺陷且影响范围超出当前 Change | 按 BUG 记录；建议 `/bug-capture`，能确认父需求时写 `related_requirement` |
| 原 REQ / Change 已归档，但所属 Sprint 未归档 | 不得回到 `/opsx-modify`；已交付能力偏差按 BUG 记录并关联原 REQ，新增能力按 REQ 记录 |
| 所属 Sprint 已归档 | 作为新的生命周期输入处理；已交付能力偏差走 BUG，新增期望走 REQ |

若同一条反馈同时包含“当前 Change 内验收偏差”和“范围外新增诉求 / 独立缺陷”，MUST 拆分：范围内部分建议 `/opsx-modify`，范围外部分按 REQ / BUG capture 记录。

---

## Directory Gate（MUST）

在创建任一 REQ / BUG 后、输出最终摘要前，MUST 运行：

```bash
python scripts/validate-directory-structure.py
```

- Exit code **MUST** be `0`
- 若报告空 Issue 包、缺少 `trace.md` 或 `REQ-NNNN` / `BUG-NNNN` 短编号重复，MUST 先修正对应目录或重新分配 ID，再继续 Workflow Sync
- 不得只依赖 `_registry.yaml` 判断新编号可用；分配前必须考虑 `plan` / `review` / `archive` 三阶段既有目录

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md`.对每条创建的 REQ / BUG：

```bash
for req in REQ-xxxx-slug ...; do
  python scripts/sync-workflow-status.py --event req.capture --req "$req" --sprint auto || exit 1
done
for bug in BUG-xxxx-slug ...; do
  python scripts/sync-workflow-status.py --event bug.capture --bug "$bug" --sprint auto || exit 1
done
```

- Exit code **MUST** be `0`
- Print summary **Workflow Sync Report**（注明 REQ N 条 + BUG M 条）；use `--output detail` only for debugging
- Do **not** hand-edit `sprint.md` Scope marker blocks

## Final Step — AI Usage Post-command Hook (MUST)

After Workflow Sync exits with code `0`, run the unified AI usage hook for **each created REQ / BUG**:

```bash
for req in REQ-xxxx-slug ...; do
  python scripts/extract-ai-usage.py --post-command-hook --workflow-event req.capture --req "$req" --json || exit 1
done
for bug in BUG-xxxx-slug ...; do
  python scripts/extract-ai-usage.py --post-command-hook --workflow-event bug.capture --bug "$bug" --json || exit 1
done
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

- 如果存在明确可推进的下一步，MUST 给出可复制执行的命令，例如 `/bug-review BUG-0122 --approve`。
- 如果下一步取决于用户选择，MUST 用条件化条目列出选项；已在「下一步」中给出的命令或动作，不得在「待用户决策/处理」中重复。
- 「待用户决策/处理」只列缺失输入、需用户选择的范围/策略/证据/验收/发布确认、阻塞项或需人工处理事项；没有则写“无”。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
