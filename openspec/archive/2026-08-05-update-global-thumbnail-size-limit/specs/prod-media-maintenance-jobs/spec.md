## MODIFIED Requirements

### Requirement: 生产媒体维护作业必须安全执行

生产媒体维护作业 MUST 支持 dry-run/apply 两阶段、分批执行、幂等处理、失败原因统计和二次审计。任何写数据库或对象存储的任务 MUST 默认先 dry-run，apply MUST 由显式参数触发，并 MUST 在执行前要求 MySQL 快照和对象存储 bucket / prefix 快照。历史缩略图重生成任务 MUST 读取当前 effective `media.thumbnail_max_size_kb`，并 MUST 覆盖 SKU、品牌 Logo 和品牌证书图片三类对象；当该值为 `0` 时按当前不限制模式重生成，当该值为正整数时按全局体积目标尽量生成更轻量 `.thumb` 缩略图。系统设置保存 MUST NOT 自动触发该维护作业；历史重生成 MUST 由运维通过受控命令、生产 Compose 维护入口或后续明确的后台维护入口显式执行。

#### Scenario: dry-run 不写入

- **WHEN** 运维执行任一生产媒体维护作业 dry-run
- **THEN** 作业 MUST 输出受影响记录数量、对象数量、跳过原因、缺失对象、目标 key 冲突和风险提示
- **AND** dry-run MUST NOT 写数据库
- **AND** dry-run MUST NOT 写对象存储
- **AND** dry-run MUST NOT 删除对象。

#### Scenario: apply 显式触发并可审计

- **GIVEN** dry-run 已通过且备份前置条件已完成
- **WHEN** 运维显式执行 apply
- **THEN** 作业 MUST 记录镜像 tag、Compose 文件、命令参数、执行时间、任务类型和 dry-run 摘要
- **AND** 输出 MUST 包含成功、失败、跳过、重试候选和失败原因统计
- **AND** 重复执行 MUST 保持幂等，已完成项 MUST 被识别为 skipped、already_done 或等价状态。

#### Scenario: 输出脱敏

- **WHEN** 维护作业输出日志、JSON 摘要或验收证据
- **THEN** 输出 MUST NOT 包含真实密钥、数据库连接串、Authorization header、Cookie、生产 `.env` 原文、本机绝对路径或真实客户敏感数据
- **AND** 输出 SHOULD 使用变量名、脱敏对象标识、计数、错误码和失败原因摘要表达结果。

#### Scenario: 历史缩略图按当前全局策略重生成

- **GIVEN** `media.thumbnail_max_size_kb` effective 值为 `20`
- **AND** 历史 SKU、品牌 Logo 或品牌证书图片存在同目录 `.thumb` 缩略图缺失、疑似无收益或超过当前体积目标的情况
- **AND** 运维已完成 dry-run 和备份确认
- **WHEN** 运维显式执行历史缩略图重生成 apply
- **THEN** 作业 MUST 读取原图并按当前全局体积目标重生成同目录 `.thumb` 缩略图
- **AND** dry-run MUST 将缺失缩略图、疑似复制原图的缩略图、疑似同尺寸缩略图以及已存在但超过当前体积目标上限的缩略图计入重试候选
- **AND** 输出 MUST 统计成功、失败、跳过、已符合、超过目标上限、未达标和重试候选
- **AND** 重复执行 MUST 保持幂等，不破坏已符合当前策略的缩略图。

#### Scenario: 保存系统设置不触发历史重生成

- **WHEN** `admin` 在系统设置 media 分组保存 `thumbnail_max_size_kb`
- **THEN** 系统 MUST NOT 自动运行生产媒体维护作业
- **AND** 系统 MUST NOT 自动批量读取原图、覆盖历史 `.thumb` 对象或写入对象存储
- **AND** 历史缩略图如需应用新策略 MUST 通过 dry-run/apply 维护流程执行。
