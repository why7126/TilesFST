# sprint-planning-governance Specification

## Purpose
定义 Sprint 提议阶段的容量门禁与超限处理规则，确保 `/sprint-propose` 在范围明显超载时阻断正式规划，并在可接受缓冲区间内记录风险与延后建议。
## Requirements
### Requirement: Sprint 容量超限硬门禁
系统 SHALL 在 `/sprint-propose` 正式生成 Sprint 四件套或更新关联 trace 之前计算候选范围的容量占用率，并在估算工作量超过计划容量 120% 时阻断正式规划。

#### Scenario: 超过 120% 时阻断 Sprint 提议
- **WHEN** `/sprint-propose` 评估候选范围且 `estimated_person_days > capacity_person_days * 1.2`
- **THEN** 系统 MUST 不生成正式 `iterations/change/<sprint>/` 四件套
- **AND** 系统 MUST 不更新 REQ、BUG 或 Change trace 的 Sprint 关联
- **AND** 系统 MUST 提示需要拆分 Sprint、移出低优先级项或替换范围后重新评估

#### Scenario: 100% 到 120% 时允许带风险继续
- **WHEN** `/sprint-propose` 评估候选范围且 `capacity_person_days < estimated_person_days <= capacity_person_days * 1.2`
- **THEN** 系统 MUST 允许继续生成正式 Sprint 四件套
- **AND** 系统 MUST 在 Sprint 文档中记录容量风险、fix 缓冲影响和延后项建议

#### Scenario: 不超过容量时正常通过
- **WHEN** `/sprint-propose` 评估候选范围且 `estimated_person_days <= capacity_person_days`
- **THEN** 系统 MUST 按既有 Review Gate、Readiness Gate 和 Capacity Gate 继续生成 Sprint 四件套

### Requirement: Sprint 超限提示可执行
系统 SHALL 在 Sprint 容量超过 120% 时输出可执行的调整建议，而不是仅记录风险。

#### Scenario: 超限提示包含范围调整动作
- **WHEN** `/sprint-propose` 因容量超过 120% 阻断
- **THEN** 系统 MUST 明确列出至少一种范围调整动作：拆分 Sprint、移出低优先级项、替换范围
- **AND** 系统 MUST 提示调整后重新运行 `/sprint-propose`

### Requirement: Sprint 验收报告分层呈现
系统 SHALL 在 Sprint 验收报告中分层呈现最终验收摘要与原始 AC 引用，使最终归档判断不被历史未勾选 AC 干扰。

#### Scenario: 验收报告包含最终摘要和原始引用
- **WHEN** 系统生成或主动更新 `iterations/*/<sprint>/acceptance-report.md`
- **THEN** 报告 MUST 包含最终验收摘要或等价章节
- **AND** 报告 MUST 包含原始 AC 引用或等价章节
- **AND** 最终验收摘要 MUST 位于原始 AC 明细之前
- **AND** 报告 MUST 明确最终摘要用于归档判断，原始 AC 引用用于追溯和人工复核

#### Scenario: 最终摘要展示归档事实
- **WHEN** Sprint 验收报告表达 Sprint 是否可关闭
- **THEN** 最终验收摘要 MUST 展示 readiness gate 结果、Change 归档状态、tasks 完成情况和 Sprint 生命周期状态
- **AND** 最终验收摘要 MUST 支持读者不读取原始 AC 明细即可判断 Sprint 是否满足关闭条件

#### Scenario: 原始 AC 未勾选项有明确语义
- **WHEN** 原始 AC 引用区域包含 `- [ ]` 未勾选项
- **THEN** 系统 MUST 标明未勾选项属于待人工 sign-off、阻断归档或历史追溯
- **AND** 历史追溯类未勾选项 MUST NOT 自动覆盖最终验收摘要中的归档结论

### Requirement: Sprint 归档门禁保持独立
系统 SHALL 保持 `/sprint-archive` 的 readiness gate、Change archive、tasks 完成与 Workflow Sync 门禁独立于原始 AC 引用呈现方式。

#### Scenario: 归档门禁失败时阻断关闭
- **WHEN** `/sprint-archive` readiness gate、Change archive 或 tasks 完成检查失败
- **THEN** 系统 MUST 阻断 Sprint 关闭
- **AND** 最终验收摘要 MUST 记录阻断项

#### Scenario: 归档门禁通过但仍需人工复核
- **WHEN** `/sprint-archive` hard gates 均通过且存在人工 QA 复核项
- **THEN** 系统 MAY 将 Sprint 标记为 completed/archive
- **AND** 报告 MUST 将人工 QA 复核项记录为 sign-off open item 或遗留复核项
- **AND** 系统 MUST NOT 因历史追溯类未勾选 AC 自动回退 Sprint 状态

### Requirement: 验收报告派生同步不覆盖人工结论
系统 SHALL 限制 Workflow Sync 对 `acceptance-report.md` 的写入范围，避免自动刷新覆盖人工最终结论、验收人或 sign-off 说明。

#### Scenario: Workflow Sync 刷新验收报告
- **WHEN** Workflow Sync 更新 `acceptance-report.md`
- **THEN** 系统 MAY 刷新派生 note、issue 状态行和 Change 状态摘要
- **AND** 系统 MUST NOT 覆盖人工填写的最终验收结论、验收人或 sign-off 说明
- **AND** 系统 MUST NOT 将原始 AC 未勾选项自动解释为 Sprint 未完成

#### Scenario: Fact Sheet 提取验收信号
- **WHEN** Fact Sheet 或 Sprint 复盘流程读取 `acceptance-report.md`
- **THEN** 系统 MUST 优先读取最终验收摘要和最终归档检查中的状态信号
- **AND** 系统 SHOULD 将原始 AC 引用中的孤立未完成文本作为证据提示而非 Sprint 完成状态事实源

### Requirement: Sprint close stale scan 门禁
系统 SHALL 在 Sprint close 或 `/sprint-archive` 归档判断前检查目标 Sprint 四件套和正式范围关联 Issue 子文档中的过期中间态文案和旧归档路径残留，防止 Sprint 完成结论与真实 Issue、Change 生命周期状态不一致。该门禁 SHALL 保留对真实流程中间态的阻断，同时避免把普通业务正文中的 `pending` 等业务词误判为流程状态。

#### Scenario: 四件套存在过期中间态文案时阻断关闭
- **WHEN** 系统检查目标 Sprint 的 `sprint.md`、`release-note.md`、`acceptance-report.md` 或 `sprint.yaml`
- **AND** 文档中存在与真实状态冲突的“待 `/req-opsx`”、“待 `/bug-opsx`”、“待 `/opsx-apply`”、`proposed`、`applied` 或等价中间态文案
- **AND** 对应 Issue 或 Change 已进入更后续的生命周期状态
- **THEN** 系统 MUST 将该命中标记为 blocker
- **AND** `/sprint-archive` 或 Sprint close 命令 MUST 返回非零退出码
- **AND** 报告 MUST 列出文件路径、命中片段、关联 Issue 或 Change、真实状态和建议修复动作

#### Scenario: Issue 子文档普通业务词不阻断关闭
- **WHEN** 系统检查目标 Sprint 正式范围关联的已闭环 Issue 子文档
- **AND** 普通正文中出现“SKU pending 图片正式化”或等价业务词
- **AND** 该内容不表达当前 Issue、验收、Change 或 Sprint 的流程中间态
- **THEN** 系统 MUST NOT 因该业务词阻断 Sprint close

#### Scenario: Issue 子文档状态字段仍阻断关闭
- **WHEN** 系统检查目标 Sprint 正式范围关联的已闭环 Issue 子文档
- **AND** frontmatter、fenced yaml、状态表格或验收结果字段残留 `status: pending_review`、`acceptance_status: pending`、`proposed`、`applied`、`in_sprint` 或等价流程中间态
- **THEN** 系统 MUST 将该命中标记为 blocker
- **AND** 报告 MUST 提供 Workflow Sync/reconcile 或人工修正建议

#### Scenario: 四件套引用旧归档路径时阻断关闭
- **WHEN** 系统检查目标 Sprint 四件套
- **AND** `sprint.md`、`release-note.md`、`acceptance-report.md` 或 `sprint.yaml` 将 `openspec/changes/archive/` 作为归档事实路径或新生成引用
- **THEN** 系统 MUST 将该命中标记为 blocker
- **AND** 报告 MUST 提示使用 `openspec/archive/YYYY-MM-DD-<change-id>/`

#### Scenario: 无 stale 命中时允许继续关闭
- **WHEN** 目标 Sprint 四件套和关联 Issue 子文档不存在 blocker 级 stale 文案或旧归档路径残留
- **AND** 既有 readiness gate、Change archive、tasks 完成和 Workflow Sync 门禁均通过
- **THEN** 系统 MUST 允许 Sprint close 或 `/sprint-archive` 继续执行

### Requirement: Sprint 目标编号列表与正式 Scope 一致
系统 SHALL 在 Sprint Scope 校验中确认 `sprint.md` 的 Sprint 目标编号列表覆盖 Sprint 正式范围中的 REQ、BUG 和必须显式展示的 Change。

#### Scenario: REQ 缺失于目标编号列表时校验失败
- **WHEN** `sprint.yaml.requirements` 包含某个 REQ
- **AND** `sprint.md` 的 Sprint 目标编号列表未包含该 REQ 的完整 ID 或短编号
- **THEN** `validate-sprint-scope.py <sprint-id>` MUST 返回失败
- **AND** 报告 MUST 列出缺失的 REQ ID
- **AND** 报告 MUST 指出缺失位置为 `sprint.md Sprint target id list`

#### Scenario: BUG 缺失于目标编号列表时校验失败
- **WHEN** `sprint.yaml.bugs` 包含某个 BUG
- **AND** `sprint.md` 的 Sprint 目标编号列表未包含该 BUG 的完整 ID 或短编号
- **THEN** `validate-sprint-scope.py <sprint-id>` MUST 返回失败
- **AND** 报告 MUST 列出缺失的 BUG ID

#### Scenario: 短编号与完整 ID 等价
- **WHEN** `sprint.yaml.requirements` 包含 `REQ-0100-mintlify-docs-site-ia-content-experience`
- **AND** `sprint.md` 的 Sprint 目标编号列表包含 `REQ-0100`
- **THEN** 系统 MUST 将该目标编号视为已覆盖

#### Scenario: 目标编号列表完整时校验通过
- **WHEN** `sprint.yaml` 中的 REQ、BUG 和必须显式展示的 Change 都出现在 Sprint 目标编号列表中
- **AND** `## 2. Scope` 主表与 Workflow Sync 分组表也覆盖正式范围
- **THEN** `validate-sprint-scope.py <sprint-id>` MUST 返回通过

### Requirement: Sprint 目标编号列表解析边界明确
系统 SHALL 只从 `sprint.md ## 1. 目标` 中的「Sprint 目标编号列表」连续 Markdown 列表解析目标编号，不得把其他章节中的编号作为目标列表证据。

#### Scenario: Scope 表编号不得作为目标列表证据
- **WHEN** 某个 REQ 只出现在 `sprint.md ## 2. Scope` 主表或 Workflow Sync 分组表
- **AND** 该 REQ 未出现在 Sprint 目标编号列表中
- **THEN** 系统 MUST 判定该 REQ 缺失于目标编号列表

#### Scenario: 目标编号列表缺失时报告格式异常
- **WHEN** `sprint.md ## 1. 目标` 中不存在「Sprint 目标编号列表」或无法解析连续列表
- **THEN** `validate-sprint-scope.py <sprint-id>` MUST 返回失败
- **AND** 报告 MUST 提示目标编号列表缺失或格式异常

#### Scenario: 聚焦校验覆盖目标编号列表
- **WHEN** 用户运行 `validate-sprint-scope.py <sprint-id> --item <id>`
- **THEN** 系统 MUST 对该 `<id>` 同时执行 Scope 主表、Workflow Sync 分组表和目标编号列表校验

### Requirement: Sprint 提议完成前同步目标编号列表
系统 SHALL 要求 `/sprint-propose` 在新建、追加或修正 Sprint 正式范围后同步 `sprint.md` 的 Sprint 目标编号列表，并以增强后的 Scope 校验作为完成门禁。

#### Scenario: 新增 REQ 后目标编号列表同步
- **WHEN** `/sprint-propose` 将已评审 REQ 纳入 Sprint 正式范围
- **THEN** `sprint.yaml.requirements` MUST 包含该 REQ
- **AND** `sprint.md` 的 Sprint 目标编号列表 MUST 包含该 REQ 的完整 ID 或短编号
- **AND** `/sprint-propose` 结束前 MUST 运行 `validate-sprint-scope.py <sprint-id> --item <REQ-id>`

#### Scenario: 校验失败时不得完成 Sprint 提议
- **WHEN** `/sprint-propose` 最终运行 `validate-sprint-scope.py` 发现目标编号列表缺失正式范围项
- **THEN** `/sprint-propose` MUST 停止并报告失败
- **AND** 系统 MUST 提示补齐目标编号列表或修复 `sprint.yaml` 后重跑校验

#### Scenario: Workflow Sync 边界保持清晰
- **WHEN** Workflow Sync 刷新 `sprint.md`
- **THEN** 系统 MUST 继续维护 `## 2. Scope` 主表与 Workflow Sync marker 分组表
- **AND** 系统 MUST NOT 静默掩盖 Sprint 目标编号列表与正式 Scope 的不一致

### Requirement: 已评审 Issue 优先纳入 Sprint
系统 SHALL 将已评审 REQ/BUG 的推荐推进顺序定义为先纳入 Sprint 正式范围，再创建或回填 OpenSpec Change。未评审 REQ/BUG 仍不得进入 Sprint 正式范围；已纳入 Sprint 的 REQ/BUG 在后续 `/req-opsx` 或 `/bug-opsx` 创建 Change 时，系统 MUST 将 Change 回填到同一 Sprint 的机器事实源。

#### Scenario: REQ 评审通过后的推荐下一步
- **WHEN** `/req-review REQ-xxxx --approve` 成功将需求评审为 `approved`
- **THEN** 命令输出 MUST 将 `/sprint-propose <sprint-id> --req REQ-xxxx` 作为优先下一步
- **AND** 命令输出 MUST NOT 将 `/req-opsx REQ-xxxx` 表达为优先下一步
- **AND** 若缺少目标 Sprint、容量或范围信息，输出 MUST 将这些内容列为待用户决策或处理点

#### Scenario: BUG 评审通过后的推荐下一步
- **WHEN** `/bug-review BUG-xxxx --approve` 成功将缺陷评审为 `approved`
- **THEN** 命令输出 MUST 将 `/sprint-propose <sprint-id> --bug BUG-xxxx` 作为优先下一步
- **AND** 命令输出 MUST NOT 将 `/bug-opsx BUG-xxxx` 表达为优先下一步
- **AND** 若缺少目标 Sprint、修复优先级或容量信息，输出 MUST 将这些内容列为待用户决策或处理点

#### Scenario: Sprint 已纳入后创建 Change
- **WHEN** 已评审 REQ/BUG 已通过 `/sprint-propose` 纳入 `iterations/change/<sprint-id>/sprint.yaml`
- **AND** 用户执行 `/req-opsx` 或 `/bug-opsx`
- **THEN** Workflow Sync MUST 将新建 Change 写入同一 Sprint 的 `changes[]`
- **AND** Workflow Sync MUST 同步对应 `scope_estimates[].change`
- **AND** 系统 MUST 移除或更新该 Issue 的“待创建 Change”提示

#### Scenario: 未评审 Issue 仍被阻断
- **WHEN** REQ/BUG 未处于 `approved`、`in_sprint` 或后续交付态
- **AND** 用户尝试执行 `/sprint-propose` 将其纳入正式范围
- **THEN** 系统 MUST 阻断正式纳入
- **AND** 输出 MUST 提供可执行评审命令作为下一步

### Requirement: Sprint scope 支持待 Change 的已评审 Issue
系统 SHALL 允许 `/sprint-propose` 将已评审但尚未创建 OpenSpec Change 的 REQ/BUG 纳入正式 Sprint 范围，并在 Sprint 文档和机器事实源中保留后续 `/req-opsx` 或 `/bug-opsx` 的可执行引导。

#### Scenario: 已评审 REQ 尚未创建 Change
- **WHEN** `/sprint-propose` 纳入一个 `approved` REQ
- **AND** 该 REQ 的 `openspec_changes` 为空
- **THEN** `sprint.yaml` MUST 在 `requirements[]` 中记录该 REQ
- **AND** Sprint 输出 MUST 提示下一步执行 `/req-opsx REQ-xxxx`
- **AND** 后续 `/opsx-apply` 仍 MUST 等待 Change 回填到 `changes[]` 后才能继续

#### Scenario: 已评审 BUG 尚未创建 Change
- **WHEN** `/sprint-propose` 纳入一个 `approved` BUG
- **AND** 该 BUG 的 `openspec_changes` 为空
- **THEN** `sprint.yaml` MUST 在 `bugs[]` 中记录该 BUG
- **AND** Sprint 输出 MUST 提示下一步执行 `/bug-opsx BUG-xxxx`
- **AND** 后续 `/opsx-apply` 仍 MUST 等待 Change 回填到 `changes[]` 后才能继续

