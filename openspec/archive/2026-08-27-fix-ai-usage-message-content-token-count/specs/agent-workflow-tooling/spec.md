## MODIFIED Requirements

### Requirement: 用户消息级命令运行边界

系统 SHALL 将一次用户消息驱动的 AI 执行过程定义为一条 AI command run，并记录 started_at、ended_at、command、workflow_event、requirements、bugs、changes、sprint_id 与 attribution_confidence。

#### Scenario: 新版 message content 列表建立 command run

- **GIVEN** Codex session JSONL 包含 `payload.type=message` 且 `payload.role=user` 的用户消息
- **AND** 用户消息的 `payload.content` 是文本片段列表
- **WHEN** AI usage extractor 解析该 session JSONL
- **THEN** 系统 SHALL 从文本片段中提取用户命令文本并建立 command run
- **AND** 系统 SHALL 根据该命令文本识别 workflow_event、BUG、REQ、Change 与 Sprint 归因
- **AND** 系统 SHALL NOT 要求原始 session JSONL 写入仓库

### Requirement: AI 命令 Token 与执行指标聚合

系统 SHALL 在 command run 维度聚合模型调用次数、输入 token、输出 token、cached input token、reasoning output token、总 token、工具调用次数、工具耗时、失败次数与重试次数。

#### Scenario: 新版 token_count 归属到 message content command run

- **GIVEN** 同一 session JSONL 中先出现新版 `payload.type=message` 用户消息
- **AND** 后续出现 `payload.type=token_count` 事件
- **AND** token 用量位于 `payload.info.last_token_usage`
- **WHEN** AI usage extractor 解析这些事件
- **THEN** 系统 SHALL 将 token_count 事件归属到最近的用户 command run
- **AND** 系统 SHALL 累计 `model_call_count` 与 token totals
- **AND** 系统 SHALL NOT 因 command run 边界缺失产生空 snapshot
- **AND** 系统 SHALL NOT 将 session 级 `total_token_usage` 当作单条 command run 成本

### Requirement: Sprint 复盘 AI 使用量矩阵

系统 SHALL 在 Sprint AI Usage 矩阵中区分真实数值 `0` 与未采集或未归因的 workflow 阶段。

#### Scenario: 未观测 workflow 阶段展示为短横线

- **GIVEN** Sprint AI Usage snapshot 只包含部分 workflow_event 的 command run
- **WHEN** Fact Sheet 渲染 Sprint AI Usage 矩阵
- **THEN** 系统 SHALL 将没有任何 command run 覆盖的 workflow 列标记为 `unknown`
- **AND** 系统 SHALL 将未观测 workflow 阶段渲染为 `-`
- **AND** 系统 SHALL NOT 将未观测 workflow 阶段渲染为普通 `0`
- **AND** 系统 SHALL 保留已观测 workflow 列中的真实 `0` 数值

#### Scenario: post-command hook 同分候选优先真实 token run

- **GIVEN** 同一 session 中存在多个与目标 workflow、Sprint、Issue 或 Change 上下文同分匹配的 command run
- **AND** 其中至少一个 run 具有非零 token 或模型调用指标
- **WHEN** post-command hook 选择目标 run 并补充显式上下文
- **THEN** 系统 SHALL 优先选择具有非零 token 或模型调用指标的 run
- **AND** 系统 SHALL NOT 因同分排序误选零 token turn

#### Scenario: Sprint 矩阵对象行裁剪到正式 scope

- **GIVEN** Sprint AI Usage snapshot 的 command run 同时关联当前 Sprint scope 内对象与历史相关对象
- **WHEN** 系统聚合 Sprint usage coverage 与矩阵对象行
- **THEN** 系统 SHALL 仅保留 `sprint.yaml` 正式 scope 内的 REQ、BUG 与 Change
- **AND** 系统 SHALL NOT 将未纳入当前 Sprint 的历史相关 REQ/BUG 渲染为当前 Sprint 矩阵对象行
