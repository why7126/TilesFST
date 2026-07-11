## ADDED Requirements

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
