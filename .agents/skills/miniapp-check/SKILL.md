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
