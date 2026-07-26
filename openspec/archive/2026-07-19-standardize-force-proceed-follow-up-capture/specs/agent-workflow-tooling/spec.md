## ADDED Requirements

### Requirement: Force-proceed follow-up Issue 默认不自动落盘
系统 MUST 将 `force-proceed` 与 follow-up Issue 创建解耦。命令在 `force-proceed` 场景发现后续需求、缺陷、风险或待办时，默认 MUST 只输出标准 capture 文案；除非用户在当前命令中明确授权自动创建，否则系统 MUST NOT 写入 `issues/requirements/**` 或 `issues/bugs/**`，MUST NOT 更新 Issue registry，MUST NOT 运行 `req.capture` 或 `bug.capture` Workflow Sync。

#### Scenario: force-proceed 未授权自动 capture
- **WHEN** 用户执行带有 `force-proceed` 语义的工作流命令
- **AND** 命令发现需要后续跟进的需求、缺陷或风险
- **AND** 用户未明确要求自动创建 follow-up Issue
- **THEN** 系统 MUST 完成当前命令允许继续的部分
- **AND** 系统 MUST 输出可用于 `/capture` 的标准文案
- **AND** 系统 MUST NOT 创建 REQ 或 BUG 文件

#### Scenario: 用户明确授权自动 capture
- **WHEN** 用户在当前命令中明确要求自动创建、记录或生成 follow-up Issue
- **AND** 命令已能判断 follow-up 类型为需求或缺陷
- **THEN** 系统 MAY 按 `/req-capture` 或 `/bug-capture` 规则创建对应 Issue
- **AND** 系统 MUST 运行对应 `req.capture` 或 `bug.capture` Workflow Sync
- **AND** 系统 MUST 在输出中列出创建的 Issue ID 与路径

#### Scenario: 类型不确定的 follow-up
- **WHEN** 命令发现 follow-up 事项但无法可靠判断其为需求或缺陷
- **THEN** 系统 MUST 输出 `/capture` 标准文案并标记类型倾向为 `待分类`
- **AND** 系统 MUST NOT 自动创建 REQ 或 BUG

### Requirement: Follow-up capture 文案标准化
系统 MUST 为未自动落盘的 follow-up 事项输出结构化 capture 文案，使用户可直接交给 `/capture`、`/req-capture` 或 `/bug-capture` 继续处理。

#### Scenario: 输出标准 capture 文案
- **WHEN** 工作流命令输出未落盘 follow-up 事项
- **THEN** 文案 MUST 包含建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令
- **AND** 文案 MUST 明确说明“未自动创建 Issue”

#### Scenario: 多个 follow-up 事项
- **WHEN** 工作流命令发现多个独立 follow-up 事项
- **THEN** 系统 MUST 分条输出标准 capture 文案
- **AND** 每条文案 MUST 能独立用于后续 capture
