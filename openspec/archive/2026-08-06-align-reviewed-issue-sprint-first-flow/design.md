---
change_id: align-reviewed-issue-sprint-first-flow
title: 评审后 Sprint 优先与命令收尾引导设计
status: applied
created_at: 2026-08-06 00:00:00
updated_at: 2026-08-06 12:06:26
---

# 设计

## 设计原则

- 以 `sprint.yaml` 作为 Sprint 范围机器事实源，避免仅靠口头或 Markdown 描述判断能否 apply。
- 将“推荐推进顺序”和“硬门禁”区分表达：推荐顺序变为评审后先 `/sprint-propose`，但对历史或修复场景中已 `in_sprint` 的 Issue，仍允许 `/req-opsx` / `/bug-opsx` 回填 Change。
- 命令技能的结束输出必须可执行，避免只写抽象描述。
- 待用户决策或处理点必须被单独列出，不能混在摘要里。

## 流程调整

调整后的 REQ/BUG 推荐链路：

```text
/req-capture 或 /bug-capture
→ /req-generate 或 /bug-generate
→ /req-complete 或 /bug-complete
→ /req-review --approve 或 /bug-review --approve
→ /sprint-propose sprint-xxx --req REQ-xxxx 或 --bug BUG-xxxx
→ /req-opsx REQ-xxxx 或 /bug-opsx BUG-xxxx
→ /opsx-apply <change-id> 或 /sprint-apply sprint-xxx
→ /opsx-archive <change-id> 或 /sprint-archive sprint-xxx
```

`/sprint-propose` 对已评审但尚未 Change 的 REQ/BUG 负责先写入 Sprint 正式范围，并保留“待创建/回填 Change”的机器状态或说明。随后 `/req-opsx` / `/bug-opsx` 创建 Change 后，通过 Workflow Sync 将 Change 回填同一 Sprint 的 `changes[]` 和 `scope_estimates[].change`。

## 命令结束输出契约

每个 `.agents/skills/*/SKILL.md` 命令技能都应在完成输出中包含：

```text
下一步：<可复制执行的命令或“暂无可推进下一步”>
待用户决策/处理：
- <决策或处理项；没有则写“无”>
```

两个区块必须分工清晰：`下一步` 承载可执行命令或明确动作；`待用户决策/处理` 只承载额外缺失输入、范围/策略选择、证据补充、验收/发布确认、阻塞项或人工处理事项。已经出现在 `下一步` 中的命令或动作不得重复写入 `待用户决策/处理`。

如果有多个分支，使用条件化命令：

```text
下一步：
- 若确认通过评审：/sprint-propose sprint-xxx --bug BUG-0122
- 若需要补充复现证据：/bug-complete BUG-0122
```

命令不得在未获授权时自动执行下一步；输出只做引导。

## 脚本校验

在现有技能预算校验中补充命令技能契约检查：

- 命令技能必须包含 `下一步` 或 `Next` 等下一步引导章节/文案。
- 命令技能必须包含 `待用户决策`、`待用户处理`、`决策点` 或等价文案。
- 命令技能必须包含下一步与待用户决策/处理的去重约束，防止把同一可执行命令重复输出两次。
- 校验失败时列出具体技能文件，阻止技能规范回退。

## 兼容性

- 历史已先 `/req-opsx` / `/bug-opsx` 再 `/sprint-propose` 的 Change 不需要迁移。
- 已处于 `in_sprint` 的 REQ/BUG 仍可执行 `/req-opsx` / `/bug-opsx` 回填 Change。
- 非 REQ/BUG 来源的纯技术治理 Change 仍可按 OpenSpec Change 流程处理，但输出也必须给出下一步和待决策点。
