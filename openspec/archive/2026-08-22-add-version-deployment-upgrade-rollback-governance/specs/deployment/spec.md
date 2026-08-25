## ADDED Requirements

### Requirement: 部署说明必须覆盖首次部署、升级和回滚
部署能力 SHALL 文档化首次部署、相邻版本升级、跨版本升级和回滚的执行边界。

#### Scenario: 部署文档说明三类部署路径
- **WHEN** 运维阅读部署文档
- **THEN** 文档 SHALL 区分首次部署、相邻版本升级和跨版本升级
- **AND** 文档 SHALL 说明同一目标版本复用同一组 backend / web 镜像，不按部署场景拆分业务镜像。

#### Scenario: 回滚说明包含证据前置
- **WHEN** 运维阅读升级回滚说明
- **THEN** 文档 SHALL 要求旧镜像、旧 env 摘要、DB 备份、对象存储影响确认和回滚后 smoke
- **AND** 文档 SHALL 说明 DB 回滚不能凭空自动完成，必须依赖备份恢复或明确反向迁移策略。

### Requirement: 部署升级输出不得泄露真实环境配置
部署升级计划、部署校验和回滚记录 SHALL 遵守真实 env 与生产敏感信息安全边界。

#### Scenario: 输出脱敏部署摘要
- **WHEN** 系统生成部署升级计划、env diff 或回滚记录
- **THEN** 输出 SHALL NOT 包含真实 `.env` 内容、数据库连接串、对象存储凭据、Authorization header、Cookie、生产私有域名或真实客户数据
- **AND** 输出 SHALL 使用变量名、hash、摘要、负责人确认或占位符表达证据。
