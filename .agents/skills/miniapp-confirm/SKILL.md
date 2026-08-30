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

`--notes` 建议包含 DevTools Network 结论、体验版 Network 结论、失败项、阻塞项、剩余风险和下一步。缺少体验版 Network evidence 时，不得写作体验版或生产 `passed`；若当前确认仅覆盖开发阶段，可将体验版或生产证据缺口记录为 `production_only_pending`、`follow_up` 或明确的 `not_applicable_for_development`，并说明后续承接阶段。

## Steps

1. 确认渠道、版本和验证结果；缺失时询问用户。
2. 执行：

```bash
python scripts/miniapp-env.py confirm --channel <trial|release> --version <version> --result <passed|blocked|follow_up> --notes "<text>"
```

3. 输出可复制到 release、Sprint 验收报告或发布记录的安全摘要。
4. 若记录 Network evidence，摘要必须区分 `network_devtools` 与 `network_trial`，并不得包含 token、Cookie、Authorization header、`.env`、真实密钥、真实客户数据或未脱敏隐私。
5. 若当前证据来自开发者工具或开发环境，输出必须标注 `target_environment=development` 或等价说明，不得声称体验版、真机或生产发布通过。

## Output

报告确认结论、验证范围、DevTools Network 结论、体验版 Network 结论、失败项、阻塞项、剩余风险和下一步 `/miniapp-restore`。

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
