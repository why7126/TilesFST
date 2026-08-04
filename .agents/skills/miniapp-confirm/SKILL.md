---
name: "miniapp-confirm"
description: "记录小程序体验版或正式版验证确认结论"
---

# miniapp-confirm

Use this skill when the user asks `/miniapp-confirm` or wants to record trial/release verification results for the miniapp.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；只读取小程序环境配置、脚本和相关发布记录片段。
- 不记录敏感信息、微信会话密钥、Cookie、Authorization header、`.env` 内容或真实用户隐私。

## Input

Recommended flags:

```text
--channel trial|release
--version <version>
--result passed|blocked|follow_up
--notes <text>
```

`--notes` 建议包含 DevTools Network 结论、体验版 Network 结论、失败项、阻塞项、剩余风险和下一步。缺少体验版 Network evidence 时，不得写作 `passed`；应使用 `blocked`、`follow_up` 或明确的 `not_applicable` 原因。

## Steps

1. 确认渠道、版本和验证结果；缺失时询问用户。
2. 执行：

```bash
python scripts/miniapp-env.py confirm --channel <trial|release> --version <version> --result <passed|blocked|follow_up> --notes "<text>"
```

3. 输出可复制到 release、Sprint 验收报告或发布记录的安全摘要。
4. 若记录 Network evidence，摘要必须区分 `network_devtools` 与 `network_trial`，并不得包含 token、Cookie、Authorization header、`.env`、真实密钥、真实客户数据或未脱敏隐私。

## Output

报告确认结论、验证范围、DevTools Network 结论、体验版 Network 结论、失败项、阻塞项、剩余风险和下一步 `/miniapp-restore`。
