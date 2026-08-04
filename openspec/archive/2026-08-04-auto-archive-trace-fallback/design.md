## 上下文

当前归档链路已经要求 canonical archive path 使用 `openspec/archive/YYYY-MM-DD-<change-id>/`，并通过归档证据校验确认 archived Change 具备 `trace.md` 或 `## 归档验证摘要`。但历史归档 Change 可能没有 `trace.md`，且并非每个历史目录都适合由人工立即补写完整 trace。缺少 trace 会影响 `/opsx-archive` 的闭环报告、Sprint close readiness、Workflow Sync 归档时间推断和复盘 Fact Sheet。

这次变更只处理归档证据韧性，不重新定义 OpenSpec 目录结构，不迁移历史 archive，不放宽 incomplete tasks、legacy archive path 或 issue 状态门禁。

## 目标 / 非目标

**目标：**

- 归档证据校验遇到 archived Change 缺少 `trace.md` 时，优先自动生成最小归档 trace。
- 最小归档 trace 必须使用项目标准时间格式，并明确标注其来源为自动补齐，避免伪装成人工执行原始记录。
- 当无法安全写入或证据不足时，工具必须输出结构化 fallback 摘要，供当前命令报告、readiness gate 或人工复核使用。
- 保留现有阻断语义：如果既不能生成 trace，也不能形成完整 fallback 摘要，归档证据校验仍然失败。

**非目标：**

- 不为所有历史归档 Change 批量补写完整 trace。
- 不改变 `openspec/archive/YYYY-MM-DD-<change-id>/` 的归档路径规则。
- 不修改业务 API、数据库、Web、微信小程序或 MinIO 行为。
- 不把结构化 fallback 当作长期优先事实源；可写场景仍以 `trace.md` 为首选证据。

## 关键决策

1. **优先生成最小 `trace.md`，而不是只在报告中豁免。**
   - 原因：`trace.md` 是现有 Workflow Sync、归档时间解析和人工回读的稳定入口；补齐后后续命令无需重复处理同一个缺口。
   - 替代方案：只允许 `proposal.md`、`design.md` 或 `tasks.md` 中的 `## 归档验证摘要`。该方案对不可写归档有价值，但可写目录下会让证据入口继续分散。

2. **最小 trace 使用可推断事实，不生成无法确认的验收结论。**
   - 需要记录的事实包括 Change ID、归档路径、归档状态、归档时间来源、tasks 完成度、delta spec 文件清单和 fallback 来源。
   - 无法确认的字段标记为 `unknown` 或“待人工复核”，不得写成已验收通过。

3. **结构化 fallback 摘要必须机器可读且字段固定。**
   - fallback 至少包含 `change_id`、`archive_path`、`evidence_status`、`archive_timestamp`、`timestamp_source`、`tasks_done`、`tasks_total`、`spec_delta_paths`、`warnings` 和 `recommended_action`。
   - 这样 readiness gate、测试和命令输出可以用同一结构判断是否闭环，而不是解析自由文本。

4. **校验脚本负责生成或报告，调用方负责展示摘要。**
   - `scripts/validate-archive-evidence.py` 或等价模块应集中实现证据解析、最小 trace 写入、fallback 构建和退出码判断。
   - `/opsx-archive`、Sprint close readiness、Workflow Sync 或 Fact Sheet 只消费结果，避免多处重复拼装 trace。

## 风险 / 取舍

- **风险：自动 trace 被误认为原始历史记录。** → 在 Frontmatter 和正文中标记 `source: auto_generated_minimal_archive_trace`，并写明生成命令与证据来源。
- **风险：归档目录不可写导致命令继续缺少持久证据。** → 输出结构化 fallback 摘要并给出 recommended action；若 fallback 字段不完整则保持非零退出。
- **风险：历史 tasks 或 proposal 缺失造成归档时间推断不稳定。** → 时间优先级使用现有 trace、Issue trace、归档目录日期，无法推断时使用 `unknown` 并要求人工复核。
- **风险：为兼容历史缺口而放宽真实失败。** → incomplete tasks、缺失 tasks、legacy archive path、Issue 未闭环仍按现有门禁阻断。
