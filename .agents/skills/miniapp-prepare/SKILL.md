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

## Steps

1. 执行：

```bash
python scripts/miniapp-env.py prepare
```

2. 如 sandbox 阻止 uv 缓存或外网 smoke，按审批规则重跑必要命令。
3. 输出微信开发者工具上传、公众平台设为体验版、手机删除旧体验版入口、重新扫码最新体验版二维码的 checklist。

## Output

报告门禁结果、当前策略、`urlCheck=true` 状态、测试命令、生产接口 smoke、人工 checklist、下一步 `/miniapp-confirm` 或 `/miniapp-restore`。
