## 设计说明

本次优化不新增脚本和业务实现，只把已存在的生命周期门禁固化为命令内可直接执行的分流规则。

## 分流原则

需求相关“不如预期”先判断当前偏差是否仍属于一个 active Change 的验收返修：

| 判断问题 | 结果 |
|---|---|
| 目标 Change 是否已 `/opsx-apply` 且未 `/opsx-archive`？ | 是则可能进入 `/opsx-modify` |
| 反馈是否仍属于原需求、原 Change、原验收项或原能力边界？ | 是则优先 `/opsx-modify` |
| 反馈是否新增原需求未包含的功能、改变 API/DB/权限/部署/对象存储边界，或是独立缺陷？ | 停止 `/opsx-modify`，转 `/capture`、`/req-capture` 或 `/bug-capture` |
| 原 REQ/Change 是否已归档？ | 不再返修原 Change；偏差走 BUG，增强走 REQ |
| 所属 Sprint 是否已归档？ | 后续输入全部作为新生命周期条目处理 |

## 命令边界

- `/explore` 只读输出类型倾向和建议命令，不落盘。
- `/capture` 在落盘前按阶段分流，若应由 active Change 返修承接，则不创建 REQ/BUG，提示 `/opsx-modify`。
- `/opsx-modify` 只允许 active Change 内验收返修；若超出边界，必须停止并给出标准 capture 文案。

## 文档同步

- 技能文件直接承载命令运行规则。
- OpenSpec delta 记录为 `agent-workflow-tooling` 的治理要求，供归档后合并为正式规格。
- `docs/spec-logs/` 记录本次治理迭代事实和跨项目复用提示。
