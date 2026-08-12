## 设计

`/spec-study` 的输出分为三类：

| 输出 | 是否落盘为 study 报告 | 说明 |
|---|---|---|
| 学习阶段候选内容 | 否 | 用最终回复或 active Change 文档承载，等待用户确认。 |
| 应用完成后的学习报告 | 是 | 只生成一份 `YYYYMMDDhhmmss-study-xxx.md`。 |
| 对同一流程的补充、修正、验证回填 | 否 | 更新同一份 study 报告，不创建第二份。 |
| 治理资产应用结果 | 是 | 汇总进同一份 study 报告，不额外创建重复的 governance 日志。 |

## 去重规则

- 同一次 `/spec-study` 流程以学习对象、学习主题和用户确认批次作为去重边界。
- 若学习阶段已预先创建 study 报告，应用完成时必须更新该报告，不得再创建一份最终报告。
- 若应用阶段尚未存在 study 报告，才创建一份正式报告。
- `/spec-study` 触发的治理资产应用属于学习报告内容，不再额外生成 `YYYYMMDDhhmmss-governance-xxx.md`。
- 报告文件仍需遵守 `docs/spec-logs/` 命名、隐私禁写、本机绝对路径禁写和脱敏规则。

## 边界

- 本规则约束 `/spec-study` 在 `docs/spec-logs/` 下的正式报告数量和类型。
- 独立 `/spec-opt` 治理变更仍按自身规则生成 `governance` 日志。
- 不限制最终回复中展示候选内容，也不限制 active OpenSpec Change 中维护 proposal、design、tasks、trace、acceptance 或 test-plan。
- 不修改业务 `src/`。
