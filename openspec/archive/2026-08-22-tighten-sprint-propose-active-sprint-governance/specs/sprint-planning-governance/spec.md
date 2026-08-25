## ADDED Requirements

### Requirement: Sprint 提议默认选择当前 Sprint

系统 SHALL 在 `/sprint-propose` 未指定 Sprint 时根据 active Sprint 数量确定默认目标，并避免含糊地创建或修改错误 Sprint。

#### Scenario: 无 active Sprint 时自动创建下一个连续编号

- **WHEN** 用户运行 `/sprint-propose` 且未指定 `--sprint`
- **AND** `iterations/change/` 下不存在 `sprint-[0-9]{3}` active Sprint
- **THEN** 系统 MUST 扫描 `iterations/archive/` 与 `iterations/change/` 下符合 `sprint-[0-9]{3}` 的目录和 `sprint.yaml:sprint_id`
- **AND** 系统 MUST 取最大编号加一作为新 Sprint ID
- **AND** 系统 MUST 将新 Sprint 创建到 `iterations/change/<next-sprint>/`

#### Scenario: 一个 active Sprint 时默认使用当前 Sprint

- **WHEN** 用户运行 `/sprint-propose` 且未指定 `--sprint`
- **AND** `iterations/change/` 下仅存在一个 `sprint-[0-9]{3}` active Sprint
- **THEN** 系统 MUST 默认使用该 Sprint 作为当前 Sprint
- **AND** 系统 MUST NOT 默认创建并行 Sprint

#### Scenario: 多个 active Sprint 时要求显式指定

- **WHEN** 用户运行 `/sprint-propose` 且未指定 `--sprint`
- **AND** `iterations/change/` 下存在两个或以上 `sprint-[0-9]{3}` active Sprint
- **THEN** 系统 MUST 阻断命令
- **AND** 输出 MUST 引导用户使用 `/sprint-propose --sprint <sprint-id>` 指定当前 Sprint

### Requirement: Sprint 新建必须连续编号

系统 SHALL 禁止跳号创建 Sprint，并限制 active Sprint 数量，避免迭代事实源出现不可解释的空洞或并行膨胀。

#### Scenario: 指定新 Sprint 必须为最大编号加一

- **WHEN** 用户运行 `/sprint-propose --sprint <sprint-id>`
- **AND** `<sprint-id>` 尚不存在于 active Sprint
- **THEN** 系统 MUST 校验 `<sprint-id>` 等于 `iterations/archive/` 与 `iterations/change/` 中最大规范 Sprint 编号加一
- **AND** 若 `<sprint-id>` 跳号，系统 MUST 阻断命令并报告下一个允许编号

#### Scenario: 已有两个 active Sprint 时禁止创建第三个

- **WHEN** `iterations/change/` 下已存在两个 `sprint-[0-9]{3}` active Sprint
- **AND** 用户指定一个不存在的下一个 Sprint
- **THEN** 系统 MUST 阻断命令
- **AND** 输出 MUST 引导用户指定现有 active Sprint

#### Scenario: 指定现有 active Sprint 时允许继续

- **WHEN** 用户运行 `/sprint-propose --sprint <sprint-id>`
- **AND** `<sprint-id>` 已存在于 `iterations/change/`
- **THEN** 系统 MUST 允许继续后续 Review Gate、Readiness Gate 和 Capacity Gate

### Requirement: Sprint 容量硬阻断后引导拆分或下一个连续 Sprint

系统 SHALL 保留 `100%~120%` 容量风险通过区间，并仅在超过 120% 的硬阻断场景引导拆分范围或指定下一个连续 Sprint。

#### Scenario: 超过 120% 时提示指定下一个连续 Sprint

- **WHEN** `/sprint-propose` 评估当前 Sprint 追加范围
- **AND** `estimated_person_days > capacity_person_days * 1.2`
- **THEN** 系统 MUST 阻断正式规划和 trace 更新
- **AND** 输出 MUST 提示拆分 Sprint、移出低优先级项、替换范围或使用 `/sprint-propose --sprint <next-sprint>` 创建下一个连续 Sprint
- **AND** `<next-sprint>` MUST 符合最大规范编号加一

#### Scenario: 100% 到 120% 保持风险通过

- **WHEN** `/sprint-propose` 评估候选范围且 `capacity_person_days < estimated_person_days <= capacity_person_days * 1.2`
- **THEN** 系统 MUST 允许继续生成或更新 Sprint
- **AND** 系统 MUST 记录容量风险、fix 缓冲影响和延后项建议

### Requirement: 归档 Sprint 冻结关联研发事实

系统 SHALL 在 Sprint 归档后冻结对应 REQ、BUG、Change 和 Sprint 四件套，防止普通研发命令继续改写已闭环事实。

#### Scenario: 普通研发命令不得修改归档 Sprint 范围

- **WHEN** Sprint 已位于 `iterations/archive/<sprint-id>/`
- **AND** 用户尝试通过 `req-*`、`bug-*`、`opsx-*`、`sprint-propose`、`sprint-apply` 或普通开发命令修改该 Sprint 关联的 REQ、BUG、Change 或四件套
- **THEN** 系统 MUST 阻断修改
- **AND** 输出 MUST 引导将偏差作为新生命周期输入处理

#### Scenario: 允许命令只能消费归档事实

- **WHEN** Sprint 已归档
- **AND** 用户运行 `explore`、`*-explore`、`sprint-exps`、`release-*`、`image-*` 或 `upgrade-*`
- **THEN** 系统 MAY 读取和引用该 Sprint 事实
- **AND** 系统 MUST NOT 反向修改已归档 REQ、BUG、Change 或 Sprint 四件套的交付语义

#### Scenario: 归档治理修复必须受控

- **WHEN** 已归档对象存在敏感信息、归档路径残留、状态漂移或公开发布所需的非内容性治理修复
- **THEN** 系统 MAY 通过明确授权的治理命令处理
- **AND** 治理命令 MUST 先 dry-run 或给出聚焦报告
- **AND** 系统 MUST 记录修复原因、范围和验证结果
