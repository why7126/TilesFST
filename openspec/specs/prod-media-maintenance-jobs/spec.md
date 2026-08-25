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

生产媒体维护作业 MUST 支持 dry-run/apply 两阶段、分批执行、幂等处理、失败原因统计和二次审计。任何写数据库或对象存储的任务 MUST 默认先 dry-run，apply MUST 由显式参数触发，并 MUST 在执行前要求 MySQL 快照和对象存储 bucket / prefix 快照。历史图片多规格生成任务 MUST 支持批量生成或重生成 `thumbnail` 与 `display`，并 MUST 保留 `original` 归属关系。针对 JPEG、PNG、WebP 历史原图，重生成的 `thumbnail` 与 `display` MUST 使用 WebP 派生格式；SVG、PDF、GIF、HEIC、TIFF、BMP 或不支持对象 MUST 分类为跳过、拒绝或 fallback。系统设置保存 MUST NOT 自动触发该维护作业；历史重生成 MUST 由运维通过受控命令、生产 Compose 维护入口或后续明确的后台维护入口显式执行。

#### Scenario: 存量 WebP 多规格生成 dry-run

- **WHEN** 运维执行存量图片 WebP 多规格生成 dry-run
- **THEN** 作业 MUST 输出受影响记录数量、对象数量、已存在 WebP 派生数量、缺失规格、跳过原因、预计写入对象、失败分类和风险提示
- **AND** dry-run MUST NOT 写数据库
- **AND** dry-run MUST NOT 写对象存储
- **AND** dry-run MUST NOT 删除对象
- **AND** 输出 MUST NOT 包含真实 bucket 名、access key、secret key、连接串、raw object key、本机绝对路径、Authorization header、Cookie、`.env` 原文、生产私有 URL 或完整 SDK 堆栈。

#### Scenario: 存量 WebP 多规格生成 apply

- **GIVEN** dry-run 已通过且备份前置条件已完成
- **WHEN** 运维显式执行存量图片 WebP 多规格生成 apply
- **THEN** 作业 MUST 为支持格式生成缺失或不合格的 WebP `thumbnail` 与 WebP `display`
- **AND** 作业 MUST 记录任务类型、执行时间、参数摘要和 dry-run 摘要
- **AND** 输出 MUST 包含成功、失败、跳过、重试候选和失败原因统计
- **AND** 重复执行 MUST 保持幂等
- **AND** 作业 MUST NOT 改写原图对象格式或原图访问语义。

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

