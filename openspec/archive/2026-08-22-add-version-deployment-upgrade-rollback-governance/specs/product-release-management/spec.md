## ADDED Requirements

### Requirement: 产品发布必须关联升级路径支持级别
产品版本发布管理能力 SHALL 在发布准备或发布确认阶段引用目标版本的部署升级支持级别和回滚证据。

#### Scenario: 发布准备默认输出首次部署和相邻升级状态
- **WHEN** release preparation evaluates a target version
- **THEN** the release object SHALL record or reference fresh install and adjacent upgrade support levels
- **AND** missing upgrade plan evidence SHALL be reported as blocker, warning, manual review, or not applicable with rationale.

#### Scenario: 跨版本升级按需生成
- **WHEN** no user explicitly requested a cross-version upgrade path for the target version
- **THEN** release preparation SHALL NOT require or generate cross-version upgrade plans by default
- **AND** users MAY generate one manually with `/upgrade-plan --from <old-version> --to <target-version>`.

#### Scenario: 发布确认不夸大跨版本支持
- **WHEN** a release lacks complete cross-version rehearsal and rollback evidence
- **THEN** release publish SHALL NOT describe cross-version upgrade as supported
- **AND** public release material SHALL use manual review or unsupported wording.
