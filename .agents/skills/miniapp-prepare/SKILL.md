---
name: "miniapp-prepare"
description: "小程序发布前准备：切生产、静态测试、生产接口 smoke、输出上传体验版清单"
---

# miniapp-prepare

Use this skill when the user asks `/miniapp-prepare` or wants to prepare the WeChat miniapp for trial/review/release.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；只读取小程序环境配置、生产发布相关规则和脚本。
- 测试和 curl 输出使用摘要；失败时只展开关键错误。

## Must Read

```text
rules/coding.md
rules/testing.md
rules/security.md
rules/directory-structure.md
rules/agent-context-budget.md
src/miniapp/README.md
scripts/miniapp-env.py
```

## Gates

Prepare MUST be blocked unless:

- 小程序策略成功切到 `prod`。
- `src/miniapp/project.private.config.json` 的 `setting.urlCheck` 已切到 `true`。
- `uv run pytest tests/test_miniapp_static.py` 通过。
- `GET https://tilesfst.wjoyhappy.site/api/v1/miniapp/home` 返回 `200` 且 `code=0`。
- `GET https://tilesfst.wjoyhappy.site/api/v1/miniapp/brands?page=1&pageSize=2` 返回 `200` 且 `code=0`。

以上为自动门禁。DevTools Network 与体验版 Network 是人工 checklist，不得在未执行时写作 `passed`；缺失时只能记录 `blocked`、`follow_up` 或明确的 `not_applicable`。

## Steps

1. 执行：

```bash
python scripts/miniapp-env.py prepare
```

2. 如 sandbox 阻止 uv 缓存或外网 smoke，按审批规则重跑必要命令。
3. 输出微信开发者工具上传、公众平台设为体验版、手机删除旧体验版入口、重新扫码最新体验版二维码的 checklist。
4. 输出 DevTools Network 人工检查项：记录 DevTools 版本、基础库版本、运行策略、`urlCheck`、页面路径、请求域名、HTTP 状态、业务响应状态和资源加载结论，并说明不等同于体验版或真机网络验收。
5. 输出体验版 Network 人工检查项：确认最新体验版入口、重新扫码、生产 API 域名、首页或列表页加载、详情页或媒体资源加载结论；无法执行时记录 `blocked`、`follow_up` 或明确 `not_applicable`。

## Output

报告门禁结果、当前策略、`urlCheck=true` 状态、测试命令、生产接口 smoke、人工 checklist、DevTools Network 待执行项、体验版 Network 待执行项、下一步 `/miniapp-confirm` 或 `/miniapp-restore`。输出不得包含 token、Cookie、Authorization header、`.env`、真实密钥、真实客户数据或未脱敏隐私。

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

