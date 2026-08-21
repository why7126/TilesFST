## ADDED Requirements

### Requirement: 小程序媒体历史对象四联审计

系统 SHALL 支持小程序媒体历史对象四联审计 helper 或等价受控流程，用于 dry-run 检查历史媒体对象的 key、object、URL 和 render 风险。审计 SHALL 默认只读，不得默认写入数据库或对象存储。审计输出 SHALL 脱敏，使用 key hash、标准前缀、资源类型、计数和失败原因枚举，不得输出真实 object key 全量值、密钥、`.env`、Authorization header、Cookie、本机绝对路径或真实客户数据。

#### Scenario: dry-run 审计覆盖媒体风险

- **WHEN** 团队执行小程序媒体历史对象 dry-run 审计
- **THEN** 审计 SHALL 支持按资源类型抽样或批量检查 SKU 图片、SKU 视频 poster、品牌 Logo、Banner、品牌证书或小程序商品卡片图
- **AND** 输出 SHALL 包含 object 存在性、MIME、大小、缩略图是否存在、缩略图是否明显轻量、URL 是否可能 fallback、失败原因枚举和统计摘要
- **AND** dry-run SHALL NOT 写数据库或对象存储。

#### Scenario: 审计结果分类明确

- **WHEN** 审计完成
- **THEN** 结果 SHALL 将对象分类为已闭环、缺缩略图、缩略图无收益、URL fallback、object 缺失、权限异常或证据不足
- **AND** 对缺缩略图或缩略图无收益的历史对象 SHALL 标记是否需要独立回填或重生成
- **AND** 审计摘要 SHALL NOT 替代小程序受影响页面的 render evidence。

#### Scenario: apply 回填显式受控

- **WHEN** 审计结果需要 apply 回填或重生成
- **THEN** 系统 SHALL 要求显式 apply 参数、MySQL 与对象存储 bucket / prefix 备份确认、幂等验证、成功数量、失败数量、跳过数量和失败原因
- **AND** 重复执行 SHALL 保持幂等
- **AND** 任一失败项 SHALL 记录实际结果、期望结果、影响范围和重试条件。
