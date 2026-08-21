---
name: "miniapp-env"
description: "切换微信小程序 API 环境策略：dev、prod、auto"
---

# miniapp-env

Use this skill when the user asks `/miniapp-env <dev|prod|auto>` or wants to switch the miniapp API environment.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；先定位再分段读取，避免全量展开无关目录。
- 只读取小程序环境相关文件、脚本和必要规则；不要默认读取全部 docs、issues、iterations 或 archive。

## Input

- `dev`：所有运行形态使用本地 API：`http://127.0.0.1:8010`，fallback 到 `localhost:8010`、`localhost:8000`。
- `prod`：所有运行形态使用生产 API：`https://tilesfst.wjoyhappy.site`。
- `auto`：开发版使用本地，体验版和正式版使用生产。

DevTools URL 校验随策略同步：

- `dev` / `auto` MUST 将 `src/miniapp/project.private.config.json` 的 `setting.urlCheck` 设为 `false`，否则开发版本地 HTTP API 会被微信开发者工具拦截并显示“网络开小差”。
- `prod` MUST 将 `setting.urlCheck` 设为 `true`，用于体验版、提审和正式发布前验证生产合法域名。

## Must Read

```text
rules/coding.md
rules/testing.md
rules/directory-structure.md
rules/agent-context-budget.md
src/miniapp/README.md
scripts/miniapp-env.py
```

## Steps

1. 确认参数为 `dev`、`prod` 或 `auto`；缺失时询问用户目标策略。
2. 执行：

```bash
python scripts/miniapp-env.py set <strategy>
```

3. 执行：

```bash
uv run pytest tests/test_miniapp_static.py
```

4. 输出当前策略、`project.private.config.json setting.urlCheck`、修改文件、测试结果和下一步建议。

## Output

说明是否影响 API、数据库、Web、小程序、管理端；是否需要 Orval；是否需要 Docker Compose 验证；是否补充或更新测试；遵循了哪些 `rules/` 文件。

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

