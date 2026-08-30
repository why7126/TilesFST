# prod-media-maintenance-jobs Specification

## Purpose
TBD - created by archiving change add-prod-media-maintenance-jobs. Update Purpose after archive.
## Requirements
### Requirement: 系统必须提供生产媒体维护作业入口

系统 MUST 提供生产 Docker Compose 环境下的媒体历史维护作业入口，用于对象 Key 迁移、缩略图回填、SKU pending 主图正式化和二次审计等任务。维护作业 MUST 在生产服务器或受控堡垒环境内执行，MUST 复用生产 env / secret 注入和 Compose 网络，MUST NOT 要求将生产 `.env`、数据库连接串或对象存储密钥下载到开发机。

#### Scenario: 通过生产 Compose 一次性容器执行

- **GIVEN** 运维已准备生产 env、外部 MySQL 和对象存储前置条件
- **WHEN** 运维执行生产媒体维护作业
- **THEN** 作业 MUST 通过 `docker compose ... run --rm` 或等价一次性容器执行
- **AND** 作业 MUST 使用 `deploy/prod/compose.tencent-cos.yml` 或经文档明确的兼容生产 Compose
- **AND** 作业 MUST NOT 改变在线 backend/web 服务启动命令、端口和健康检查语义
- **AND** 命令示例 MUST NOT 包含真实 `.env` 内容、数据库连接串、对象存储密钥或生产私有 URL。

#### Scenario: 维护镜像策略明确

- **WHEN** 团队实现生产媒体维护作业入口
- **THEN** 系统 SHOULD 提供 `tilesfst-maintenance` service 或等价专用维护入口
- **AND** 若复用 `tilesfst-backend` 镜像执行维护命令，设计与验收 MUST 证明该入口不影响在线服务语义
- **AND** 临时只读挂载 `scripts/` 的方式 MUST 仅作为应急审计或 dry-run 方案
- **AND** 临时挂载方案 MUST NOT 默认允许 apply。

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

### Requirement: 生产媒体维护作业必须支持备份回滚和二次审计

生产媒体维护作业 MUST 在 apply 前要求 MySQL 快照与对象存储 bucket / prefix 快照。回滚说明 MUST 以恢复快照为主；未验证反向脚本不得被描述为默认可靠回滚。作业执行后 MUST 支持二次审计并输出媒体四联或五联验收摘要。多规格图片生成二次审计 MUST 覆盖 `thumbnail`、`display`、`original` 的 key、object、URL、render 和规格收益；WebP 派生补生成二次审计 MUST 额外覆盖 WebP key、`image/webp` MIME、原图格式保留和体积收益。

#### Scenario: WebP 多规格生成后二次审计

- **WHEN** 存量图片 WebP 多规格生成 apply 完成
- **THEN** 系统 MUST 支持二次审计
- **AND** 审计摘要 MUST 覆盖 `thumbnail`、`display`、`original` 的 key、object、URL、render 和体积/像素收益
- **AND** 审计摘要 MUST 标明 `thumbnail` 与 `display` 是否为 WebP、MIME 是否为 `image/webp`、原图格式是否保留
- **AND** 任一 fail 项 MUST 包含足以支撑后续 `/bug-capture` 的失败现象、影响范围、期望结果和实际结果
- **AND** 审计输出 MUST 脱敏。

### Requirement: 媒体维护 dry-run 必须快速摘要对象存储不可达

生产媒体维护作业在 dry-run 期间 MUST 区分对象真实不存在和对象存储不可达。当对象存储因 endpoint、region、bucket、权限、凭据、网络或服务状态导致不可达时，dry-run MUST 快速返回阻断摘要，MUST 将顶层状态或对象验收维度标记为 `blocked`，并 MUST NOT 输出可进入 apply 的结论。

#### Scenario: 对象存储不可达时返回 blocked 摘要

- **WHEN** 运维执行生产媒体维护 dry-run 且对象存储 endpoint、bucket、region、权限或网络不可用
- **THEN** 作业 MUST 返回 `object_storage_unreachable` 或等价失败分类
- **AND** 作业 MUST 将顶层 summary 或 acceptance summary 的对象维度标记为 `blocked`
- **AND** 作业 MUST 列出受影响对象相关子任务或等价 `affected_tasks`
- **AND** 作业 MUST 建议先检查 endpoint、region、bucket、权限、网络与 env 注入后重新 dry-run
- **AND** 作业 MUST NOT 输出可进入备份确认或 apply 的结论。

#### Scenario: 对象不存在仍归入 missing 统计

- **WHEN** dry-run 访问单个媒体对象并收到 `MEDIA_NOT_FOUND`、`NoSuchKey`、`NoSuchObject` 或等价对象不存在结果
- **THEN** 作业 MUST 将该对象归入 missing 类统计
- **AND** 作业 MUST NOT 将单个对象不存在误报为 `object_storage_unreachable`
- **AND** 作业 MUST 在对象存储整体可达时继续生成正常 dry-run 摘要。

#### Scenario: 阻断摘要必须脱敏

- **WHEN** dry-run 输出对象存储不可达摘要、日志或验收证据
- **THEN** 输出 MAY 包含 provider、bucket hash、auto create bucket 策略、失败分类和建议动作
- **AND** 输出 MUST NOT 包含真实 bucket 名、access key、secret key、连接串、raw object key、本机绝对路径、Authorization header、Cookie、`.env` 原文、生产私有 URL 或完整 SDK 堆栈。

#### Scenario: 聚合维护任务传播对象维度 blocked

- **WHEN** 聚合媒体维护任务中的任一对象相关子任务发现对象存储不可达
- **THEN** 聚合任务 MUST 在顶层 summary 传播 `blocked` 状态
- **AND** 聚合任务 MUST 标明受影响子任务和未完成对象检查范围
- **AND** 聚合任务 MUST 将后续对象相关子任务标记为 skipped、blocked 或等价不可执行状态
- **AND** 聚合任务 MUST 提示修复对象存储环境后重新 dry-run。

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

### Requirement: 生产媒体维护作业必须覆盖 Banner 自定义上传图

生产媒体维护作业 MUST 将 Banner 自定义上传图纳入历史图片派生图维护范围。对于 `banners.image_object_key` 指向 `images/default/banners/` 或等价 Banner 自定义上传目录的 JPEG、PNG、WebP 原图，系统 MUST 能通过 dry-run 报告缺失或不合格的 `thumbnail` 与 `display` 派生图，并能在 apply 中生成同目录 WebP `.thumb.webp` 与 `.display.webp`。当 Banner 原图已迁入 `images/default/banners/{banner_id}/` 目录时，作业 MUST 同步维护历史无 id URL 的同名 WebP alias，避免旧 `/media/images/default/banners/<filename>.thumb.webp` 或 `.display.webp` fallback 到原图。维护作业 MUST 保留原图格式和访问语义，MUST NOT 删除原图或已有合格派生图。

#### Scenario: Banner 派生图 dry-run

- **WHEN** 运维执行 `backfill-image-variants` dry-run
- **AND** 数据库存在 `banners.image_object_key` 指向 `images/default/banners/` 的历史自定义上传图片
- **AND** 对应 `.thumb.webp` 或 `.display.webp` 对象缺失或不合格
- **THEN** 作业 MUST 在候选或摘要中包含 Banner 来源，来源类型 SHOULD 为 `banner_image`
- **AND** 作业 MUST 报告缺失规格、预计写入对象数量、跳过原因和失败分类
- **AND** 对已迁入 `images/default/banners/{banner_id}/` 的 Banner，作业 MUST 报告旧无 id 路径 alias 是否缺失或不合格
- **AND** dry-run MUST NOT 写数据库
- **AND** dry-run MUST NOT 写对象存储
- **AND** dry-run MUST NOT 删除对象
- **AND** 输出 MUST 保持脱敏。

#### Scenario: Banner 派生图 apply

- **GIVEN** Banner 派生图 dry-run 已通过
- **AND** MySQL 快照与对象存储 bucket / prefix 快照已完成
- **WHEN** 运维显式执行 `backfill-image-variants --apply --confirm-backup`
- **THEN** 作业 MUST 为支持格式的 Banner 原图生成同目录 WebP `.thumb.webp` 与 `.display.webp`
- **AND** 对已迁入 `images/default/banners/{banner_id}/` 的 Banner，作业 MUST 为旧无 id 路径生成或覆盖同名 WebP alias
- **AND** 作业 MUST NOT 改写 `banners.image_object_key`
- **AND** 作业 MUST NOT 改写原图对象格式或原图访问语义
- **AND** 输出 MUST 包含成功、失败、跳过、重试候选和失败原因统计
- **AND** 重复执行 MUST 保持幂等。

#### Scenario: 聚合维护任务包含 Banner 缩略图候选

- **WHEN** 运维执行 `media-drift-reconcile` dry-run 或 apply
- **THEN** 聚合任务 MUST 通过缩略图回填或等价子任务覆盖 Banner `.thumb.webp` 缺失候选
- **AND** 顶层摘要或子任务摘要 MUST 不把 Banner 缺失缩略图遗漏为 0
- **AND** 仍 MUST 保持对象存储不可达 blocked 传播、失败分类、脱敏输出和 `--apply --confirm-backup` 写入门禁。

#### Scenario: Banner 派生图 URL 二次审计

- **WHEN** Banner 派生图 apply 完成
- **THEN** 运维 MUST 能用 `/media/...thumb.webp` 与 `/media/...display.webp` 验证派生图 URL
- **AND** 历史无 id Banner 派生图 URL 若仍被访问，也 MUST 直接命中 WebP alias
- **AND** 成功响应 MUST 返回 `Content-Type: image/webp`
- **AND** 成功响应 MUST NOT 出现 `x-media-fallback: 1`
- **AND** 验收记录 SHOULD 包含 Content-Length 对比、对象 MIME、幂等 dry-run 摘要和端侧 render evidence。

