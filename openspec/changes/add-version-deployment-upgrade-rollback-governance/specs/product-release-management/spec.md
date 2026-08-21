## ADDED Requirements

### Requirement: 产品发布必须关联升级路径支持级别
产品版本发布管理能力 SHALL 在发布准备或发布确认阶段引用目标版本的部署升级支持级别和回滚证据。

#### Scenario: 发布准备输出升级路径状态
- **WHEN** release preparation evaluates a target version
- **THEN** the release object SHALL record or reference fresh install, adjacent upgrade, and known cross-version upgrade support levels
- **AND** missing upgrade plan evidence SHALL be reported as blocker, warning, manual review, or not applicable with rationale.

#### Scenario: 发布确认不夸大跨版本支持
- **WHEN** a release lacks complete cross-version rehearsal and rollback evidence
- **THEN** release publish SHALL NOT describe cross-version upgrade as supported
- **AND** public release material SHALL use manual review or unsupported wording.
