## MODIFIED Requirements

### Requirement: 生产媒体维护作业必须安全执行

生产媒体维护作业 MUST 支持 dry-run/apply 两阶段、分批执行、幂等处理、失败原因统计和二次审计。任何写数据库或对象存储的任务 MUST 默认先 dry-run，apply MUST 由显式参数触发，并 MUST 在执行前要求 MySQL 快照和对象存储 bucket / prefix 快照。历史图片多规格生成任务 MUST 支持批量生成或重生成 `thumbnail` 与 `display`，并 MUST 保留 `original` 归属关系。重生成 `.display` 图时 MUST 读取系统设置 media 分组的 display 图体积目标 effective 配置，默认 MUST 为 `768` KB；重生成 `.thumbnail` 图时 MUST 继续读取缩略图体积目标配置。系统设置保存 MUST NOT 自动触发该维护作业；历史重生成 MUST 由运维通过受控命令、生产 Compose 维护入口或后续明确的后台维护入口显式执行。

#### Scenario: 维护作业默认 dry-run

- **WHEN** 运维执行生产媒体维护作业且未提供 apply 确认
- **THEN** 作业 MUST 只输出待处理数量、预计写入对象、跳过原因、失败分类和风险摘要
- **AND** dry-run MUST NOT 写数据库
- **AND** dry-run MUST NOT 写对象存储
- **AND** 输出 MUST NOT 包含真实 `.env`、数据库连接串、对象存储密钥、Authorization header、Cookie、本机绝对路径或真实客户数据。

#### Scenario: 多规格历史图片 apply 受控

- **GIVEN** dry-run 已完成且备份或风险确认已记录
- **WHEN** 运维显式执行多规格图片生成 apply
- **THEN** 作业 MUST 生成缺失或不合格的 `thumbnail` 与 `display`
- **AND** `.display` 重生成 MUST 读取 display 图体积目标 effective 配置
- **AND** 输出 MUST 包含成功、失败、跳过、重试候选和失败原因统计
- **AND** 重复执行 MUST 保持幂等
- **AND** apply 后 MUST 支持二次审计验证 key、object、URL、render 和规格收益。

#### Scenario: 保存系统设置不触发维护任务

- **WHEN** `admin` 保存 display 图体积目标上限配置
- **THEN** 系统 MUST NOT 自动启动生产媒体维护作业
- **AND** 系统 MUST NOT 自动扫描对象存储、读取历史原图或覆盖历史 `.display` 对象
- **AND** 历史 display 图如需应用新策略，MUST 由运维显式执行 dry-run / apply。
