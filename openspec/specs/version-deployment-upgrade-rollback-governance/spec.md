# version-deployment-upgrade-rollback-governance Specification

## Purpose
版本部署升级与回滚治理能力用于以结构化升级路径对象管理 `from_version -> to_version` 的首次部署、相邻升级、跨版本升级、验证证据、支持级别和回滚边界，避免将发布存在、迁移代码存在或镜像存在误判为升级路径已验证。
## Requirements
### Requirement: 升级路径对象
系统 SHALL 使用结构化升级路径对象表达 `from_version -> to_version` 的首次部署、相邻升级、跨版本升级和回滚治理事实。

#### Scenario: 升级路径对象字段完整
- **WHEN** 系统生成升级路径对象
- **THEN** 对象 SHALL 包含 `from_version`、`to_version`、`support_level`、`source_confidence`、`impact_summary`、`required_checks`、`steps`、`rollback`、`blockers`、`warnings` 和 `evidence`
- **AND** `from_version` SHALL 支持 `fresh` 或具体版本号。

#### Scenario: 升级路径对象脱敏
- **WHEN** 系统写入或展示升级路径对象
- **THEN** 对象 SHALL NOT 包含真实 `.env` 内容、密钥、数据库连接串、Authorization header、Cookie、本机绝对路径或真实客户数据。

#### Scenario: 正式 release 目录只保留真实确认路径
- **WHEN** 系统向 `releases/<to-version>/upgrade-plans/` 写入升级路径对象
- **THEN** 该路径 SHALL 是项目团队确认需要支持或评估的真实部署升级路径
- **AND** 仅用于解释能力、单测覆盖或演示支持级别的示例版本 SHALL NOT 写入正式 release 事实源。

#### Scenario: 正常发布默认升级路径范围
- **WHEN** 系统准备一个目标版本的正常发布
- **THEN** 系统 SHALL 默认要求 `fresh -> <to-version>` 首次部署计划
- **AND** 若存在上一正式发布版本，系统 SHALL 默认要求 `<previous-release-version> -> <to-version>` 相邻升级计划
- **AND** 系统 SHALL NOT 默认生成任意旧版本到目标版本的跨版本升级计划。

### Requirement: 升级支持级别
系统 SHALL 为每条部署或升级路径输出证据驱动的支持级别。

#### Scenario: 输出支持级别
- **WHEN** 系统评估部署或升级路径
- **THEN** 支持级别 SHALL 为 `fresh-install-supported`、`adjacent-upgrade-supported`、`cross-version-upgrade-supported`、`cross-version-upgrade-requires-manual-review` 或 `unsupported` 之一
- **AND** 输出 SHALL 说明支持级别的证据、blocker、warning 或人工复核原因。

#### Scenario: 跨版本证据不足时降级
- **WHEN** 跨版本升级缺少中间版本 release 事实源、跨版本演练、DB drift/smoke、env diff、对象存储审计或回滚证据
- **THEN** 系统 SHALL NOT 将该路径标记为 `cross-version-upgrade-supported`
- **AND** 系统 SHALL 将其标记为 `cross-version-upgrade-requires-manual-review` 或 `unsupported`。

### Requirement: 版本事实源一致性
系统 SHALL 在部署升级计划中校验产品版本、发布版本、镜像版本、源码版本和部署运行版本的一致性。

#### Scenario: 版本事实源校验
- **WHEN** 系统生成或验证升级计划
- **THEN** 系统 SHALL 校验 `releases/<version>/release.json.version`、`src/shared/product-version.ts`、`image-manifest.json.image_tag`、Git tag 或 commit、部署 env `TILESFST_IMAGE_TAG` 或等价目标版本
- **AND** 缺失、漂移或不一致 SHALL 输出 blocker 或 warning。

#### Scenario: Git tag 不替代发布事实源
- **WHEN** Git tag 存在但目标版本缺少 release 事实源
- **THEN** 系统 SHALL NOT 仅凭 Git tag 宣称版本已发布或升级路径已验证
- **AND** 系统 SHALL 要求补齐 release 事实或标记来源可信度为 `reconstructed`、`partial` 或等价非 verified 状态。

### Requirement: 首次部署计划
系统 SHALL 为目标版本生成首次部署计划，用于空环境部署验证。

#### Scenario: 首次部署计划覆盖基础门禁
- **WHEN** 系统生成 `fresh -> <to_version>` 部署计划
- **THEN** 计划 SHALL 覆盖目标 release、image manifest、生产 env 必填检查、`APP_ENV=production` MySQL 要求、对象存储配置、Docker Compose config、空库初始化、首次管理员初始化和部署后 smoke
- **AND** 计划通过后系统 MAY 将路径标记为 `fresh-install-supported`。

### Requirement: 相邻升级与回滚计划
系统 SHALL 为上一发布版本到目标版本生成相邻升级计划和回滚计划。

#### Scenario: 相邻升级计划覆盖升级门禁
- **WHEN** 系统生成 `<previous_version> -> <to_version>` 升级计划
- **THEN** 计划 SHALL 覆盖来源和目标 release 事实源、目标 image manifest、env diff、DB 影响判断、备份确认、`TILESFST_IMAGE_TAG` 更新、服务重启策略和升级后 smoke。

#### Scenario: 相邻升级回滚计划覆盖恢复证据
- **WHEN** 系统生成相邻升级回滚计划
- **THEN** 计划 SHALL 覆盖旧镜像 tag 或旧离线包、旧 env 摘要、DB 备份恢复条件、对象存储写入影响和回滚后 smoke。

### Requirement: 跨版本升级与回滚计划
系统 SHALL 为指定旧版本到目标版本生成跨版本升级计划和回滚计划。

#### Scenario: 跨版本计划由用户按需触发
- **WHEN** 用户明确执行 `/upgrade-plan --from <old-version> --to <target-version>` 且 `<old-version>` 不是上一正式发布版本
- **THEN** 系统 SHALL 生成跨版本升级计划
- **AND** 缺少演练、DB/env/object storage 或回滚证据时，系统 SHALL 将支持级别降级为 `cross-version-upgrade-requires-manual-review` 或 `unsupported`。

#### Scenario: 跨版本计划聚合中间版本影响
- **WHEN** 系统生成 `<old_version> -> <to_version>` 跨版本升级计划
- **THEN** 计划 SHALL 聚合中间版本的 release 事实源、DB schema/migration、env 示例变化、Dockerfile、Compose、镜像构建输入、API/Orval、对象存储和生产维护任务影响
- **AND** 计划 SHALL 明确必须 dry-run 的维护任务、人工确认或演练步骤，以及是否需要先升级到中间版本。

#### Scenario: 跨版本回滚计划明确不可逆边界
- **WHEN** 系统生成跨版本回滚计划
- **THEN** 计划 SHALL 明确全量备份要求、旧镜像和旧 env 恢复方式、DB 回滚只能基于备份或明确反向迁移策略、对象存储写入型维护任务不可逆风险和回滚后 smoke。

### Requirement: 环境变量差异分析
系统 SHALL 提供 env diff 能力，比较来源版本与目标版本的可提交 env 示例。

#### Scenario: env diff 覆盖示例文件
- **WHEN** 系统执行 env diff
- **THEN** 系统 SHALL 覆盖 `.env.example`、`src/backend/.env.example`、`src/backend/.env.docker`、`deploy/**/*.env.example` 和 `scripts/build-images.env.example`
- **AND** 输出 SHALL 包含 `added`、`removed`、`changed_default`、`required_in_production`、`unsafe_example_value` 和 `manual_review` 分类。

#### Scenario: env diff 不输出真实值
- **WHEN** 系统输出 env diff
- **THEN** 输出 SHALL 只包含变量名、分类、说明和修复建议
- **AND** 输出 SHALL NOT 包含真实生产 env 值。

### Requirement: 数据库升级验证证据
系统 SHALL 在升级计划中记录数据库升级验证证据，并区分 SQLite 与 MySQL。

#### Scenario: 数据库影响要求 MySQL 证据
- **WHEN** 升级计划的数据库影响不是 `none`、`na` 或等价不涉及状态
- **THEN** 计划 SHALL 要求 MySQL schema drift 或目标 MySQL smoke、DB 备份和回滚证据
- **AND** 系统 SHALL NOT 仅凭本地 SQLite 测试通过宣称生产 DB 升级安全。

### Requirement: 回滚证据模型
系统 SHALL 为升级路径定义结构化回滚证据模型。

#### Scenario: 回滚证据字段完整
- **WHEN** 系统记录升级回滚证据
- **THEN** 证据 SHALL 覆盖 `previous_image`、`target_image`、`env_snapshot`、`database_backup`、`object_storage_backup` 或只读确认、`rollback_steps` 和 `post_rollback_smoke`
- **AND** 缺少必要证据 SHALL 使升级计划标记为 blocked 或 requires manual review。

### Requirement: upgrade 命令边界
系统 SHALL 提供 upgrade 计划与校验入口，用于生成和验证升级路径对象。

#### Scenario: 命令只生成计划和校验结果
- **WHEN** 用户执行 `/upgrade-plan`、`/upgrade-validate` 或等价命令
- **THEN** 命令 SHALL 读取 release、image manifest、env 示例、DB schema/migration、Compose 和维护任务文档
- **AND** 命令 SHALL 输出支持级别、影响摘要、blocker、warning、升级步骤、回滚步骤和证据缺口
- **AND** 命令 SHALL NOT 自动执行生产升级、自动修改真实 env、自动执行写入型 DB 或对象存储维护任务。

### Requirement: 升级计划目标环境分离
版本部署升级与回滚治理 SHALL 支持开发环境和生产环境两类升级计划目标，并避免把生产实施门禁误用为开发部署门禁。

#### Scenario: 开发环境升级计划
- **WHEN** 系统生成 `deployment_target=development` 的升级计划
- **THEN** 计划 SHALL 表达开发部署、开发验证和开发回滚边界
- **AND** 生产真实 env、生产 MySQL 或对象存储备份、生产 smoke 和生产公开证据 SHALL NOT 作为开发计划 blocker
- **AND** 生产实施要求 MAY 作为后续生产发布提醒记录。

#### Scenario: 生产环境升级计划
- **WHEN** 系统生成 `deployment_target=production` 的升级计划
- **THEN** 计划 SHALL 保留生产 env、备份、MySQL、对象存储、smoke 和回滚证据要求
- **AND** 不得凭开发环境部署计划宣称生产升级路径已验证。

#### Scenario: 常规发布默认升级计划跟随发布目标
- **WHEN** 正常发布需要生成默认升级计划
- **THEN** `fresh -> <to-version>` 和 `<previous-release-version> -> <to-version>` 的默认计划 SHALL 使用发布对象声明的目标环境
- **AND** 若后续单独生产发布，生产发布 SHALL 生成或校验生产目标升级计划。

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

