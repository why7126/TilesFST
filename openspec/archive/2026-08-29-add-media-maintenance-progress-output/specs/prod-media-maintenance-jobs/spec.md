## ADDED Requirements

### Requirement: 生产媒体维护作业必须支持可选进度输出

系统 MUST 为生产媒体维护 CLI 提供默认关闭的可选进度输出能力，并在开启后保持最终 JSON stdout 兼容。

#### Scenario: 默认执行保持 stdout JSON 兼容

- **WHEN** 运维执行媒体维护命令且未传入进度参数
- **THEN** 命令 MUST 只在 stdout 输出最终任务结果 JSON
- **AND** 现有依赖 stdout 解析 JSON 的生产脚本、`jq` 管道和审计归档 MUST 不受影响

#### Scenario: 开启进度输出

- **WHEN** 运维执行媒体维护命令并传入 `--progress` 或等价显式参数
- **THEN** 系统 MUST 在执行过程中输出进度信息
- **AND** 进度信息 MUST 包含任务名、阶段、总量、已完成数量、成功数量、失败数量、跳过数量和进度百分比或等价字段
- **AND** 最终任务结果 JSON MUST 继续输出到 stdout
- **AND** 进度信息 SHOULD 输出到 stderr，避免污染 stdout JSON

#### Scenario: 派生图回填进度

- **WHEN** 运维对 `backfill-image-variants` 或 `backfill-brand-certificate-thumbnails` 启用进度输出
- **THEN** 系统 MUST 展示 dry-run 扫描或 apply 处理过程中的 item 级进度
- **AND** `backfill-image-variants` MUST 明确单个源图可能产生 thumbnail 与 display 多个写入的计数口径

#### Scenario: 聚合任务阶段进度

- **WHEN** 运维对 `media-drift-reconcile` 启用进度输出
- **THEN** 系统 MUST 至少展示 SKU pending 主图正式化、证书图片 key 迁移、缩略图回填和对象 key 审计 4 个阶段的进度或阶段汇总
- **AND** 如果子任务支持 item 级进度，聚合任务 SHOULD 透传子任务进度

#### Scenario: 长耗时子任务输出 item 级心跳

- **WHEN** 聚合任务进入 `business_id_media_key_migration` 等长耗时子任务
- **THEN** 系统 MUST 在子任务内部继续输出 item 级进度
- **AND** 进度行 MUST 使用当前子任务的 `total`、`completed` 和 `progress_percent`
- **AND** 系统 SHOULD 在对象存储或数据库慢操作前输出 `checking_source`、`checking_target`、`copying_object`、`updating_db` 等枚举化状态
- **AND** 这些状态 MUST NOT 包含真实对象 key、文件名、数据库值或敏感异常详情

#### Scenario: 进度输出脱敏

- **WHEN** 系统输出媒体维护进度信息
- **THEN** 进度行 MUST NOT 包含真实 object key、原始文件名、客户信息、数据库连接串、对象存储 endpoint、access key、secret key、Authorization header、Cookie、真实 `.env` 内容或本机绝对路径
- **AND** 失败对象定位 SHOULD 继续通过最终 JSON 中既有的脱敏 hash、标准前缀和失败原因枚举表达
