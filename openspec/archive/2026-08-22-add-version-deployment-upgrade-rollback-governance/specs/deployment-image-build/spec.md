## ADDED Requirements

### Requirement: 镜像 manifest 必须作为升级计划证据
镜像构建能力 SHALL 将目标版本 image manifest 作为升级路径计划和回滚计划的镜像证据来源。

#### Scenario: 升级计划引用目标镜像 manifest
- **WHEN** 系统生成目标版本升级计划
- **THEN** 计划 SHALL 校验并引用 `releases/<version>/image-manifest.json`
- **AND** 计划 SHALL 记录 backend image、web image、image tag、tarball、sha256 或等价脱敏摘要
- **AND** 计划 SHALL 在 manifest 缺失、版本不一致、tag 不一致或 input hash 漂移时输出 blocker。

#### Scenario: 同一目标版本复用同一组镜像
- **WHEN** 系统为首次部署、相邻升级或跨版本升级生成计划
- **THEN** 系统 SHALL 使用同一目标版本 backend / web 镜像证据
- **AND** 系统 SHALL NOT 要求为不同部署场景构建不同业务镜像，除非后续 Change 明确改变镜像策略。
