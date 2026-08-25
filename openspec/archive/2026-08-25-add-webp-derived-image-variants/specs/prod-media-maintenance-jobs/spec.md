## MODIFIED Requirements

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
