## ADDED Requirements

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
