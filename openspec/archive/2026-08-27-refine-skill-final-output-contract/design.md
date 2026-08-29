## 设计目标

命令最终回复只向用户展示执行结果和下一步，不展示内部规范模板。输出契约需要让 Agent 在结束前完成三件判断：

1. 当前是否存在唯一可执行下一步。
2. 是否被用户选择、补证、验收、发布确认或阻塞项卡住。
3. 【待用户决策/处理】是否只包含额外人工事项，而不是重复【下一步】命令。

## 输出三态

| 状态 | 下一步 | 待用户决策/处理 |
|---|---|---|
| 有唯一可执行命令 | 写真实命令，例如 `/opsx-apply REQ-0123-upload-stage-trace-spans` | 无 |
| 被用户决策阻塞 | 暂无可推进下一步 | 写需要选择、补充或确认的事项 |
| 有命令且有额外人工事项 | 写真实命令 | 只写命令之外的人工事项 |

## 命令族示例策略

- REQ 链路使用完整原始 `REQ-*`，例如 `/req-generate REQ-0123-upload-stage-trace-spans`、`/opsx-apply REQ-0123-upload-stage-trace-spans`。
- BUG 链路使用完整原始 `BUG-*`，例如 `/bug-complete BUG-0144-miniapp-usage-events-overreporting`、`/opsx-archive BUG-0144-miniapp-usage-events-overreporting`。
- 非 REQ/BUG 的直接 Change 才使用真实 `<change-id>` 对应的实际值，例如 `/opsx-apply refine-skill-final-output-contract`。
- 发布、镜像、升级命令使用实际版本和计划路径，例如 `/release-prepare v1.2.0`、`/upgrade-validate --plan releases/v1.2.0/upgrade-plans/fresh-to-v1.2.0.json`。

## 禁止模式

- 不在最终回复输出尖括号占位符，例如 `<可直接执行的命令>` 或 `<需要用户选择...>`。
- 不在非 BUG 命令中使用通用 `/bug-review BUG-0122` 示例。
- 不把“确认是否执行下一步命令”作为待处理项；若下一步已经可执行，待处理应为“无”或额外人工事项。
- 不在用户可见最终回复中输出 `MUST`、`SHOULD`、`Final Output Contract` 等规范语气，除非用户正在询问规范本身。

## 校验策略

`validate-agent-context-budget.py` 在既有预算、Sprint gate 和 REQ/BUG 参数校验基础上新增输出契约卫生检查：

- 技能最终输出契约不得包含可被照抄的尖括号模板。
- 技能最终输出契约不得继续使用通用 BUG 示例作为所有命令族示例。
- `/sprint-propose`、`/req-opsx`、`/bug-opsx` 不得保留会诱发重复确认的旧 Output 示例。
- `/upgrade-plan`、`/upgrade-validate` 必须补齐与其他命令一致的待处理范围定义。

## 取舍

- 已采纳：批量统一 Final Output Contract 文案，减少命令之间漂移。
- 已采纳：保留命令族专属示例，帮助 Agent 输出真实下一步。
- 未采纳：只依赖现有“不得重复”一句话；原因是它不能阻止占位符和通用示例被原样输出。
- 未采纳：为每个命令设计完全不同的契约；原因是会增加维护成本，统一三态判定更稳定。
