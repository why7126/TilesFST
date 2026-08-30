## ADDED Requirements

### Requirement: 默认升级路径提示
版本部署升级与回滚治理 SHALL 为正常发布提供默认升级路径提示，帮助操作者一次性看到目标环境所需的首次部署和相邻升级计划。

#### Scenario: 状态面板提示缺失默认升级计划
- **WHEN** 某个发布目标缺少 `fresh -> <version>` 或上一正式版本到当前版本的目标环境升级计划
- **THEN** 状态面板 SHALL 输出对应 `/upgrade-plan --from ... --to ... --target ...` 命令
- **AND** 输出 SHALL 不要求操作者记忆默认路径规则。

### Requirement: 镜像稳定输入边界
版本部署升级与回滚治理 SHALL 将镜像稳定输入限定为会影响构建产物、运行时行为或部署包行为的文件和发布范围字段。

#### Scenario: 发布证据叙述不触发镜像漂移
- **WHEN** 仅发布证据、运维叙述或长期文档说明发生变化，且不影响 Dockerfile、Compose、Nginx、构建脚本、env 示例、schema、migration 或稳定发布范围字段
- **THEN** 镜像计划或 manifest 校验 SHALL NOT 因这些叙述文件变化而报告 image input drift
- **AND** 需要补充的发布证据 SHALL 由 release 或 deployment gate 单独表达。
