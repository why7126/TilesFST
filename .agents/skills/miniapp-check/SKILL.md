---
name: "miniapp-check"
description: "检查微信小程序环境策略、运行入口同步和生产接口可访问性"
---

# miniapp-check

Use this skill when the user asks `/miniapp-check` or wants to verify miniapp environment configuration before preview, trial, review, or release.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；只读取小程序环境配置、脚本和测试片段。
- 生产 smoke 失败时输出关键状态码和 URL，不输出长响应体。

## Input

- Optional flags: `--smoke` to check production endpoints.

## Must Read

```text
rules/coding.md
rules/testing.md
rules/security.md
rules/agent-context-budget.md
scripts/miniapp-env.py
src/miniapp/utils/env.ts
src/miniapp/utils/env.js
src/miniapp/project.private.config.json
```

## Steps

1. 执行：

```bash
python scripts/miniapp-env.py check --smoke
```

2. 执行静态测试（除非用户只要求快速查看）：

```bash
uv run pytest tests/test_miniapp_static.py
```

3. 报告当前策略、`.ts/.js` 同步状态、`project.private.config.json setting.urlCheck` 是否符合策略、生产接口 smoke 结果、合法域名和手机缓存检查提醒。

## Output

明确给出是否可继续上传体验版；若 blocked，给出最短修复路径。若策略为 `auto` 或 `dev` 且 `urlCheck=true`，优先执行 `python scripts/miniapp-env.py set auto` 或 `set dev` 修复本地开发者工具网络拦截。

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

