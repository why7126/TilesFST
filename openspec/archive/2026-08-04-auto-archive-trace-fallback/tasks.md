## 1. 归档证据模型

- [x] 1.1 梳理现有归档证据校验、Workflow Sync 归档时间解析、Sprint close readiness 和 Fact Sheet 对 `trace.md` 的读取路径。
- [x] 1.2 在归档证据校验脚本或共享模块中定义最小归档 trace 与结构化 fallback 摘要的数据字段。
- [x] 1.3 实现 archived Change 缺少 `trace.md` 时的最小事实收集逻辑，覆盖归档目录名、`tasks.md`、delta spec、proposal/design 和关联 Issue trace。

## 2. 自动补齐与 fallback

- [x] 2.1 在归档目录可写且事实足够时生成最小 `trace.md`，并标记自动生成来源、归档路径、状态、时间来源和任务完成摘要。
- [x] 2.2 在不可写或不适合写入时输出结构化 fallback 摘要，确保调用方可机器判定证据闭环。
- [x] 2.3 在事实不足时保持非零退出码，并报告缺失字段、已检查路径和建议人工补齐动作。

## 3. 工作流接入

- [x] 3.1 调整 `/opsx-archive` 相关技能说明或脚本调用，报告 `trace-present`、`auto-generated-minimal-trace`、`fallback-summary-pass` 和 blocker 状态。
- [x] 3.2 确认 Sprint close readiness、Workflow Sync 或 Fact Sheet 消费归档证据时识别新的最小 trace 与结构化 fallback 结果。
- [x] 3.3 确认 legacy archive path、incomplete tasks、缺失 tasks 和 Issue 未闭环门禁不被 fallback 逻辑放宽。

## 4. 测试与校验

- [x] 4.1 增加 pytest 覆盖可写归档目录自动生成最小 `trace.md`。
- [x] 4.2 增加 pytest 覆盖不可写或不写入场景输出结构化 fallback 摘要。
- [x] 4.3 增加 pytest 覆盖证据不足时保持 blocker，以及 incomplete tasks 等既有 blocker 不被误放行。
- [x] 4.4 运行相关 pytest、`python scripts/validate-openspec-language.py` 和必要的 OpenSpec / 目录校验，修复发现的问题。
