## ADDED Requirements

### Requirement: Agent 命令需求偏差阶段分流

`/capture`、`/explore` 与 `/opsx-modify` MUST 在处理已有关联 REQ、BUG、Change 或 Sprint 的“不如预期”反馈时，先判断目标 Change 与 Sprint 生命周期阶段，再决定使用验收返修、BUG capture 或 REQ capture。

#### Scenario: Active Change 内验收返修

- **GIVEN** 反馈关联的 Change 已完成 `/opsx-apply`
- **AND** 该 Change 尚未 `/opsx-archive`
- **AND** 反馈仍属于原需求、原 Change、原验收项或原能力边界
- **WHEN** AI 判断后续命令
- **THEN** AI MUST 推荐 `/opsx-modify <REQ-id|BUG-id|change-id> <反馈>`
- **AND** `/capture` MUST NOT 为该反馈自动创建新的 REQ 或 BUG

#### Scenario: Active Change 范围外反馈

- **GIVEN** 反馈关联的 Change 尚未归档
- **AND** 反馈新增原需求未包含的功能，或改变 API、DB、权限、部署、对象存储边界，或构成影响范围超出当前 Change 的独立缺陷
- **WHEN** AI 判断后续命令
- **THEN** AI MUST 停止 `/opsx-modify`
- **AND** AI MUST 推荐 `/capture`、`/req-capture` 或 `/bug-capture`
- **AND** 若反馈是已承诺行为的偏差，BUG SHOULD 记录 `related_requirement`

#### Scenario: Change 已归档但 Sprint 未归档

- **GIVEN** 原 REQ 或 Change 已归档
- **AND** 所属 Sprint 仍在 `iterations/change/`
- **WHEN** 用户发现已交付能力与预期不符
- **THEN** AI MUST NOT 推荐 `/opsx-modify`
- **AND** AI SHOULD 推荐 `/bug-capture` 并关联原 REQ
- **AND** 若反馈是新增能力或体验增强，AI SHOULD 推荐 `/req-capture`

#### Scenario: Sprint 已归档后的反馈

- **GIVEN** 所属 Sprint 已归档到 `iterations/archive/`
- **WHEN** 用户提出已交付能力偏差或新增期望
- **THEN** AI MUST 将该反馈作为新的生命周期输入处理
- **AND** 已交付能力偏差 SHOULD 走 `/bug-capture`
- **AND** 新增期望 SHOULD 走 `/req-capture`
