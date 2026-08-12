## ADDED Requirements

### Requirement: Issue 生命周期与索引治理

系统 SHALL 使用 `issues/requirements/` 与 `issues/bugs/` 下的阶段目录、registry、trace、Sprint 四件套和 OpenSpec Change 共同维护 Issue 生命周期事实源。

#### Scenario: 维护当前态看板索引

- **GIVEN** REQ 或 BUG 发生 capture、生成、补齐、评审、纳入 Sprint、创建 Change、apply、archive 或状态同步
- **WHEN** 对应命令完成
- **THEN** 命令 SHOULD 更新 `issues/requirements/CHANGELOG.md` 或 `issues/bugs/CHANGELOG.md` 中该 Issue 的当前态行
- **AND** 当前态行 SHOULD 包含状态、阶段、关联 Sprint、关联 Change、最近更新时间、下一步和事实源路径
- **AND** 当前态看板不得替代 `_registry.yaml`、单条 `trace.md`、Sprint 四件套或 OpenSpec Change 作为机器事实源
