## ADDED Requirements

### Requirement: 单一项目发布语义

产品版本发布管理 SHALL 使用单一项目发布语义，不再将 development 或 production 作为本项目发布目标维度。

#### Scenario: 旧 target 入参不改变发布门禁
- **WHEN** release、status、publish 或 upgrade 命令收到历史兼容的 `--target development` 或 `--target production`
- **THEN** validator SHALL treat it as compatibility input only
- **AND** the release scope SHALL remain `project`
- **AND** target input SHALL NOT change required gates, blocker classification, default next command, publish readiness, or upgrade plan filename.

#### Scenario: 发布对象不要求目标环境字段
- **WHEN** creating or validating a new `releases/<version>/release.json`
- **THEN** `release_target` and `production_deployment` SHALL NOT be required
- **AND** their absence SHALL NOT block release prepare, status, or publish validation.

#### Scenario: 默认升级计划使用无后缀文件名
- **WHEN** generating or validating default upgrade plans for a release
- **THEN** plan files SHALL be named `<from-version>-to-<to-version>.json`
- **AND** plan filenames SHALL NOT include `.development` or `.production` suffixes.

## MODIFIED Requirements

### Requirement: 发布状态决策面板

发布状态面板 SHALL 以只读方式汇总 release、image、upgrade 和 publish 当前阶段，并在单一项目发布语义下区分用户决策、证据缺口、普通 follow-up 和唯一下一步。

#### Scenario: 状态面板区分决策与证据
- **WHEN** 操作者查看某个版本的发布状态
- **THEN** 状态面板 SHALL 分别列出需要用户选择的决策项、需要命令或人工补齐的证据项，以及不阻断当前项目发布的后续事项
- **AND** 每个阻塞项 SHALL 标明分类、影响阶段、当前证据、建议动作和复核命令。

#### Scenario: 状态面板输出唯一下一步
- **WHEN** 状态面板能够推导出下一条安全动作
- **THEN** 输出 SHALL 提供一条可复制的下一步命令
- **AND** 若仍存在需要用户选择、补证或人工确认的事项，输出 SHALL 将其放入待用户处理区域而不是混入下一步命令。

### Requirement: 发布阻塞分类契约

产品版本发布管理 SHALL 使用统一阻塞分类表达 release、image、upgrade 和 publish 中的决策、证据、环境、范围和安全问题，不再使用生产目标专属分类作为当前发布门禁。

#### Scenario: 阻塞分类字段完整
- **WHEN** 发布命令、状态面板或 validator 报告发布阻塞项
- **THEN** 阻塞项 SHALL use `decision_missing`, `prepare_evidence_missing`, `publish_evidence_missing`, `input_drift`, `environment_unavailable`, `scope_incomplete`, `public_safety`, or `schema_invalid`
- **AND** 阻塞项 SHOULD include phase, owner, current_evidence, safe_remediation, and rerun_check.

#### Scenario: 发布确认阶段不再重新发现普通下一步
- **WHEN** 发布状态面板已报告某版本未达到 publish ready
- **THEN** `/release-publish` SHOULD 只确认已就绪发布或报告状态面板已暴露的阻塞项
- **AND** 普通缺失的 image manifest、默认 upgrade plan 或用户决策 SHOULD 在 `/release-status` 或 `/release-prepare` 阶段提前暴露。

## REMOVED Requirements

### Requirement: 发布目标环境分离

Reason: 本项目不区分 development / production 发布目标；历史 target 字段仅保留兼容读取，不再作为发布治理维度。

### Requirement: 生产证据后置承接

Reason: 本项目没有独立生产发布路径，`production_only_pending` 不再作为当前发布状态或发布确认的专属分类。

### Requirement: 生产发布环境证据强门禁

Reason: 本项目不维护生产目标专属门禁；发布确认只按单一项目发布语义校验当前 release、image、upgrade、公告、版本号和公开安全证据。
