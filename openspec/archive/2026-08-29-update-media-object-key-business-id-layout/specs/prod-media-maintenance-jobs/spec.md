## MODIFIED Requirements

### Requirement: 生产媒体维护作业必须安全执行

生产媒体维护作业 MUST 支持 dry-run/apply 两阶段、分批执行、幂等处理、失败原因统计和二次审计。任何写数据库或对象存储的任务 MUST 默认先 dry-run，apply MUST 由显式参数触发，并 MUST 在执行前要求 MySQL 快照和对象存储 bucket / prefix 快照。历史图片多规格生成任务 MUST 支持批量生成或重生成 `thumbnail` 与 `display`，并 MUST 保留 `original` 归属关系。

生产媒体维护作业 MUST 支持按媒体类型、业务对象类型、业务对象 id、数量限制或前缀范围迁移历史媒体 key 到业务对象 id 目录。迁移任务 MUST 至少覆盖用户头像、品牌 Logo、Banner 图片、SKU 图片、SKU 视频、品牌证书图片和品牌证书 PDF/文档。dry-run 和 apply 输出 MUST 区分对象存储不可达、源对象缺失、目标 key 已存在、业务 id 缺失、DB 更新失败、缩略图缺失、展示图缺失和不支持媒体类型。系统设置保存 MUST NOT 自动触发该维护作业；历史迁移 MUST 由运维通过受控命令、生产 Compose 维护入口或后续明确的后台维护入口显式执行。

#### Scenario: 业务对象 id 目录迁移 dry-run

- **WHEN** 运维执行媒体业务对象 id 目录迁移 dry-run
- **THEN** 作业 MUST 输出待迁移记录数量、对象数量、派生图数量、跳过数量、失败分类、目标冲突和风险提示
- **AND** dry-run MUST NOT 写数据库或对象存储
- **AND** 输出 MUST NOT 包含真实 bucket 名、access key、secret key、连接串、raw object key、本机绝对路径、Authorization header、Cookie、`.env` 原文、生产私有 URL 或完整 SDK 堆栈。

#### Scenario: 业务对象 id 目录迁移 apply

- **GIVEN** MySQL 快照和对象存储 bucket/prefix 快照已确认
- **WHEN** 运维显式执行媒体业务对象 id 目录迁移 apply
- **THEN** 作业 MUST 分批复制对象并更新数据库媒体引用
- **AND** 原图、缩略图、展示图、视频和文件对象 MUST 按媒体类型保持可追溯归属
- **AND** 重复执行 MUST 幂等跳过已迁移或不适用记录
- **AND** 旧对象删除 MUST 作为单独高风险动作确认。
