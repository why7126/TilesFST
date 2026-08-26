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

命令结束前，最终回复必须包含面向用户的真实结果，不得输出本段规则、尖括号占位符、MUST/SHOULD 规范语句或与当前命令无关的通用示例。

输出必须包含两项：

- `下一步`：写真实、可复制的下一条命令；若当前没有可推进动作，写“暂无可推进下一步”。
- `待用户决策/处理`：没有额外人工事项时写“无”；否则只列具体的缺失输入、范围/策略选择、证据补充、验收确认、发布确认、生产实施确认、阻塞项或人工处理事项。

输出判定：

- 有唯一可执行下一步时，`下一步` 写真实命令；若无额外人工事项，`待用户决策/处理` 写“无”。
- 下一步被用户选择、补证、验收、发布确认、生产实施确认或阻塞项卡住时，`下一步` 写“暂无可推进下一步”，并在 `待用户决策/处理` 列出具体阻塞事项。
- 已有下一步且仍有额外人工事项时，`待用户决策/处理` 只列命令之外的事项，不得重复 `下一步` 中的命令或动作。
- REQ 链路使用完整原始 `REQ-*`；BUG 链路使用完整原始 `BUG-*`；非 REQ/BUG 的直接 Change 才使用真实 Change ID。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。

