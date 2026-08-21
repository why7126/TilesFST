---
name: "miniapp-restore"
description: "发布后恢复微信小程序默认环境策略"
---

# miniapp-restore

Use this skill when the user asks `/miniapp-restore` or wants to restore the miniapp environment after trial/release verification.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；只读取小程序环境配置、脚本和静态测试。

## Input

- Optional `--strategy dev|prod|auto`；默认恢复为 `auto`。
- 恢复为 `auto` 或 `dev` 时 MUST 同步关闭 `src/miniapp/project.private.config.json` 的 `setting.urlCheck`，避免开发版本地 HTTP API 被微信开发者工具拦截。

## Steps

1. 执行：

```bash
python scripts/miniapp-env.py restore --strategy auto
```

2. 执行：

```bash
uv run pytest tests/test_miniapp_static.py
```

3. 输出恢复后的策略摘要、`project.private.config.json setting.urlCheck` 和测试结果。

## Output

说明恢复后的策略、修改文件、测试结果、开发者工具是否需要重新编译，以及是否仍需要人工上传小程序。

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

